from __future__ import annotations

import argparse
import base64
import json
import logging
import random
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("doubao-tts")


@dataclass(frozen=True)
class TTSConfig:
    api_url: str = "https://openspeech.bytedance.com/api/v1/tts"
    api_key: str = "xxx"
    cluster: str = "volcano_icl"
    uid: str = "豆包语音"
    voice_type: str = "S_O0JFH2mX1"
    encoding: str = "mp3"
    speed_ratio: float = 1.0


def synthesize(text: str, output: Path, config: TTSConfig = TTSConfig()) -> Path:
    """调用豆包 TTS 接口，将 text 合成语音并写入 output 文件。"""
    payload = {
        "app": {"cluster": config.cluster},
        "user": {"uid": config.uid},
        "audio": {
            "voice_type": config.voice_type,
            "encoding": config.encoding,
            "speed_ratio": config.speed_ratio,
        },
        "request": {
            "reqid": uuid.uuid4().hex,
            "text": text,
            "operation": "query",
        },
    }
    headers = {
        "x-api-key": config.api_key,
        "Content-Type": "application/json",
    }

    logger.info("请求 TTS：text=%s, voice=%s", text[:30], config.voice_type)

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(config.api_url, headers=headers, data=json.dumps(payload), timeout=60)
            resp.raise_for_status()
            break
        except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as e:
            if attempt == max_retries:
                raise RuntimeError(f"TTS 请求失败，已重试 {max_retries} 次: {e}") from e
            wait = random.uniform(3, 10)
            logger.warning("第 %d 次请求失败（%s），%.1f 秒后重试...", attempt, e, wait)
            time.sleep(wait)

    body = resp.json()

    if body.get("code") != 3000:
        raise RuntimeError(f"TTS 失败: code={body.get('code')}, message={body.get('message')}")

    audio_b64 = body.get("data")
    if not audio_b64:
        raise RuntimeError("响应缺少 data 字段")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(base64.b64decode(audio_b64))
    duration = body.get("addition", {}).get("duration")
    logger.info("已生成音频：%s（时长 %s ms）", output, duration)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="豆包 TTS 合成脚本")
    parser.add_argument("text", help="要合成的文本")
    parser.add_argument(
        "-o", "--output",
        default="output.mp3",
        help="输出 mp3 路径，默认 output.mp3（脚本所在目录）",
    )
    parser.add_argument("--voice", default=TTSConfig.voice_type, help="音色 voice_type")
    parser.add_argument("--speed", type=float, default=TTSConfig.speed_ratio, help="语速")
    args = parser.parse_args()

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = Path(__file__).parent / output_path

    config = TTSConfig(voice_type=args.voice, speed_ratio=args.speed)
    synthesize(args.text, output_path, config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
