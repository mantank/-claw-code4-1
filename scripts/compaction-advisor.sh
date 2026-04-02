#!/bin/bash
# compaction-advisor.sh
# 基于 claw-code query_engine 的 Compaction 双触发逻辑
# 监控 context 使用情况，当接近阈值时记录建议

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# 解析当前 session 状态（从 openclaw status 输出中提取）
get_session_context() {
    local output
    output=$(openclaw session status 2>/dev/null)
    
    # 提取 context 百分比
    local context_pct
    context_pct=$(echo "$output" | grep -oP 'Context: \K[0-9]+' | head -1)
    
    # 提取 context 绝对值
    local context_abs
    context_abs=$(echo "$output" | grep -oP 'Context: [0-9]+/[0-9]+' | grep -oP '/\K[0-9]+' | head -1)
    
    # 提取 compactions 次数
    local compactions
    compactions=$(echo "$output" | grep -oP 'Compactions: \K[0-9]+' | head -1)
    
    # 提取 tokens
    local tokens_in
    tokens_in=$(echo "$output" | grep -oP 'Tokens: \K[0-9]+' | head -1)
    local tokens_out
    tokens_out=$(echo "$output" | grep -oP 'Tokens: [0-9]+ in / \K[0-9]+' | head -1)
    
    echo "${context_pct:-0}|${context_abs:-0}|${compactions:-0}|${tokens_in:-0}|${tokens_out:-0}"
}

# 判断是否需要触发 compaction
check_compaction() {
    local context_pct="$1"
    local context_abs="$2"
    local compactions="$3"
    local tokens_in="$4"
    local tokens_out="$5"
    
    # claw-code 风格阈值
    local MAX_CONTEXT_PCT=80      # 80% context 就警告
    local MAX_TURNS=20           # 等价 max_turns
    local MAX_BUDGET_TOKENS=80000 # 等价 max_budget_tokens（保守值）
    
    # 估算当前轮次（按经验每轮约 3k tokens）
    local estimated_turns=$((tokens_in / 3000))
    
    local status="OK"
    local action=""
    local reason=""
    
    # 检查1：context 百分比
    if [ "$context_pct" -ge "$MAX_CONTEXT_PCT" ]; then
        status="WARN"
        action="建议触发 compaction"
        reason="context 使用已达 ${context_pct}%"
    fi
    
    # 检查2：估算轮次
    if [ "$estimated_turns" -ge "$MAX_TURNS" ]; then
        status="WARN"
        action="建议触发 compaction"
        reason="${reason}; 估算轮次约 ${estimated_turns} 轮"
    fi
    
    # 检查3：token 预算
    local total_tokens=$((tokens_in + tokens_out))
    if [ "$total_tokens" -ge "$MAX_BUDGET_TOKENS" ]; then
        status="WARN"
        action="建议触发 compaction"
        reason="${reason}; token 总量 ${total_tokens} 接近预算"
    fi
    
    # 记录
    local timestamp
    timestamp=$(date -u -d '+8 hours' '+%Y-%m-%d %H:%M')
    
    if [ "$status" = "WARN" ]; then
        echo "[${timestamp}] ⚠️ ${reason} | action: ${action}" >> "${HOME}/.openclaw/workspace/memory/compaction-log.md"
    fi
    
    echo "$status|$context_pct|$estimated_turns|$total_tokens"
}

# 主逻辑
read_context() {
    local ctx
    ctx=$(get_session_context)
    IFS='|' read -r context_pct context_abs compactions tokens_in tokens_out <<< "$ctx"
    
    local result
    result=$(check_compaction "$context_pct" "$context_abs" "$compactions" "$tokens_in" "$tokens_out")
    IFS='|' read -r status pct turns tokens <<< "$result"
    
    echo "Context: ${pct}% | 估算轮次: ${turns} | Token总量: ${tokens} | 状态: ${status}"
}

read_context
