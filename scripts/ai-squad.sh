#!/bin/bash
# ai-squad.sh — 001指挥Claude Code + Codex + Gemini 三Agent协同
# 用法: bash ai-squad.sh "你的任务描述"
# 例如: bash ai-squad.sh "帮我搭一个Python Flask Web API，支持用户注册登录"

TASK="${1:-请输入任务}"
WORKDIR="${2:-/root/.openclaw/workspace/projects/$(date +%Y%m%d-%H%M%S)}"
SESSION="ai-squad"

echo "🚀 AI Squad 启动"
echo "任务：$TASK"
echo "工作目录：$WORKDIR"
mkdir -p "$WORKDIR"

# 写任务文件，各Agent共享
cat > "$WORKDIR/TASK.md" << EOF
# 任务

$TASK

## 工作目录
$WORKDIR

## 分工（001统筹，各Agent认领）
- Claude Code：负责核心代码实现
- Codex：负责测试、调试、修复bug
- Gemini：负责文档、方案研究、搜索参考资料

## 协作规范
- 完成阶段性工作后在 $WORKDIR/STATUS.md 更新进度
- 遇到问题写入 $WORKDIR/ISSUES.md
- 最终产出整理到 $WORKDIR/OUTPUT/
EOF

# 杀掉已有的同名session避免冲突
tmux kill-session -t "$SESSION" 2>/dev/null

# 创建tmux session，分4个窗格
# 布局：左上=001(监控), 右上=Claude Code, 左下=Codex, 右下=Gemini
tmux new-session -d -s "$SESSION" -x 220 -y 50

# 窗格0：001监控台（左上）
tmux rename-window -t "$SESSION:0" "001-Monitor"
tmux send-keys -t "$SESSION:0" "cd $WORKDIR && echo '=== 001 监控台 ===' && echo '任务：$TASK' && echo '' && echo '等待各Agent就绪...' && watch -n 3 'echo \"--- STATUS ---\" && cat STATUS.md 2>/dev/null || echo \"进行中...\"'" Enter

# 创建右上窗格：Claude Code
tmux split-window -t "$SESSION:0" -h
tmux send-keys -t "$SESSION:0.1" "cd $WORKDIR && echo '=== Claude Code 就绪 ===' && echo '任务文件：$WORKDIR/TASK.md' && echo '' && echo '启动Claude Code...' && sleep 1 && claude" Enter

# 创建左下窗格：Codex  
tmux split-window -t "$SESSION:0.0" -v
tmux send-keys -t "$SESSION:0.2" "cd $WORKDIR && echo '=== Codex 就绪 ===' && sleep 2 && codex -a never" Enter

# 创建右下窗格：Gemini
tmux split-window -t "$SESSION:0.1" -v
tmux send-keys -t "$SESSION:0.3" "cd $WORKDIR && echo '=== Gemini 就绪 ===' && sleep 2 && gemini" Enter

# 调整布局
tmux select-layout -t "$SESSION:0" tiled

# 回到监控台
tmux select-pane -t "$SESSION:0.0"

echo ""
echo "✅ AI Squad 已启动！"
echo ""
echo "连接命令："
echo "  tmux attach -t $SESSION"
echo ""
echo "窗格说明："
echo "  左上(0): 001监控台 - 看各Agent进度"
echo "  右上(1): Claude Code - 核心编码"  
echo "  左下(2): Codex - 测试调试"
echo "  右下(3): Gemini - 研究文档"
echo ""
echo "操作提示："
echo "  切换窗格: Ctrl+B 然后按方向键"
echo "  退出tmux: Ctrl+B 然后按 D（后台保持运行）"
echo "  关闭squad: tmux kill-session -t $SESSION"
