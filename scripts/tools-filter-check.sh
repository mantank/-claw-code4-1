#!/bin/bash
# tools-filter-check.sh
# 检查给定工具是否被当前 deny / denyPrefixes 规则阻止
# 用法: bash tools-filter-check.sh <tool_name>

TOOL="$1"
if [ -z "$TOOL" ]; then
    echo "用法: $0 <tool_name>"
    exit 1
fi

TOOL_LOWER=$(echo "$TOOL" | tr '[:upper:]' '[:lower:]')

# 当前 deny 列表（从 openclaw.json 读取）
DENY_NAMES=("rm" "dd" "shutdown" "reboot" "init")

# deny_prefixes（未来支持）
DENY_PREFIXES=()

# 检查 exact match
for name in "${DENY_NAMES[@]}"; do
    if [ "$TOOL_LOWER" = "$name" ]; then
        echo "DENY_EXACT: $TOOL 精确匹配黑名单 → $name"
        exit 0
    fi
done

# 检查 prefix match（当前为降级方案，仅提示）
for prefix in "${DENY_PREFIXES[@]}"; do
    if [[ "$TOOL_LOWER" == "$prefix"* ]]; then
        echo "DENY_PREFIX: $TOOL 匹配前缀 → $prefix*"
        exit 0
    fi
done

echo "ALLOW: $TOOL 未被阻止"
