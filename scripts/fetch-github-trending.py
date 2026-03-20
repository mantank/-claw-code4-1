#!/usr/bin/env python3
"""AI新闻源抓取：GitHub Trending + Hacker News"""
import urllib.request
import json
import re
import sys
import time

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0'

def fetch_github_trending(lang='Python', days=7, limit=8):
    """用GitHub API搜近期热门仓库"""
    from datetime import datetime, timedelta
    date_from = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    q = f'language:{lang}+created:>{date_from}'
    url = f'https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page={limit}'
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    resp = urllib.request.urlopen(req, timeout=15)
    data = json.loads(resp.read())
    results = []
    for item in data.get('items', [])[:limit]:
        results.append({
            'name': f"{item['owner']['login']}/{item['name']}",
            'stars': f"{item['stargazers_count']:,}",
            'desc': (item.get('description') or '')[:100],
            'lang': item.get('language', ''),
            'url': item['html_url']
        })
    return results

def fetch_hackernews(limit=8, keywords=['AI', 'LLM', 'OpenAI', 'GitHub', 'coding', 'agent', 'model', 'Python']):
    """抓HN热搜，过滤AI相关"""
    req = urllib.request.Request(
        'https://hacker-news.firebaseio.com/v0/topstories.json',
        headers={'User-Agent': UA}
    )
    resp = urllib.request.urlopen(req, timeout=10)
    ids = json.loads(resp.read())[:30]
    results = []
    for sid in ids:
        item_req = urllib.request.Request(
            f'https://hacker-news.firebaseio.com/v0/item/{sid}.json',
            headers={'User-Agent': UA}
        )
        try:
            item_resp = urllib.request.urlopen(item_req, timeout=5)
            item = json.loads(item_resp.read())
            if item.get('type') == 'story' and item.get('url'):
                title = item.get('title', '')
                # 过滤关键词
                if any(k.lower() in title.lower() for k in keywords):
                    results.append({
                        'title': title,
                        'score': item.get('score', 0),
                        'url': item.get('url', ''),
                        'hn_url': f'https://news.ycombinator.com/item?id={sid}'
                    })
                    if len(results) >= limit:
                        break
        except:
            continue
    return results

if __name__ == '__main__':
    source = sys.argv[1] if len(sys.argv) > 1 else 'github'
    
    if source == 'github':
        results = fetch_github_trending('Python', days=7, limit=8)
        print(f'=== GitHub Python热门项目（7天内）===')
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['name']} ⭐{r['stars']} | {r['lang'] or '?'}")
            if r['desc']: print(f"   {r['desc']}")
            print(f"   {r['url']}")
    
    elif source == 'hn':
        results = fetch_hackernews(limit=8)
        print(f'=== Hacker News AI相关热搜 ===')
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['title']} ({r['score']} pts)")
            print(f"   {r['url'][:80]}")
