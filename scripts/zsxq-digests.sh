#!/bin/bash
# 生财有术精华帖采集脚本
# 用法: bash scripts/zsxq-digests.sh [count] [scope]
# scope: digests=精华 all=最新

COUNT="${1:-10}"
SCOPE="${2:-digests}"
COOKIE="zsxq_access_token=9DED7F62-5A95-4E52-9FE5-F44270AB368A_B12E75520B50E663"

API="https://api.zsxq.com/v2/groups/1824528822/topics?scope=${SCOPE}&count=${COUNT}&end_time=9999999999999"

raw=$(curl -s "$API" \
  -H "Cookie: $COOKIE" \
  -H "User-Agent: Mozilla/5.0")

echo "$raw" | python3 -c "
import json, sys, re, html
raw = sys.stdin.read()
try:
    d = json.loads(raw)
except:
    print('JSON解析失败')
    sys.exit(1)

if d.get('succeeded') != True:
    print('❌ 请求失败:', d.get('succeed_code', d.get('message','')))
    sys.exit(1)

topics = d.get('resp_data', {}).get('topics', [])
if not topics:
    print('⚠️ 无数据（可能cookie过期）')
    sys.exit(1)

print(f\"获取到 {len(topics)} 条{'精华' if '$SCOPE' == 'digests' else '最新'}帖\n\")

for i, t in enumerate(topics, 1):
    talk = t.get('talk', {})
    owner = talk.get('owner', {})
    text = talk.get('text', '')
    # 解析HTML实体
    text = html.unescape(text)
    # 去掉HTML标签
    text = re.sub(r'<[^>]+>', '', text).strip()
    # 去掉多余空白
    text = re.sub(r'\s+', ' ', text)
    
    author = owner.get('name', '?')
    alias = owner.get('alias', '')
    create_time = t.get('create_time', '')[:10]
    topic_id = t.get('topic_id', '')
    url = f\"https://wx.zsxq.com/dweb2/index/topic/{topic_id}\"
    
    # 判断类型
    has_voice = bool(t.get('content_voice'))
    has_image = bool(t.get('content_image'))
    msg_type = '🔊' if has_voice else ('📷' if has_image else '📝')
    
    print(f\"{msg_type} {i}. 【{author}】{create_time}\")
    print(f\"   {text[:120]}{'...' if len(text) > 120 else ''}\")
    print(f\"   🔗 {url}\")
    print()
" SCOPE="$SCOPE"
