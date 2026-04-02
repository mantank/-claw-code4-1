# MEMORY.md - 索引

> 这是记忆索引文件，详细内容在各主题文件中。
> 需要找什么 → 看下面的索引 → 读对应文件。

## 关于旭
- 陈旭，称呼"旭"，叫他"老大"，Telegram @chenxu1988，GMT+8
- 非程序员出身，目标：AI超级个体（工具+内容+变现）
- 偏好：简单可用 > 复杂完美，落地优先，中文沟通
- 看不懂英文，回复全中文，模型专有名词可保留但加说明

## 主题文件索引

| 文件 | 内容 | 大小限制 |
|------|------|----------|
| `memory/content-ops.md` | 公众号/小红书/写作经验/品牌/图片 | ≤3KB |
| `memory/tools-config.md` | API Key/模型/服务器/代理/数据库ID | ≤3KB |
| `memory/agent-team.md` | 001/002配置/协作规则/Cron任务 | ≤2KB |
| `memory/business.md` | 变现/社群/用户增长/生财有术 | ≤2KB |
| `memory/industry-notes.md` | 行业动态/模型评测/技术趋势 | ≤2KB |
| `memory/milestones.md` | 重要事件时间线 | ≤2KB |
| `memory/YYYY-MM-DD.md` | 当日工作日志（保留最近7天） | ≤3KB |

## 当前重点（2026-04-02更新）
- **变现优先**：赚钱>一切，先帮朋友跑通真实场景→拿案例→收费（3/15旭决策）
- 旭财务压力大（月入8K，月还7K+），AI工具费是负担，必须尽快变现
- 公众号流水线：每日14:30+19:00两批cron，草稿箱常备8+篇
- 002产能稳定：每日可产8篇草稿，需安排发布节奏
- 004案例库：425个案例/551页，已开辟新素材源
- **OpenClaw 2026.4.1 运行中**（4/2升级，exec审批问题需手动配置allow-always解决）
- 001模型：Claude Max $100/月（Opus 4.6），002/003：Gemini 3.1 Flash Lite
- Gemini API $370额度至2026-05-10
- **新装技能（6个）**：dream-memory/memory-extractor/verification-gate/swarm-coordinator/structured-context-compressor/kairos-lite（cc-harness-skills，2026-04-02安装）

## 待解决（2026-04-02）
- Brave Search API Token失效（421）→ 搜索功能全挂
- 生财有术Cookie失效（401）→ 精华帖推送中断
- exec审批需配置 `exec.approvalPolicy allow-always` 才彻底解决

## 规则
- 日志超过7天 → 有价值的内容归入主题文件，日志归档到 `memory/archive/`
- 主题文件超过3KB → 清理过期内容
- 禁止在MEMORY.md堆积详细信息，保持索引功能
