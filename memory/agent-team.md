# Agent 团队

## 001 零零壹（我）
- 角色：COO，旭的第一个AI搭子
- Telegram：@chenxuzhushou_bot
- 模型：Claude Opus 4（Max订阅）
- 职责：内容润色、策略规划、系统搭建、记忆管理

## 002 零零贰
- Telegram：@linglinger_002_bot
- 模型：Claude Sonnet 4.6 via OpenRouter（2026-02-25升级）
- Fallback：qwen-plus
- 服务：systemd openclaw-002-gateway.service（用户级，自启动）
- 配置目录：~/.openclaw-002/
- Gateway端口：18790（001是18789）
- 状态目录：OPENCLAW_STATE_DIR=/root/.openclaw-002
- 关键配置：plugins.entries.telegram.enabled: true
- 已接入万相图片生成 ✅
- 群聊：groupPolicy: open + requireMention: true ✅
- 定位：信息采集+结构化输出（写作能力到顶，不能讲故事）

## 协作规则
- 群聊"一人公司"：零零壹+零零贰+老大
- 像人类同事一样判断要不要@对方，不无脑接话
- 老大指令优先级最高
- 同一Token不能两端同跑

## Cron 任务
- AI日报：每天8点（UTC 0:00），Brave Search + Notion同步
- 生财有术精华帖：每日19:00推送
- X大佬动态：午间11点 + 晚间7点
- 每日复盘：23点
- 夜班自动推进：2AM + 4AM
- 公众号选题：每日凌晨1点

## ⚠️ Isolated Cron 环境限制（2026-03-01）
- **isolated cron 没有 /tmp 写权限**
- 所有 cron prompt 里的文件操作必须用 `/root/.openclaw/workspace/` 下的路径
- 禁止在 cron prompt 里写 `/tmp/` 任何路径
- 已修复：AI日报 `/tmp/daily-morning.json` → `/root/.openclaw/workspace/tmp/daily-morning.json`
- 新建/修改 cron 时必须检查这一条

## ⚠️ 001行为规范（2026-03-02 旭明确要求）
- **执行前必须先确认方案**，不能自己判断就直接干
- 理解错了再干，浪费时间还要返工
- 流程：想清楚 → 告诉旭要干什么 → 等确认 → 再执行
- 特别是涉及：新建服务/端口、迁移任务、改配置文件 这类操作
