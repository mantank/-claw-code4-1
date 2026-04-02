#!/bin/bash
# memory-mutex-unlock.sh
# 释放主题锁
# 用法: unlock.sh <topic> <agent_id>

WORKSPACE="${HOME}/.openclaw/workspace"
MUTEX_DIR="${WORKSPACE}/memory/.mutex"
TOPIC="$1"
AGENT="$2"
LOCK_FILE="${MUTEX_DIR}/${TOPIC}.lock"

if [ -z "$TOPIC" ] || [ -z "$AGENT" ]; then
    echo "用法: unlock.sh <topic> <agent_id>"
    exit 2
fi

if [ -f "$LOCK_FILE" ] && [ "$(cat "$LOCK_FILE")" = "$AGENT" ]; then
    rm "$LOCK_FILE"
    echo "RELEASED"
    exit 0
else
    echo "NOT_HELD"
    exit 1
fi
