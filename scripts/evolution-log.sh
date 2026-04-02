#!/bin/bash
# evolution-log.sh
# 进化日志 — 记录每次"自我改进"的内容
# 第四阶段 4.5 产出

WORKSPACE="${HOME}/.openclaw/workspace"
EVOLUTION_LOG="${WORKSPACE}/memory/evolution-log.md"
TIMESTAMP=$(date -u -d '+8 hours' '+%Y-%m-%d %H:%M GMT+8')

mkdir -p "$(dirname "$EVOLUTION_LOG")"

# ── 读取参数 ────────────────────────────────────────
CATEGORY="$1"      # self-tuning | self-diagnosis | self-extend | self-upgrade
ACTION="$2"        # 具体动作描述
RESULT="$3"         # 结果
METRICS="$4"       # 可选：指标变化

if [ -z "$CATEGORY" ] || [ -z "$ACTION" ]; then
    echo "用法: evolution-log.sh <category> <action> <result> [metrics]"
    exit 1
fi

# ── 追加记录 ────────────────────────────────────────
{
    echo "## 进化记录 — $TIMESTAMP"
    echo "类别: **$CATEGORY**"
    echo "动作: $ACTION"
    echo "结果: $RESULT"
    [ -n "$METRICS" ] && echo "指标: $METRICS"
    echo ""
} >> "$EVOLUTION_LOG"

# ── 更新汇总摘要 ─────────────────────────────────────
SUMMARY_FILE="${WORKSPACE}/memory/evolution-summary.md"
TOTAL_COUNT=$(grep -c "^## 进化记录" "$EVOLUTION_LOG" 2>/dev/null || echo "0")

{
    echo "## 最后更新: $TIMESTAMP"
    echo "- 类别: $CATEGORY"
    echo "- 动作: $ACTION"
    echo "- 结果: $RESULT"
    echo "- 累计进化次数: $TOTAL_COUNT"
    echo ""
} > "$SUMMARY_FILE"

echo "✅ 进化记录已保存 (#$TOTAL_COUNT)"
