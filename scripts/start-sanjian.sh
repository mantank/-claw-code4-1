#!/bin/bash
# start-sanjian.sh — 重建三剑客 tmux session
# 小龙虾重启后执行此脚本恢复三剑客工作环境

PROJECT="/root/.openclaw/workspace/projects/openclaw-cn"

# 如果 session 已存在就跳过
if tmux has-session -t sanjian 2>/dev/null; then
  echo "✅ sanjian session 已存在，无需重建"
  tmux list-windows -t sanjian
  exit 0
fi

echo "🔧 重建三剑客 tmux session..."
tmux new-session -d -s sanjian -n claude-code -x 220 -y 50
tmux new-window -t sanjian -n codex
tmux new-window -t sanjian -n gemini
tmux new-window -t sanjian -n workspace

tmux send-keys -t sanjian:claude-code "cd $PROJECT" Enter
tmux send-keys -t sanjian:codex "cd $PROJECT" Enter
tmux send-keys -t sanjian:gemini "cd $PROJECT" Enter
tmux send-keys -t sanjian:workspace "cd $PROJECT" Enter

echo "✅ 三剑客 session 已就绪"
tmux list-windows -t sanjian
