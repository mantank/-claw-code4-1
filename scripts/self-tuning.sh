#!/bin/bash
# self-tuning.sh
# 自我调参 — 根据 cost/性能数据自动调整 compaction 策略
# 第四阶段 4.1 产出

WORKSPACE="${HOME}/.openclaw/workspace"
CONFIG="${HOME}/.openclaw/openclaw.json"
LOG="${WORKSPACE}/memory/auto-tuning-log.md"

mkdir -p "$(dirname "$LOG")"

TIMESTAMP=$(date -u -d '+8 hours' '+%Y-%m-%d %H:%M GMT+8')

# ── 读取当前 session 状态 ──────────────────────────────
get_status() {
    openclaw session status 2>/dev/null
}

status=$(get_status)
context_pct=$(echo "$status" | grep -oP 'Context[:\s]+\K[0-9]+' | head -1)
compactions=$(echo "$status" | grep -oP 'Compactions[:\s]+\K[0-9]+' | head -1)
tokens_in=$(echo "$status" | grep -oP 'Tokens[:\s]+\K[0-9]+' | head -1)
tokens_out=$(echo "$status" | grep -oP 'Tokens[:\s]+[0-9]+ in / \K[0-9]+' | head -1)
total_tokens=$((tokens_in + tokens_out))

# ── 读取历史 cost 数据 ────────────────────────────────
COST_LOG="${WORKSPACE}/memory/cost-log.md"
if [ -f "$COST_LOG" ]; then
    last_cost_line=$(tail -5 "$COST_LOG" 2>/dev/null | head -1)
    last_cost=$(echo "$last_cost_line" | grep -oP '[\d.]+' | head -1 || echo "0")
else
    last_cost="0"
fi

# ── 调参策略 ────────────────────────────────────────
ACTION="NONE"
REASON=""

# 阈值
CONTEXT_WARN=70
CONTEXT_CRITICAL=85
TOKEN_BUDGET=80000

ctx="${context_pct:-0}"
total_tok="${total_tokens:-0}"

if [ "$ctx" -ge "$CONTEXT_CRITICAL" ] 2>/dev/null; then
    ACTION="COMPACT_NOW"
    REASON="Context ${ctx}% 超过临界值 85%，建议立即 compaction"
elif [ "$total_tok" -ge "$TOKEN_BUDGET" ] 2>/dev/null; then
    ACTION="COMPACT_NOW"
    REASON="Token 总量 ${total_tok} 超过预算 80k"
elif [ "$ctx" -ge "$CONTEXT_WARN" ] 2>/dev/null; then
    ACTION="SCHEDULE_COMPACTION"
    REASON="Context ${ctx}% 超过警告线 70%，建议近期 compaction"
else
    ACTION="OPTIMAL"
    REASON="当前状态良好，无需调整"
fi

# ── 写日志 ─────────────────────────────────────────
{
    echo "## 自我调参记录 — $TIMESTAMP"
    echo "Context: ${ctx}% | Tokens: ${total_tok} | Compactions: ${compactions:-0}"
    echo "Action: **$ACTION** — $REASON"
    echo ""
} >> "$LOG"

# ── 控制台输出 ──────────────────────────────────────
echo "═══════════════════════════════════════"
echo "  自我调参检查 — $(date -u -d '+8 hours' '+%H:%M')"
echo "═══════════════════════════════════════"
echo "  Context: ${ctx}% | Tokens: ${total_tok}"
echo "  动作: $ACTION"
echo "  原因: $REASON"
echo "═══════════════════════════════════════"

# 如果需要立即 compaction，输出指令
if [ "$ACTION" = "COMPACT_NOW" ]; then
    echo ""
    echo "⚠️  建议执行: /compact 或开启新 session"
fi
