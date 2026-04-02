#!/bin/bash
# self-diagnosis.sh
# 自我诊断 — 异常时自动生成诊断报告
# 第四阶段 4.2 产出

WORKSPACE="${HOME}/.openclaw/workspace"
DIAG_LOG="${WORKSPACE}/memory/diagnosis-log.md"
TIMESTAMP=$(date -u -d '+8 hours' '+%Y-%m-%d %H:%M GMT+8')

mkdir -p "$(dirname "$DIAG_LOG")"

echo "## 诊断报告 — $TIMESTAMP" >> "$DIAG_LOG"

# ── 1. OpenClaw 健康检查 ────────────────────────────
openclaw_status=$(openclaw gateway status 2>&1)
if echo "$openclaw_status" | grep -q "running\|active"; then
    echo "✅ Gateway: 运行中" >> "$DIAG_LOG"
else
    echo "❌ Gateway: 异常 — $openclaw_status" >> "$DIAG_LOG"
fi

# ── 2. Session 状态 ────────────────────────────────
session_out=$(openclaw session status 2>&1)
if echo "$session_out" | grep -q "error\|Error"; then
    echo "❌ Session: 错误" >> "$DIAG_LOG"
    echo "  $session_out" >> "$DIAG_LOG"
else
    echo "✅ Session: 正常" >> "$DIAG_LOG"
fi

# ── 3. 磁盘空间 ────────────────────────────────────
disk_avail=$(df -h "$WORKSPACE" 2>/dev/null | awk 'NR==2 {print $4}')
echo "📦 磁盘可用: $disk_avail" >> "$DIAG_LOG"

# ── 4. 内存状态 ────────────────────────────────────
mem_info=$(free -h 2>/dev/null | awk '/Mem:/ {print $3 "/" $2}')
echo "🧠 内存: $mem_info" >> "$DIAG_LOG"

# ── 5. API Key 可用性 ──────────────────────────────
# 测试 Gemini API
gemini_test=$(curl -s --max-time 5 "https://generativelanguage.googleapis.com/v1beta/models?key=AIzaSyDHiKNnvz71qzDIzk-I5ZVdyAwb2vuRxqo&pageSize=1" 2>&1 | grep -o "models\|error" | head -1)
if [ "$gemini_test" = "models" ]; then
    echo "✅ Gemini API: 正常" >> "$DIAG_LOG"
else
    echo "❌ Gemini API: 异常 — $gemini_test" >> "$DIAG_LOG"
fi

# ── 6. 最近错误日志 ────────────────────────────────
recent_errors=$(find "$WORKSPACE" -name "*.log" -mtime -1 -exec grep -l "ERROR\|error\|Exception" {} \; 2>/dev/null | head -3)
if [ -n "$recent_errors" ]; then
    echo "⚠️  最近错误日志: $recent_errors" >> "$DIAG_LOG"
else
    echo "✅ 无近期错误日志" >> "$DIAG_LOG"
fi

# ── 7. Cron 任务状态 ───────────────────────────────
crontab -l 2>/dev/null | grep -c "openclaw\|cron" || echo "0" > /tmp/cron_count.txt
cron_count=$(cat /tmp/cron_count.txt 2>/dev/null || echo "0")
echo "⏰ Cron 任务数: $cron_count" >> "$DIAG_LOG"

echo "" >> "$DIAG_LOG"

# ── 控制台快速输出 ──────────────────────────────────
echo "═══════════════════════════════════════"
echo "  自我诊断报告 — $(date -u -d '+8 hours' '+%H:%M')"
echo "═══════════════════════════════════════"
echo "  Gateway: $(echo "$openclaw_status" | grep -q 'running\|active' && echo '✅' || echo '❌')"
echo "  磁盘: $disk_avail | 内存: $mem_info"
echo "  Gemini API: $([ "$gemini_test" = "models" ] && echo '✅' || echo '❌')"
echo "  Cron任务: $cron_count 个"
echo "═══════════════════════════════════════"
echo "  完整报告已写入: $DIAG_LOG"
