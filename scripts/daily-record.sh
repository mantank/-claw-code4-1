#!/bin/bash
# 每日记录生成脚本 - 由cron在23:30 GMT+8触发
# 用法: daily-record.sh "内容" "日期(YYYY-MM-DD)"

NOTION_KEY="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"
DB_ID="304453f1-8074-8112-89f2-cb45a4ba29d9"
CONTENT="$1"
DATE="${2:-$(TZ=Asia/Shanghai date +%Y-%m-%d)}"
TITLE="每日记录 $DATE"

# Create page in 待办清单 database
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{
    \"parent\": {\"database_id\": \"$DB_ID\"},
    \"properties\": {
      \"事项名称\": {\"title\": [{\"text\": {\"content\": \"$TITLE\"}}]},
      \"分类\": {\"select\": {\"name\": \"每日记录\"}},
      \"状态\": {\"status\": {\"name\": \"完成\"}},
      \"日期\": {\"date\": {\"start\": \"$DATE\"}}
    },
    \"children\": [
      {
        \"object\": \"block\",
        \"type\": \"paragraph\",
        \"paragraph\": {
          \"rich_text\": [{\"type\": \"text\", \"text\": {\"content\": \"$(echo "$CONTENT" | head -c 1900)\"}}]
        }
      }
    ]
  }"
