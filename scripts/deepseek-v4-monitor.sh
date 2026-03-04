#!/bin/bash
# DeepSeek V4 发布监控脚本
# 检查是否已确认发布，避免重复通知

STATE_FILE="/root/.openclaw/workspace/memory/deepseek-v4-state.json"

# 如果已经通知过，直接退出
if [ -f "$STATE_FILE" ] && grep -q '"notified":true' "$STATE_FILE" 2>/dev/null; then
  echo "STATUS:ALREADY_NOTIFIED"
  exit 0
fi

echo "STATUS:MONITORING"
