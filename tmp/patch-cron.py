import json, sys

with open('/root/.openclaw/cron/jobs.json') as f:
    data = json.load(f)

jobs = data if isinstance(data, list) else data.get('jobs', [])

new_message = """生成今日AI日报并用 message 工具发送到 Telegram（target=8526440826，channel=telegram）。

## 全局搜索规则
- 所有搜索只用 web_search（Brave Search），freshness="pd"（过去24小时）
- 每个板块用 2-3 组不同关键词分别搜索
- 只收录24小时以内的内容，时间对不上的跳过
- 每板块不超过5条，不够不凑，超出只留最有价值的
- 禁止编造链接

## 每条信息输出格式（所有板块统一）
**【标题/名称】**
🔸 事件：发生了什么（一句话说清楚）
🚀 行业价值：跟从业者有什么关系，该怎么应对
🔗 来源：[媒体/平台名](链接)

---

## 板块一：模型速报 🚀
搜索关键词组（freshness=pd）：
1. "OpenAI model release 2026"
2. "Anthropic Claude release 2026"
3. "Google Gemini model update 2026"
4. "DeepSeek OR Grok OR Meta Llama model release"
5. "AI model launch site:x.com"

---

## 板块二：AI工具&应用 🛠️
搜索关键词组（freshness=pd）：
1. "new AI tool launch site:producthunt.com"
2. "new AI app release site:techcrunch.com"
3. "AI feature update site:venturebeat.com"

---

## 板块三：GitHub精选 🐙
搜索关键词组（freshness=pd）：
1. "AI agent framework release site:github.com"
2. "new MCP server release site:github.com"
3. "Claude OR OpenAI agent tool release site:github.com"
格式额外加：仓库名（⭐星数）

---

## 板块四：OpenClaw动态 🦾
从以下来源抓取最新资讯和技能应用场景：
官方来源（必抓，逐一 web_fetch）：
- web_fetch: https://docs.openclaw.ai/zh-CN
- web_fetch: https://clawhub.ai

搜索关键词组（freshness=pd）：
1. "openclaw new feature OR release"
2. "openclaw skill site:clawhub.ai OR site:github.com"
3. "openclaw site:x.com"
4. "site:claw123.ai openclaw"

技能参考来源：
- https://clawhub.ai（官方技能站）
- https://github.com/VoltAgent/awesome-openclaw-skills
- https://openclawdirectory.co.uk

---

## 板块五：博主精读 👀
搜索关键词组（freshness=pd）：
1. "karpathy site:x.com"
2. "sama site:x.com"
3. "宝玉 AI site:x.com"
4. "emollick site:x.com"
只写有实质观点的，没有新内容直接跳过。

---

## 板块六：今日选题 💡
基于以上今日实际内容，给出1-2个适合"深夜开发者LND"公众号的选题。
格式：
选题一：《标题》
切入角度：一句话说明

---

## 发送格式（完整模板）
用 message 工具发送，内容如下：

**📊 AI日报 | {今天日期}**

━━━━━━━━━━━━━━━━
**🚀 模型速报**

**【模型名】**
🔸 事件：xxx
🚀 行业价值：xxx
🔗 来源：[媒体名](链接)

━━━━━━━━━━━━━━━━
**🛠️ AI工具&应用**

**【工具名】**
🔸 事件：xxx
🚀 行业价值：xxx
🔗 来源：[媒体名](链接)

━━━━━━━━━━━━━━━━
**🐙 GitHub精选**

**仓库名（⭐星数）**
🔸 事件：xxx
🚀 行业价值：xxx
🔗 来源：[GitHub](链接)

━━━━━━━━━━━━━━━━
**🦾 OpenClaw动态**

**【技能/功能名】**
🔸 事件：xxx
🚀 行业价值：xxx
🔗 来源：[来源名](链接)

━━━━━━━━━━━━━━━━
**👀 博主精读**

**@账号**
🔸 观点：xxx
🔗 来源：[原文](链接)

━━━━━━━━━━━━━━━━
**💡 今日选题**

选题一：《标题》
切入角度：xxx

选题二：《标题》
切入角度：xxx"""

for job in jobs:
    if job.get('id') == '59db55de-0c5c-4118-8f80-74b902d61914':
        job['payload']['message'] = new_message
        job['payload']['timeoutSeconds'] = 300
        print('已更新:', job['name'])

with open('/root/.openclaw/cron/jobs.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('写入完成')
