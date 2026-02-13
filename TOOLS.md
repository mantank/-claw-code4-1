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

### 生财有术（知识星球）
- Group ID: 1824528822
- API: https://api.zsxq.com/v2/groups/1824528822/topics
- Cookie: zsxq_access_token=5902DC7A-7001-4CA7-B8B5-55BD1C00884B_B12E75520B50E663
- 精华帖: scope=digests
- 最新帖: scope=all
- Cookie过期: 2026年底

### 飞书
- App ID: cli_a908765086b85bc6
- App Secret: 4HZ5OiOueIU1PYCy59T48fpYvomTWELl
- OPENA知识库 space_id: 7603748469693484257 (读写权限✅)
- 10个飞书Skills已安装（im/bitable/doc-writer/drive/task/calendar/approval/contact/wiki/card）
