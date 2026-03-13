#!/bin/bash
# 飞书知识库AI日报同步脚本
# 用法: feishu-daily-sync.sh "2026-03-13" "/path/to/content.json"
# content.json 是飞书block格式的JSON文件
#
# 如果只传日期不传content文件，则只创建空节点并返回obj_token

APP_ID="cli_a908765086b85bc6"
APP_SECRET="4HZ5OiOueIU1PYCy59T48fpYvomTWELl"
SPACE_ID="7603748469693484257"
PARENT_NODE="Rbcyw0mT1isRxmkBGVdcCdMZn7c"  # AI日报目录节点

DATE="$1"
CONTENT_FILE="$2"

if [ -z "$DATE" ]; then
    echo "Usage: $0 <date> [content.json]"
    exit 1
fi

# 1. 获取tenant_access_token
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"${APP_ID}\",\"app_secret\":\"${APP_SECRET}\"}" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tenant_access_token','ERROR'))")

if [ "$TOKEN" = "ERROR" ]; then
    echo "ERROR: 获取token失败"
    exit 1
fi

# 2. 检查该日期的节点是否已存在
EXISTING=$(curl -s "https://open.feishu.cn/open-apis/wiki/v2/spaces/${SPACE_ID}/nodes?parent_node_token=${PARENT_NODE}&page_size=50" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import json, sys
d = json.load(sys.stdin)
items = d.get('data',{}).get('items',[])
for item in items:
    if '${DATE}' in item.get('title',''):
        print(item.get('node_token',''))
        break
else:
    print('NOT_FOUND')
")

if [ "$EXISTING" != "NOT_FOUND" ] && [ -n "$EXISTING" ]; then
    echo "该日期节点已存在: $EXISTING"
    # 获取obj_token
    OBJ_TOKEN=$(curl -s "https://open.feishu.cn/open-apis/wiki/v2/spaces/${SPACE_ID}/nodes/${EXISTING}" \
      -H "Authorization: Bearer $TOKEN" | python3 -c "import json,sys; print(json.load(sys.stdin).get('data',{}).get('node',{}).get('obj_token','ERROR'))")
else
    # 3. 创建新的wiki节点
    TITLE="📊 AI日报 | ${DATE}"
    RESULT=$(curl -s -X POST "https://open.feishu.cn/open-apis/wiki/v2/spaces/${SPACE_ID}/nodes" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"obj_type\":\"docx\",\"node_type\":\"origin\",\"title\":\"${TITLE}\",\"parent_node_token\":\"${PARENT_NODE}\"}")

    OBJ_TOKEN=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('data',{}).get('node',{}).get('obj_token','ERROR'))")
    NODE_TOKEN=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('data',{}).get('node',{}).get('node_token','ERROR'))")

    if [ "$OBJ_TOKEN" = "ERROR" ]; then
        echo "ERROR: 创建节点失败"
        echo "$RESULT"
        exit 1
    fi
    echo "创建节点成功: node=$NODE_TOKEN obj=$OBJ_TOKEN"
fi

# 4. 如果有内容文件，写入内容
if [ -n "$CONTENT_FILE" ] && [ -f "$CONTENT_FILE" ]; then
    WRITE_RESULT=$(curl -s -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/${OBJ_TOKEN}/blocks/${OBJ_TOKEN}/children" \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d @"${CONTENT_FILE}")

    STATUS=$(echo "$WRITE_RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print('OK' if d.get('code')==0 else d.get('msg', 'UNKNOWN_ERROR'))")
    echo "写入内容: $STATUS"
else
    echo "OBJ_TOKEN=$OBJ_TOKEN (无内容文件，仅创建节点)"
fi
