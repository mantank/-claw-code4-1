#!/bin/bash
# Notion 每日记录页面管理
# 用法:
#   notion-daily-page.sh create "2026-02-25"          → 创建当天页面，返回 page_id
#   notion-daily-page.sh find "2026-02-25"            → 查找当天页面，返回 page_id
#   notion-daily-page.sh find-or-create "2026-02-25"  → 查找或创建，返回 page_id
#   notion-daily-page.sh append <page_id> <json_file> → 追加 blocks 到页面

NOTION_KEY="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"
DB_ID="bf0b46f590d943089e758c61c0a7b0e7"
NOTION_VER="2022-06-28"

ACTION="$1"
DATE="$2"

case "$ACTION" in
  find)
    # 按日期+标题前缀查找当天的每日记录
    curl -s -X POST "https://api.notion.com/v1/databases/${DB_ID}/query" \
      -H "Authorization: Bearer ${NOTION_KEY}" \
      -H "Notion-Version: ${NOTION_VER}" \
      -H "Content-Type: application/json" \
      -d "{
        \"filter\": {
          \"and\": [
            {\"property\": \"日期\", \"date\": {\"equals\": \"${DATE}\"}},
            {\"property\": \"标签 个人成长\", \"rich_text\": {\"equals\": \"每日记录\"}}
          ]
        }
      }" | python3 -c "
import json, sys
data = json.load(sys.stdin)
results = data.get('results', [])
if results:
    print(results[0]['id'])
else:
    print('NOT_FOUND')
"
    ;;

  create)
    # 创建新的每日记录页面（空壳，只有标题）
    curl -s -X POST "https://api.notion.com/v1/pages" \
      -H "Authorization: Bearer ${NOTION_KEY}" \
      -H "Notion-Version: ${NOTION_VER}" \
      -H "Content-Type: application/json" \
      -d "{
        \"parent\": {\"database_id\": \"${DB_ID}\"},
        \"properties\": {
          \"名称\": {\"title\": [{\"text\": {\"content\": \"📅 ${DATE} 每日记录\"}}]},
          \"日期\": {\"date\": {\"start\": \"${DATE}\"}},
          \"标签 个人成长\": {\"rich_text\": [{\"text\": {\"content\": \"每日记录\"}}]},
          \"作者\": {\"rich_text\": [{\"text\": {\"content\": \"零零壹\"}}]}
        }
      }" | python3 -c "import json,sys; print(json.load(sys.stdin).get('id','ERROR'))"
    ;;

  find-or-create)
    PAGE_ID=$(bash "$0" find "$DATE")
    if [ "$PAGE_ID" = "NOT_FOUND" ]; then
      PAGE_ID=$(bash "$0" create "$DATE")
    fi
    echo "$PAGE_ID"
    ;;

  append)
    # 追加 blocks 到已有页面
    PAGE_ID="$2"
    BLOCKS_FILE="$3"
    curl -s -X PATCH "https://api.notion.com/v1/blocks/${PAGE_ID}/children" \
      -H "Authorization: Bearer ${NOTION_KEY}" \
      -H "Notion-Version: ${NOTION_VER}" \
      -H "Content-Type: application/json" \
      -d @"${BLOCKS_FILE}" | python3 -c "import json,sys; d=json.load(sys.stdin); print('OK' if 'results' in d else d.get('message','ERROR'))"
    ;;

  *)
    echo "Usage: $0 {find|create|find-or-create|append} <date|page_id> [blocks_file]"
    exit 1
    ;;
esac
