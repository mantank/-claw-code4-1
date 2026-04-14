#!/bin/bash
# 每日AI热点简报 - 针对「深夜开发者LND」账号方向
# 数据源：X实时热词 + AI产品动态 + 竞品文章

GROK_API="https://api.x.ai/v1/chat/completions"
GROK_KEY="xai-4YPImuiPnmESoKUHoKBbX7Mp1yX1IojfdBpSghrrA9ApexIkIaHgBZBFrhhnnsDFn5xQPPnEBQ9HObuG"
PROXY="http://127.0.0.1:7890"
BRAVE_KEY="BSA61abs6MtSz8nRiSdAGqiKxuI1zwn"

echo "=== BRIEFING_START ==="
echo "DATE: $(TZ='Asia/Shanghai' date '+%Y-%m-%d %H:%M')"

# ===== 一、AI产品/工具最新动态（web_search，最可靠） =====
echo ""
echo "## 🚀 AI产品动态（最近24小时）"

curl -s "https://api.search.brave.com/res/v1/web/search" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "X-Subscription-Token: $BRAVE_KEY" \
  -G \
  --data-urlencode "q=AI工具 新发布 2026 OpenClaw DeepSeek Claude Cursor" \
  --data-urlencode "count=5" \
  --data-urlencode "freshness=pd" \
  --data-urlencode "search_lang=zh-hans" 2>/dev/null | gzip -dc | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    results = d.get('web',{}).get('results',[])
    for i,r in enumerate(results[:5]):
        title = r.get('title','?')[:50]
        desc = r.get('description','')[:80]
        print(f'{i+1}. {title}')
        if desc: print(f'   {desc}')
except: print('（获取失败）')
" 2>/dev/null

# ===== 二、OpenClaw/独立开发者圈动态 =====
echo ""
echo "## 🦞 OpenClaw & 独立开发者圈"

curl -s "https://api.search.brave.com/res/v1/web/search" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "X-Subscription-Token: $BRAVE_KEY" \
  -G \
  --data-urlencode "q=OpenClaw 小龙虾 AI Agent 独立开发 副业" \
  --data-urlencode "count=5" \
  --data-urlencode "freshness=pd" \
  --data-urlencode "search_lang=zh-hans" 2>/dev/null | gzip -dc | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    results = d.get('web',{}).get('results',[])
    for i,r in enumerate(results[:4]):
        title = r.get('title','?')[:50]
        url = r.get('url','')
        # 过滤官网
        if 'openclaw' not in url.lower() or 'docs' not in url.lower():
            print(f'{i+1}. {title}')
except: print('（获取失败）')
" 2>/dev/null

# ===== 三、竞品账号文章（搜索最新内容） =====
echo ""
echo "## 👀 竞品文章动态"

curl -s "https://api.search.brave.com/res/v1/web/search" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "X-Subscription-Token: $BRAVE_KEY" \
  -G \
  --data-urlencode "q=数字生命卡兹克 OR 宝玉xp OR 归藏 AI OpenClaw 公众号" \
  --data-urlencode "count=5" \
  --data-urlencode "freshness=pw" 2>/dev/null | gzip -dc | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    results = d.get('web',{}).get('results',[])
    for i,r in enumerate(results[:4]):
        title = r.get('title','?')[:50]
        source = r.get('profile',{}).get('name','') or r.get('url','')[:30]
        print(f'{i+1}. {title}  [{source}]')
except: print('（获取失败）')
" 2>/dev/null

# ===== 四、X上AI圈讨论（Grok，走代理） =====
echo ""
echo "## 🐦 X上AI圈热点"

RESP=$(curl -s -x "$PROXY" --max-time 20 \
  -X POST "$GROK_API" \
  -H "Authorization: Bearer $GROK_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-3-mini",
    "messages": [{"role":"user","content":"今天X上AI开发者圈（OpenClaw/Claude/Cursor/独立开发者）在热议什么？给3个话题，每个一句话中文总结，不超过20字。格式：1. 话题 — 说明"}],
    "max_tokens": 200
  }' 2>/dev/null)

echo "$RESP" | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    content=d.get('choices',[{}])[0].get('message',{}).get('content','（代理不可用，跳过）')
    print(content)
except: print('（跳过）')
" 2>/dev/null

echo ""
echo "=== BRIEFING_END ==="
