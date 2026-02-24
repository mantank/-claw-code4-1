#!/bin/bash
# grok-x-trends.sh - 用 Grok API x_search 搜 X/Twitter 过去24h AI热点
# 输出: 中文热点列表，含帖子链接
# 依赖: Mihomo 代理运行在 127.0.0.1:7890

GROK_API_KEY="xai-4YPImuiPnmESoKUHoKBbX7Mp1yX1IojfdBpSghrrA9ApexIkIaHgBZBFrhhnnsDFn5xQPPnEBQ9HObuG"
PROXY="http://127.0.0.1:7890"

RESPONSE=$(HTTPS_PROXY="$PROXY" HTTP_PROXY="$PROXY" \
  curl -s --connect-timeout 30 --max-time 150 https://api.x.ai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GROK_API_KEY" \
  -d '{
    "model": "grok-4-1-fast-reasoning",
    "stream": false,
    "input": [{
      "role": "user",
      "content": "Search X for the top 5 hottest AI topics from the past 24 hours. Target audience: Chinese indie developers and tech entrepreneurs. Focus on: AI coding tools, model releases, productivity breakthroughs, controversial AI takes, indie hacker wins with AI. For each topic output: 1) one-sentence Chinese summary 2) heat level 高/中/低 3) one post URL 4) why it matters to indie devs. Format as numbered list in Chinese."
    }],
    "tools": [{"type": "x_search"}]
  }' 2>&1)

# 提取文本内容
echo "$RESPONSE" | python3 -c "
import json, sys
d = json.loads(sys.stdin.read())
if 'error' in d:
    print('ERROR:', d['error'])
    sys.exit(1)
for item in d.get('output', []):
    if item.get('type') == 'message':
        for c in item.get('content', []):
            if c.get('type') == 'output_text':
                print(c['text'])
" 2>/dev/null
