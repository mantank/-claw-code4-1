#!/bin/bash
# self-dashboard.sh
# OpenClaw 自监控仪表盘 — 第三阶段 3.3 产出
# 整合：system-check + compaction-advisor + workspace-scan + session-status

WORKSPACE="${HOME}/.openclaw/workspace"
LOG_DIR="${WORKSPACE}/memory/dashboard-logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date -u -d '+8 hours' '+%Y-%m-%d %H:%M GMT+8')
LOG_FILE="${LOG_DIR}/dashboard-$(date -u -d '+8 hours' '+%Y-%m-%d').md"

echo "## 自监控仪表盘 — $TIMESTAMP" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# ── 1. 系统状态 ──────────────────────────────────────
echo "### 1. 系统状态" >> "$LOG_FILE"
openclaw --version 2>/dev/null | head -1 | sed 's/^/  /' >> "$LOG_FILE"
echo "  Node: $(node --version 2>/dev/null)" >> "$LOG_FILE"
echo "  Python: $(python3 --version 2>/dev/null | sed 's/Python //')" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# ── 2. Context / Compaction 状态 ─────────────────────
echo "### 2. Context 与 Compaction" >> "$LOG_FILE"
output=$(openclaw session status 2>/dev/null)
context_pct=$(echo "$output" | grep -oP 'Context: \K[0-9]+' | head -1)
context_abs=$(echo "$output" | grep -oP 'Context: [0-9]+/[0-9]+' | grep -oP '/\K[0-9]+' | head -1)
compactions=$(echo "$output" | grep -oP 'Compactions: \K[0-9]+' | head -1)
tokens_in=$(echo "$output" | grep -oP 'Tokens: \K[0-9]+' | head -1)
tokens_out=$(echo "$output" | grep -oP 'Tokens: [0-9]+ in / \K[0-9]+' | head -1)

# 阈值判断
MAX_CONTEXT_PCT=80
MAX_TURNS=20
MAX_BUDGET_TOKENS=80000
estimated_turns=$((tokens_in / 3000))
total_tokens=$((tokens_in + tokens_out))

echo "  Context: ${context_pct:-0}% | 上限: ${context_abs:-?}k" >> "$LOG_FILE"
echo "  Compactions: ${compactions:-0}" >> "$LOG_FILE"
echo "  Tokens in: ${tokens_in:-0} | out: ${tokens_out:-0} | total: ${total_tokens:-0}" >> "$LOG_FILE"
echo "  估算轮次: ${estimated_turns:-0}" >> "$LOG_FILE"

# 状态判定
if [ "${context_pct:-0}" -ge "$MAX_CONTEXT_PCT" ]; then
    echo "  ⚠️ Context 使用率已达 ${context_pct}% — 建议触发 compaction" >> "$LOG_FILE"
elif [ "${estimated_turns:-0}" -ge "$MAX_TURNS" ]; then
    echo "  ⚠️ 轮次已达 ${estimated_turns} — 建议触发 compaction" >> "$LOG_FILE"
else
    echo "  ✅ Context 状态正常" >> "$LOG_FILE"
fi
echo "" >> "$LOG_FILE"

# ── 3. Workspace 活跃度 ─────────────────────────────
echo "### 3. Workspace 活跃度" >> "$LOG_FILE"
total_files=$(find "$WORKSPACE" -type f 2>/dev/null | wc -l)
recent_24h=$(find "$WORKSPACE" -type f -mtime -1 ! -path '*/.git/*' 2>/dev/null | wc -l)
recent_7d=$(find "$WORKSPACE" -type f -mtime -7 ! -path '*/.git/*' 2>/dev/null | wc -l)
disk_usage=$(du -sh "$WORKSPACE" 2>/dev/null | cut -f1)

echo "  总文件: $total_files | 今日活跃: $recent_24h | 7日活跃: $recent_7d" >> "$LOG_FILE"
echo "  磁盘占用: $disk_usage" >> "$LOG_FILE"

# Git 状态
if [ -d "${WORKSPACE}/.git" ]; then
    last_commit=$(git -C "$WORKSPACE" log -1 --format="%ci" 2>/dev/null | cut -d' ' -f1)
    days_since=$((($(date +%s) - $(git -C "$WORKSPACE" log -1 --format=%ct 2>/dev/null)) / 86400))
    echo "  Git: 最后 commit ${days_since:-0} 天前 ($last_commit)" >> "$LOG_FILE"
fi
echo "" >> "$LOG_FILE"

# ── 4. API Key 健康度 ──────────────────────────────
echo "### 4. API Key 状态" >> "$LOG_FILE"
# 检查各 key 是否存在（不暴露值）
gemini_key=$(grep -q "AIzaSyDHiKNnvz71qzDIzk" "${WORKSPACE}/TOOLS.md" 2>/dev/null && echo "✅" || echo "❌")
openrouter_key=$(grep -q "sk-or-v1-f3becdb1de34" "${WORKSPACE}/TOOLS.md" 2>/dev/null && echo "✅" || echo "❌")
grok_key=$(grep -q "xai-4YPImuiPnmESoKU" "${WORKSPACE}/TOOLS.md" 2>/dev/null && echo "✅" || echo "❌")
echo "  Gemini API: $gemini_key" >> "$LOG_FILE"
echo "  OpenRouter: $openrouter_key" >> "$LOG_FILE"
echo "  Grok API: $grok_key" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# ── 5. 团队状态快照 ───────────────────────────────
echo "### 5. 团队状态" >> "$LOG_FILE"
# 检查各 agent 最后活跃时间
for agent_dir in /root/.openclaw-{002,003,004}; do
    if [ -d "$agent_dir" ]; then
        name=$(basename "$agent_dir")
        last_active=$(find "$agent_dir/workspace" -type f ! -path '*/.git/*' -mtime -0.5 2>/dev/null | wc -l)
        echo "  $name: ${last_active} 个今日活跃文件" >> "$LOG_FILE"
    fi
done
echo "" >> "$LOG_FILE"

echo "---" >> "$LOG_FILE"

# ── 控制台输出 ──────────────────────────────────────
echo "═══════════════════════════════════════"
echo "  OpenClaw 自监控仪表盘 — $(date -u -d '+8 hours' '+%H:%M')"
echo "═══════════════════════════════════════"
echo "  Context: ${context_pct:-?}% | Compaction: ${compactions:-0} | Tokens: ${total_tokens:-0}"
echo "  Workspace: $total_files 文件 | $recent_24h 今日活跃"
echo "  Gemini: $gemini_key | OpenRouter: $openrouter_key | Grok: $grok_key"
if [ "${context_pct:-0}" -ge "$MAX_CONTEXT_PCT" ]; then
    echo "  ⚠️  建议触发 compaction"
else
    echo "  ✅ 系统正常"
fi
echo "═══════════════════════════════════════"
