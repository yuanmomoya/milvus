# Milvus 从入门到精通 — 视频教程制作指南

本文档整合了视频系列的设计规范、旁白风格、TTS 工具用法和完整制作工作流。
后续生成新章节视频时，以本文档为唯一参考。

---

## 一、项目概览

HyperFrames 视频脚本，配合 [HyperFrames by HeyGen](https://hyperframes.heygen.com) 渲染为教学视频。

### 目录结构

```
milvus-master-course-vidoe/
├── VIDEO_GUIDE.md                     # 本文件（唯一参考文档）
├── doubao_tts.py                      # 豆包 TTS 合成脚本
├── build_narration.py                 # 逐段 TTS + 拼接 + 时长 JSON
├── remap_timing.py                    # 自动重映射 HTML 场景时间
├── chapter-01-vector-database-basics/
│   ├── index.html                     # HyperFrames 视频脚本
│   ├── narration.md                   # 旁白文本（按场景分段，供人阅读）
│   ├── narration.txt                  # 纯文本旁白（喂给 TTS，段落间空行分隔）
│   ├── narration.mp3                  # TTS 生成的音频
│   ├── narration_timing.json          # 各场景时长数据
│   └── chapter-01.mp4                 # 渲染输出
├── chapter-02-milvus-architecture/
│   └── ...（同上结构）
└── ...（后续章节）
```

### 视频风格

- **诙谐幽默**：用生活类比解释技术概念（物流中心、图书馆、北京找人）
- **视觉节奏**：每场景 8-15 秒，入场动画 stagger，无跳切
- **深色科技感**：深夜蓝底 + 青绿/紫色高亮
- **中文优先**：所有文字、旁白均为中文

---

## 二、设计系统（Design System）

### Brand Personality

技术教学 + 诙谐幽默。像一个懂行的朋友在白板前给你讲课，偶尔抖个包袱。
视觉上要有"高级感的趣味"——不是低幼卡通，而是用生动类比和动态图解让抽象概念变得直觉化。

### Palette

| Role       | Hex       | Usage                          |
|------------|-----------|--------------------------------|
| Background | `#0f1729` | 深夜蓝，主背景                 |
| Surface    | `#1a2744` | 卡片、代码块背景               |
| Foreground | `#e8edf5` | 主文字                         |
| Muted      | `#8b9dc3` | 次要文字、标签                 |
| Accent     | `#00d4aa` | 数据流、高亮、关键概念         |
| Warm       | `#f59e0b` | 警告、对比、类比中的"传统方式" |
| Violet     | `#a78bfa` | 算法、索引、技术名词           |
| Error      | `#ef4444` | 错误示例、性能瓶颈             |

### Typography

| Role      | Font                                    | Weight  | Size Range |
|-----------|-----------------------------------------|---------|------------|
| Headline  | "Noto Sans SC", "PingFang SC", sans-serif | 700-900 | 72-120px   |
| Body      | "Noto Sans SC", "PingFang SC", sans-serif | 400-500 | 32-48px    |
| Code      | "JetBrains Mono", "Fira Code", monospace  | 400     | 28-36px    |
| Label     | "Noto Sans SC", sans-serif                | 500     | 24-32px    |

### Motion

- 入场动画：0.4-0.7s，ease: power3.out / expo.out
- 代码出现：逐行 stagger 0.15s，typewriter 感
- 图表绘制：路径 draw-on 效果，0.8-1.2s
- 场景切换：crossfade 0.4s 或 blur-through 0.3s
- 背景装饰：缓慢呼吸 scale 1.0-1.05，drift

### Scene Layout Principles

- 左侧 60% 放主要内容（文字、图解）
- 右侧 40% 放辅助视觉（代码、示意图）
- 或全屏居中用于标题场景和重点强调
- **底部 100px 必须保留给字幕条**（`scene-content` 设 `padding-bottom: 160px`，避免主内容被字幕遮挡）

### What NOT to Do

- 不要用渐变文字（gradient text）
- 不要用纯黑 #000 背景
- 不要所有元素都居中对齐
- 不要用 emoji 代替设计元素
- 不要让代码块小于 28px
- 不要让 scene 的 `data-duration` 超过到下一个 scene 的间隔

---

## 三、场景时序规则（Scene Timing Rules）

⚠️ **重要：避免场景重叠**

HyperFrames 的 scene 是绝对定位叠加渲染的，不会自动隐藏前一个 scene。

**铁律：每个 scene 的 `data-duration` 必须正好等于下一个 scene 的 `data-start` - 当前 scene 的 `data-start`。**

举例（正确）：

```html
<div data-start="0"    data-duration="11.5"></div>  <!-- 11.5 - 0    = 11.5 ✓ -->
<div data-start="11.5" data-duration="12.8"></div>  <!-- 24.3 - 11.5 = 12.8 ✓ -->
<div data-start="24.3" data-duration="17.7"></div>  <!-- 42.0 - 24.3 = 17.7 ✓ -->
```

**最后一个 scene** 的 `data-duration` = `composition data-duration - 该 scene data-start`。

**Composition 总时长** = 音频时长（按 narration.mp3 的真实秒数设置）。

---

## 四、旁白风格规范

### 前置说明（每章开头）

每章 Hook 之后、正式内容之前，必须有一段"前置说明"（约 2-3 句），告诉学员：
- 这一章要解决什么问题 / 学完能获得什么
- 大致会覆盖哪几个知识点

示例：
> 这一章我们搞明白三件事：向量是什么、怎么衡量相似度、以及为什么需要索引加速。

### 段落衔接（Scene 之间）

每个 Scene 的开头需要一句"承接句"，把上一个 Scene 的结论自然引向当前 Scene 的主题。

衔接模式：
1. 因果型："知道了 X，下一个问题自然就来了：Y"
2. 递进型："光有 X 还不够，还需要 Y"
3. 转折型："X 在小规模下没问题，但一旦数据量上来……"
4. 总结引出型："刚才讲的是原理，接下来看它在工程上怎么落地"

反面示例（避免）：
- "具体来说：" ← 太生硬，像 PPT 翻页
- "接下来我们看 X" ← 没有逻辑连接
- 直接开始新概念，没有任何过渡

### 总结与预告（每章结尾）

- 用一句话概括本章核心收获
- 用一句话预告下一章内容，建立期待感

### 语速与节奏

- 中文旁白目标语速：约 3.5-4 字/秒
- 每个 Scene 目标时长：8-15 秒（TTS 实际时长为准）
- 全章目标时长：120-200 秒

---

## 五、制作工作流

### 完整流程

```
编辑 narration.md/txt → 生成 TTS 音频 → 同步 HTML 时间轴 → 渲染视频
```

### Step 1: 编辑旁白

- `narration.md` — 带 Scene 标记的结构化旁白（供人阅读和 AI 参考）
- `narration.txt` — 纯文本，段落间用空行分隔（喂给 TTS）

每个段落对应一个 Scene，段落顺序 = Scene 顺序。

### Step 2: 生成 TTS 音频

```bash
cd milvus-master-course-vidoe
python3 build_narration.py
```

脚本做三件事：
1. 按空行拆分 `narration.txt` 为多个段落
2. 逐段调用豆包 TTS（`doubao_tts.py`）生成 mp3
3. 用 ffmpeg 拼接成完整 `narration.mp3`，输出 `narration_timing.json`

输出的 `narration_timing.json` 格式：
```json
{
  "total_duration": 191.21,
  "scenes": [
    {"index": 0, "start": 0.0, "duration": 21.26, "chars": 112},
    {"index": 1, "start": 21.26, "duration": 15.26, "chars": 78}
  ]
}
```

### Step 3: 同步 HTML 时间轴

```bash
python3 remap_timing.py
```

脚本读取 `narration_timing.json`，自动更新 `index.html` 中的：
- composition 容器的 `data-duration`
- `<audio>` 的 `data-duration`
- 每个 scene 的 `data-start` 和 `data-duration`
- GSAP timeline 中所有动画的绝对时间（按比例缩放）

**注意：** `remap_timing.py` 中硬编码了旧的场景时间。如果 HTML 已被更新过，需要先更新脚本中的 `old_chXX` 数组为当前值。

### Step 4: 渲染视频

```bash
source ~/.nvm/nvm.sh && nvm use 22
cd chapter-XX-xxx
npx hyperframes render --output chapter-XX.mp4
```

### 单独生成一段 TTS

```bash
python3 doubao_tts.py "要合成的文本" -o chapter-XX/narration.mp3
```

参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `text` | 待合成文本（位置参数，必填） | — |
| `-o`, `--output` | 输出 mp3 路径 | `output.mp3` |
| `--voice` | 音色 voice_type | `S_O0JFH2mX1` |
| `--speed` | 语速 speed_ratio | `1.0` |

Python 调用：

```python
from pathlib import Path
from doubao_tts import synthesize, TTSConfig

synthesize("你好，这是测试", Path("test.mp3"), TTSConfig(speed_ratio=1.1))
```

---

## 六、豆包 TTS API 参考

```bash
curl -L -X POST 'https://openspeech.bytedance.com/api/v1/tts' \
  -H 'x-api-key: 1232f6e7-4fdb-4409-884a-184254bdc769' \
  -H 'Content-Type: application/json' \
  -d '{
    "app": {"cluster": "volcano_icl"},
    "user": {"uid": "豆包语音"},
    "audio": {"voice_type": "S_O0JFH2mX1", "encoding": "mp3", "speed_ratio": 1.0},
    "request": {"reqid": "unique-id", "text": "要合成的文本", "operation": "query"}
  }'
```

响应中 `data` 字段为 base64 编码的 mp3 音频。

---

## 七、依赖环境

| 工具 | 版本 | 用途 |
|------|------|------|
| Python | 3.12+（miniforge3） | TTS 脚本、时间轴工具 |
| Node.js | 22（via nvm） | HyperFrames 渲染 |
| ffmpeg / ffprobe | 系统安装 | 音频拼接、时长检测 |
| requests | Python 包 | 调用豆包 TTS API |

---

## 八、字幕规范

字幕从第 03 章开始默认启用。底部固定半透明条 + 旁白逐句淡入淡出。

### 视觉样式

- **位置**：底部 100px 高度，跨整个 1920px 宽度
- **背景**：`rgba(15, 23, 41, 0.85)` 深夜蓝半透明
- **顶部边框**：`1px solid rgba(0, 212, 170, 0.3)` 青绿色细线作为分隔
- **z-index: 100**，叠加在所有 scene 之上
- **文字**：34px，font-weight 500，`#e8edf5` 白色，水平居中
- **宽度**：`width: 88%`，超长单句用 `text-overflow: ellipsis` 省略

### HTML 结构

字幕层是独立的 `clip`，跨整个 composition 时长，每句字幕一个 `<div>`：

```html
<div id="subtitle-bar" class="subtitle-layer clip"
     data-start="0" data-duration="TOTAL" data-track-index="99">
  <div class="subtitle-bg"></div>
  <div class="subtitle-text" id="sub-00">第一句旁白</div>
  <div class="subtitle-text" id="sub-01">第二句旁白</div>
  ...
</div>
```

```css
.subtitle-layer { position: absolute; bottom: 0; left: 0; width: 100%; height: 100px; z-index: 100; }
.subtitle-bg { position: absolute; inset: 0; background: rgba(15, 23, 41, 0.85);
               border-top: 1px solid rgba(0, 212, 170, 0.3); }
.subtitle-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                 font-size: 34px; font-weight: 500; color: #e8edf5; text-align: center;
                 width: 88%; opacity: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
```

### 拆分与时间分配规则

1. **句级拆分**：每个 scene 的旁白按中文标点 `。！？` 拆成 2-4 句短句
2. **时间分配**：每句的显示时长按字符数比例分摊到所属 scene 的时长内
   ```
   句 i 的 duration = scene.duration × (chars_i / 总字符数)
   句 i 的 start    = scene.start + 前面所有句的 duration 之和
   ```
3. **淡入淡出**：每句 GSAP `fromTo` 0 → 1 用 0.25s 淡入；结束前 0.3s 触发 0 淡出
   ```js
   tl.fromTo("#sub-00", {opacity:0}, {opacity:1, duration:0.25, ease:"power2.out"}, startTime);
   tl.to("#sub-00", {opacity:0, duration:0.25, ease:"power2.in"}, endTime - 0.3);
   ```

### 主内容避让

`scene-content` 必须设置 `padding-bottom: 160px`（100px 字幕条 + 60px 缓冲），
确保正文不会被字幕遮挡。

### 自动生成

`gen_chapter03.py` 是带字幕的章节生成器模板，可复用：
- 读取 `narration_timing.json` 拿到每个 scene 的精确时长
- 读取 `narration.txt` 按段落对应 scene
- 自动按句拆分 + 计算时间 + 输出完整 `index.html`

新章节做带字幕视频时，复制 `gen_chapter03.py` 为 `gen_chapterXX.py`，
修改 `CH_DIR` 和 `SCENE_VISUALS`（每个 scene 的标题和要点列表）即可。

---

## 九、章节对应关系

| 视频目录 | 对应教程文档 | 字幕 |
|----------|-------------|------|
| chapter-01-vector-database-basics | docs/01-向量数据库基础.md | ✗ |
| chapter-02-milvus-architecture | docs/02-Milvus整体架构.md | ✗ |
| chapter-03-quick-start | docs/03-Milvus快速开始.md | ✓ |
