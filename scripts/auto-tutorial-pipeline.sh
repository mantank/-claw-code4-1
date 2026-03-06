#!/bin/bash
# auto-tutorial-pipeline.sh
# 001全权执行：003采集完 → Gemini规划 → Claude Code写入 → Codex审核 → build → push
# 旭已授权，无需再确认

OUTPUT="/root/.openclaw-003/workspace/output/tutorials-raw.json"
PLAN="/tmp/tutorials-plan.md"
PROJECT="/root/.openclaw/workspace/projects/openclaw-cn"
LOG="/root/.openclaw/workspace/memory/tutorial-task-log.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() { echo "[$TIMESTAMP] $1" | tee -a "$LOG"; }

# ── 阶段1：检查003输出文件 ──────────────────────────────
if [ ! -f "$OUTPUT" ]; then
  log "⏳ 阶段1: 文件不存在，003还在初始化"
  exit 0
fi

# 检查文件大小（太小说明还没写够）
SIZE=$(wc -c < "$OUTPUT")
if [ "$SIZE" -lt 500 ]; then
  log "⏳ 阶段1: 文件太小($SIZE bytes)，003还在采集"
  exit 0
fi

# 检查第一批是否完成
BATCH1_DONE=$(grep -c '"status": "done"' "$OUTPUT" 2>/dev/null || echo 0)
if [ "$BATCH1_DONE" -eq 0 ]; then
  # 检查文件是否30分钟内有更新
  MODIFIED=$(stat -c %Y "$OUTPUT" 2>/dev/null || echo 0)
  NOW=$(date +%s)
  DIFF=$((NOW - MODIFIED))
  if [ "$DIFF" -gt 1800 ]; then
    log "⚠️ 阶段1: 文件超过30分钟未更新($DIFF 秒)，003可能卡住了"
    exit 2  # 让监控cron来唤醒003
  fi
  log "⏳ 阶段1: 第一批采集中，文件 ${DIFF}秒 前更新，继续等待"
  exit 0
fi

log "✅ 阶段1: 003至少完成一批采集，进入质量检查"

# ── 阶段2：质量检查 ─────────────────────────────────────
ITEM_COUNT=$(python3 -c "
import json
try:
    with open('$OUTPUT') as f:
        content = f.read()
    # 提取JSON数组
    import re
    matches = re.findall(r'\{[^{}]+\"title\"[^{}]+\}', content)
    print(len(matches))
except Exception as e:
    print(0)
" 2>/dev/null)

log "📊 阶段2: 当前采集条目数: $ITEM_COUNT"

if [ "$ITEM_COUNT" -lt 10 ]; then
  log "⏳ 阶段2: 条目不足10条，继续等待003采集"
  exit 0
fi

log "✅ 阶段2: 条目够了，准备让三剑客处理"
exit 3  # 信号：数据就绪，可以启动三剑客
