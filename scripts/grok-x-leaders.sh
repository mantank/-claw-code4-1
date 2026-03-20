#!/bin/bash
# grok-x-leaders.sh - 抓取关注的AI大佬最新X/Twitter动态
# 用途: 定时推送大佬精华内容
# 依赖: Mihomo 代理 127.0.0.1:7890

GROK_API_KEY="xai-4YPImuiPnmESoKUHoKBbX7Mp1yX1IojfdBpSghrrA9ApexIkIaHgBZBFrhhnnsDFn5xQPPnEBQ9HObuG"
PROXY="http://127.0.0.1:7890"

RESPONSE=$(HTTPS_PROXY="$PROXY" HTTP_PROXY="$PROXY" \
  curl -s --connect-timeout 30 --max-time 150 https://api.x.ai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GROK_API_KEY" \
  -d '{
    "model": "grok-4-1-fast-reasoning",
    "stream": false,
    "input": [{"role": "user", "content": "Search X for the latest posts (past 24 hours) from these AI thought leaders: @karpathy (Andrej Karpathy), @DrJimFan (Jim Fan/NVIDIA), @emollick (Ethan Mollick), @ylecun (Yann LeCun), @AndrewYNg (Andrew Ng), @sama (Sam Altman), @swyx (swyx), @mattshumer_ (Matt Shumer), @skirano (Simon Willison), @levelsio. For each person who posted in the last 24 hours: 1) Their name and handle 2) Full post content in Chinese (at least 3-5 sentences, include key details, quotes, data points) 3) The exact post URL (MUST include the full URL like https://x.com/username/status/123456) 4) Why it matters to indie developers (2-3 sentences in Chinese). Skip anyone who did not post. Format each result as:\n\n【@username】\n原文链接: https://x.com/xxx/status/xxx\n正文: (详细中文摘要，至少3-5句话)\n对独立开发者的意义: (2-3句话)\n\nOutput all in Chinese."}],
    "tools": [{"type": "x_search"}]
  }' 2>&1)

# 提取文本内容
echo "$RESPONSE" | python3 -c "
import json, sys
raw = sys.stdin.read()
try:
    d = json.loads(raw)
    if d.get('error'):
        print('ERROR:', json.dumps(d['error'], ensure_ascii=False))
        sys.exit(1)
    for item in d.get('output', []):
        if item.get('type') == 'message':
            for c in item.get('content', []):
                if c.get('type') == 'output_text':
                    print(c['text'])
except json.JSONDecodeError:
    print(f'PROXY/NETWORK ERROR: {raw[:200]}')
    sys.exit(1)
except Exception as e:
    print(f'PARSE ERROR: {e}')
    print('RAW:', raw[:300])
    sys.exit(1)
"
