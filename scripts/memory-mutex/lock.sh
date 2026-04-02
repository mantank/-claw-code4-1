#!/bin/bash
# memory-mutex-lock.sh
# 记忆互斥锁 — Claim 一个主题写入权
# 用法: lock.sh <topic> <agent_id>
# 成功：输出 "ACQUIRED" 并 exit 0
# 失败：输出 "HELD_BY: <owner>" 并 exit 1

WORKSPACE="${HOME}/.openclaw/workspace"
MUTEX_DIR="${WORKSPACE}/memory/.mutex"
mkdir -p "$MUTEX_DIR"

TOPIC="$1"
AGENT="$2"
LOCK_FILE="${MUTEX_DIR}/${TOPIC}.lock"

if [ -z "$TOPIC" ] || [ -z "$AGENT" ]; then
    echo "用法: lock.sh <topic> <agent_id>"
    exit 2
fi

# 检查是否已有锁
if [ -f "$LOCK_FILE" ]; then
    HOLDER=$(cat "$LOCK_FILE")
    if [ "$HOLDER" = "$AGENT" ]; then
        # 自己持有，可重入
        echo "ACQUIRED"
        exit 0
    else
        echo "HELD_BY: $HOLDER"
        exit 1
    fi
fi

# 尝试获取锁（原子操作）
echo "$AGENT" > "$LOCK_FILE"
if [ "$(cat "$LOCK_FILE")" = "$AGENT" ]; then
    echo "ACQUIRED"
    exit 0
else
    echo "HELD_BY: $(cat "$LOCK_FILE")"
    exit 1
fi
