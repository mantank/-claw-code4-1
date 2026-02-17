#!/bin/bash
# Notion 推送脚本
# 用法: notion-push.sh "标题" "内容" "类型(日报/日课/总结)" ["日期 YYYY-MM-DD"]

NOTION_KEY="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"
DATABASE_ID="bf0b46f590d943089e758c61c0a7b0e7"

TITLE="${1:-无标题}"
CONTENT="${2:-}"
TAG="${3:-日报}"
DATE="${4:-$(date -u -d '+8 hours' +%Y-%m-%d)}"

# 将内容按2000字符分块（Notion API限制）
# 构建children blocks
BLOCKS="[]"
if [ -n "$CONTENT" ]; then
  # 按换行分段，每段一个paragraph block
  BLOCKS=$(python3 -c "
import json, sys

content = sys.argv[1]
blocks = []
for line in content.split('\n'):
    line = line.strip()
    if not line:
        continue
    # 截断到2000字符
    chunks = [line[i:i+2000] for i in range(0, len(line), 2000)]
    for chunk in chunks:
        blocks.append({
            'object': 'block',
            'type': 'paragraph',
            'paragraph': {
                'rich_text': [{'type': 'text', 'text': {'content': chunk}}]
            }
        })
print(json.dumps(blocks))
" "$CONTENT")
fi

# 构建请求
PAYLOAD=$(python3 -c "
import json, sys
title = sys.argv[1]
date = sys.argv[2]
tag = sys.argv[3]
blocks = json.loads(sys.argv[4])

data = {
    'parent': {'database_id': '$DATABASE_ID'},
    'properties': {
        '名称': {'title': [{'text': {'content': title}}]},
        '日期': {'date': {'start': date}},
        '作者': {'rich_text': [{'text': {'content': '零零壹'}}]},
        '标签 个人成长': {'rich_text': [{'text': {'content': tag}}]}
    },
    'children': blocks
}
print(json.dumps(data, ensure_ascii=False))
" "$TITLE" "$DATE" "$TAG" "$BLOCKS")

curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"
