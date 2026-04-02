#!/bin/bash
# memory-mutex-dedup.sh
# 检查即将写入的内容是否与已记录的事实重复
# 用法: dedup.sh <topic> <content_snippet>
# 输出: DUPLICATE 或 NEW

WORKSPACE="${HOME}/.openclaw/workspace"
MUTEX_DIR="${WORKSPACE}/memory/.mutex"
TOPIC="$1"
SNIPPET="$2"

FACT_FILE="${WORKSPACE}/memory/facts.md"

if [ -z "$TOPIC" ] || [ -z "$SNIPPET" ]; then
    echo "用法: dedup.sh <topic> <content_snippet>"
    exit 2
fi

# 简单实现：在 facts.md 中搜索 snippet 的关键词
# 实际使用时可按需扩展更复杂的匹配逻辑
if [ -f "$FACT_FILE" ]; then
    # 取snippet前30字符作为关键词
    KEYWORD=$(echo "$SNIPPET" | cut -c1-30 | tr ' ' '\n' | head -1)
    if grep -q "$KEYWORD" "$FACT_FILE" 2>/dev/null; then
        echo "DUPLICATE"
        exit 0
    fi
fi

echo "NEW"
exit 1
