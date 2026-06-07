#!/bin/bash
source ~/.nvm/nvm.sh && nvm use 22

BASE="/Users/changmeng.yuan.o/Desktop/milvus/milvus-master-course-vidoe"
cd "$BASE"

for dir in chapter-*/; do
  ch_num=$(echo "$dir" | grep -o '[0-9]\{2\}')
  output="${dir}chapter-${ch_num}.mp4"

  if [ -f "$output" ]; then
    echo "SKIP: $output already exists"
    continue
  fi

  echo "RENDER: $dir -> $output"
  cd "$dir"
  npx hyperframes render --output "chapter-${ch_num}.mp4" 2>&1 | grep -E "(complete|error|Error)"
  cd "$BASE"
done

echo "ALL DONE"
