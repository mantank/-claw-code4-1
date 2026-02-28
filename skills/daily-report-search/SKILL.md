# Skill: 日报搜索策略

## 触发场景
生成「AI日报」「今日热点」「技术日报」「每日速报」时激活。

---

## 信息源优先级

### 一线信息源（每日必查）
| 来源 | 工具 | 优先级 |
|------|------|--------|
| Grok x_search（X平台热帖） | Grok API + x_search | ⭐⭐⭐ |
| 生财有术精华帖 | zsxq API（见TOOLS.md） | ⭐⭐⭐ |
| Hacker News Top | web_fetch hn.algolia.com | ⭐⭐ |
| ProductHunt今日榜 | web_fetch producthunt.com | ⭐⭐ |
| Reddit r/artificial | web_search | ⭐ |

### 搜索关键词模板
```
AI工具: "AI tool" OR "new model" OR "launched today" site:twitter.com
国内动态: "大模型" OR "AI应用" 发布 今日
技术突破: "breakthrough" OR "sota" site:arxiv.org
```

---

## 执行步骤

### Step 1 — 多源并行抓取
同时调用以下（不要串行等待）：
1. Grok API x_search → AI/科技热词
2. 生财有术API → 精华帖（scope=digests）
3. web_fetch HN首页

### Step 2 — 去重 & 筛选
- 去掉重复消息
- 优先选：有数据、有产品、有实操价值的内容
- 排除：纯观点/鸡汤/广告

### Step 3 — 结构化输出
```markdown
## 今日 AI 日报 — YYYY-MM-DD

### 🔥 最热
1. [标题] — 一句话摘要（来源）

### 🛠️ 工具 & 产品
1. ...

### 💡 值得关注
1. ...
```

### Step 4 — 写入Notion（可选）
```bash
scripts/notion-push.sh "AI日报 YYYY-MM-DD" "内容" "AI日报" "YYYY-MM-DD"
```

---

## Grok API 调用示例
```bash
curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer xai-4YPImuiPnmESoKUHoKBbX7Mp1yX1IojfdBpSghrrA9ApexIkIaHgBZBFrhhnnsDFn5xQPPnEBQ9HObuG" \
  -H "Content-Type: application/json" \
  -d '{"model":"grok-3-mini","messages":[{"role":"user","content":"今天AI领域最热的5个话题，每条20字以内"}]}'
```

## 注意
- Grok x_search 需要 Mihomo 代理（127.0.0.1:7890）
- 生财有术Cookie到期：2026年底，过期需更新
