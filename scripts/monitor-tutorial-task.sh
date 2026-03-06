#!/bin/bash
# monitor-tutorial-task.sh — 每10分钟检查教程采集进度

OUTPUT="/root/.openclaw-003/workspace/output/tutorials-raw.json"
TASK_LOG="/root/.openclaw/workspace/memory/tutorial-task-log.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] 检查教程采集进度..."

# 检查输出文件是否存在
if [ ! -f "$OUTPUT" ]; then
  echo "[$TIMESTAMP] 文件不存在，003可能还在初始阶段" >> "$TASK_LOG"
  exit 0
fi

# 统计条目数量
COUNT=$(python3 -c "
import json
try:
    data = [l for l in open('$OUTPUT') if l.strip().startswith('{') and '\"title\"' in l]
    print(len(data))
except:
    print(0)
" 2>/dev/null || echo "0")

# 检查batch完成标记
BATCH1=$(grep -c '"batch": 1' "$OUTPUT" 2>/dev/null || echo "0")
BATCH2=$(grep -c '"batch": 2' "$OUTPUT" 2>/dev/null || echo "0")

echo "[$TIMESTAMP] 当前条目数: $COUNT | batch1: $BATCH1 | batch2: $BATCH2" >> "$TASK_LOG"
echo "[$TIMESTAMP] 进度 — 条目: $COUNT, 第一批: $([ $BATCH1 -gt 0 ] && echo '✅完成' || echo '⏳进行中'), 第二批: $([ $BATCH2 -gt 0 ] && echo '✅完成' || echo '待开始')"

