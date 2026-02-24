# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

### Google Gemini API

- API Key: AIzaSyB3GsuTddVoxP5rGYce0F1285JjN3gHRYU
- 图片生成模型: gemini-2.0-flash-exp-image-generation（备用）
- 对话模型: gemini-2.5-flash / gemini-2.5-pro
- 用途: 备用对话模型（赠送额度已用完，3 Pro不可用）

### Notion

- API Key: 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
- 工作日志数据库ID: bf0b46f590d943089e758c61c0a7b0e7
- 推送脚本: `scripts/notion-push.sh "标题" "内容" "类型" "日期"`
- 类型：AI日报 / 日课 / 总结 / 工作记录
- 零零壹工作台页面: 303453f1-8074-8126-9d08-d9dbaf045e8c
- AI日报数据库: 303453f1-8074-8130-9096-c99bd40be6c0
- 日课十二条数据库: 303453f1-8074-819b-b376-ceb1c3e4b402
- 项目看板数据库: 303453f1-8074-8162-98be-d2bf7b2dcc03
- 知识库数据库: 303453f1-8074-81ab-ba5c-d4101f22c310
- 📋 待办任务数据库: 304453f1-8074-81f9-8c9f-d28cb59a7f68
- 📝 公众号文章库: 306453f1-8074-8107-b53a-e2dc0cece51b

---

Add whatever helps you do your job. This is your cheat sheet.

### 阿里云百炼（万相图片生成）
- API Key: sk-3e086717facd4d88a573260d127a15b0
- 模型: wan2.6-t2i（万相2.6，最新，支持同步调用）
- 接口: POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
- Header: Authorization: Bearer {key}, Content-Type: application/json
- 尺寸: 总像素1280²~1440²，宽高比1:4~4:1
- 有免费额度，超出按张计费

### 生财有术（知识星球）
- Group ID: 1824528822
- API: https://api.zsxq.com/v2/groups/1824528822/topics
- Cookie: zsxq_access_token=5902DC7A-7001-4CA7-B8B5-55BD1C00884B_B12E75520B50E663
- 精华帖: scope=digests
- 最新帖: scope=all
- Cookie过期: 2026年底

### 火山引擎（即梦AI图片生成）
- 子账号: openclaw001
- 登录: https://console.volcengine.com/auth/login/user/2101365095
- AK: AKLTZmQ0OWNkY2NhZTg2NDBhNWE3MmNhYmE5N2Y5OTViNjE
- SK(base64): WkRCaFlqWTRObVZtWXpGaE5EUTFOR0psWldNeU9EazVaV0ZtWkdaaU0yTQ==
- API: https://visual.volcengineapi.com, Action=CVProcess, Version=2022-08-31
- 可用req_key: high_aes_general_v20, high_aes
- 签名: 用 @volcengine/openapi npm包（Service + createJSONAPI）
- 免费额度: 200次
- 图片生成优先级: 即梦AI(火山引擎) > Gemini 2.0 Flash > Evolink(IP被封)

### Evolink（当前状态）
- 新key: sk-5ZFrdndazZvcDEDFjEU8gbxScFHXLYLzzKjr8WlZn7WjJG0u
- 旧key两个都403（IP被封，服务器43.159.48.54腾讯云）
- 图片正确接口: /v1/images/generations（异步任务模式）
- 待本地机器测试

### Grok API (xAI)
- API Key: xai-4YPImuiPnmESoKUHoKBbX7Mp1yX1IojfdBpSghrrA9ApexIkIaHgBZBFrhhnnsDFn5xQPPnEBQ9HObuG
- Endpoint: https://api.x.ai/v1/responses（tools版）/ https://api.x.ai/v1/chat/completions（普通版）
- 模型: grok-4-1-fast-reasoning（支持x_search工具）/ grok-3-mini（普通对话）
- x_search工具: 仅grok-4系列支持，需要Mihomo代理
- 定价: $0.20/$0.50 per million tokens（grok-4-1-fast）
- Credits: $5 预充，约可跑数月选题任务
- 脚本: scripts/grok-x-trends.sh

### Mihomo 代理（服务器本地）
- 安装路径: /usr/local/bin/mihomo
- 配置目录: /etc/mihomo/
- 订阅: WgetCloud（到期2026-03-07，需续费）
- 本地代理端口: 127.0.0.1:7890（混合HTTP/SOCKS5）
- systemd服务: mihomo.service（已enable，开机自启）
- 用途: 绕过Cloudflare/xAI对机房IP的封锁
- 续订链接: https://bava8u2znaj6bdzzjnfb.wgetcloud.online/link/1600b449-67c9-365f-916d-eedf0ab4dbe3

### 飞书
- App ID: cli_a908765086b85bc6
- App Secret: 4HZ5OiOueIU1PYCy59T48fpYvomTWELl
- OPENA知识库 space_id: 7603748469693484257 (读写权限✅)
- 10个飞书Skills已安装（im/bitable/doc-writer/drive/task/calendar/approval/contact/wiki/card）
