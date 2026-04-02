#!/bin/bash
# session-migrator.sh
# 将 SESSION-STATE.md 迁移为结构化 JSON 格式
# 基于 claw-code session_store.py 设计

SESSION_STATE="${HOME}/.openclaw/workspace/SESSION-STATE.md"
SESSION_JSON="${HOME}/.openclaw/workspace/.session-state.json"
SCHEMA="${HOME}/.openclaw/workspace/schemas/session-state-schema.json"

# 读取 session_status 输出
get_session_info() {
    local output
    output=$(openclaw session list 2>/dev/null | head -20)
    echo "$output"
}

# 迁移 MD → JSON
migrate_md_to_json() {
    if [ ! -f "$SESSION_STATE" ]; then
        echo "错误：找不到 $SESSION_STATE"
        return 1
    fi
    
    local session_id
    session_id=$(date +%s)-$(head /dev/urandom | tr -dc 'a-z0-9' | head -c 6)
    
    local started_at
    started_at=$(grep -oP '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}' "$SESSION_STATE" | head -1)
    [ -z "$started_at" ] && started_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    local model
    model=$(grep -oP 'model: \K[^\s]+' "$SESSION_STATE" | head -1)
    [ -z "$model" ] && model="unknown"
    
    local turns
    turns=$(grep -c "^## " "$SESSION_STATE" 2>/dev/null || echo 0)
    
    # 提取已完成升级模块
    local modules
    modules=$(grep -oP '2\.\d+' "$SESSION_STATE" | sort -u | tr '\n' ',' | sed 's/,$//')
    
    cat > "$SESSION_JSON" <<EOF
{
  "session_id": "${session_id}",
  "started_at": "${started_at}",
  "model": "${model}",
  "turns": ${turns},
  "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
  "context": {"used_percent": 0},
  "compactions": 0,
  "files_modified": [],
  "tasks_completed": [],
  "upgrade_modules_completed": [${modules//,/\"，\"}],
  "last_active": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
    echo "✅ 迁移完成 → $SESSION_JSON"
    cat "$SESSION_JSON"
}

# 展示当前状态
show_status() {
    echo "=== Session State 状态 ==="
    echo "Markdown: ${SESSION_STATE} ($(wc -l < "$SESSION_STATE" 2>/dev/null || echo 0) 行)"
    echo "JSON:     ${SESSION_JSON} ($(wc -l < "$SESSION_JSON" 2>/dev/null || echo 0) 行)"
    echo ""
    echo "Schema:   ${SCHEMA}"
}

case "${1:-status}" in
    migrate)
        migrate_md_to_json
        ;;
    status|*)
        show_status
        ;;
esac
