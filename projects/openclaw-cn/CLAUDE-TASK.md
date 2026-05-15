# 任务：创建教程详情页（3篇）

## 目标
配置 Astro Content Collections，爬取3个教程来源，重写成 Markdown，
让用户点教程卡片后在站内查看完整内容，不跳转外部网站。

## 3篇教程（优先级顺序）

### 第1篇：OpenClaw 安装教程（入门）
- 参考来源：https://docs.openclaw.ai/zh-CN
- slug: `openclaw-install`
- 内容要求：完整安装流程（Node.js安装、npm install、onboard配置、gateway启动、连接Telegram/微信）
- 难度：入门 | 时长：10分钟

### 第2篇：Skills 技能安装（进阶）
- 参考来源：https://clawhub.ai + https://docs.openclaw.ai/zh-CN
- slug: `install-skills`
- 内容要求：什么是Skill、clawhub CLI安装、搜索技能、安装验证
- 难度：进阶 | 时长：20分钟

### 第3篇：Cron 定时任务配置（进阶）
- 参考来源：https://docs.openclaw.ai/zh-CN
- slug: `setup-cron`
- 内容要求：cron表达式基础、openclaw cron add命令、常用场景示例（每日日报、提醒）
- 难度：进阶 | 时长：30分钟

## 实现步骤

### Step 1: 配置 Content Collections
创建 `src/content.config.ts`：
```typescript
import { defineCollection, z } from 'astro:content';

const tutorials = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    duration: z.string(),
    difficulty: z.enum(['入门', '进阶', '实战']),
    outcome: z.string(),
    order: z.number().optional(),
  }),
});

export const collections = { tutorials };
```

### Step 2: 创建3个 Markdown 文件
路径：`src/content/tutorials/`
- `openclaw-install.md`
- `install-skills.md`
- `setup-cron.md`

每个文件格式：
```markdown
---
title: 标题
description: 一句话描述
duration: X 分钟
difficulty: 入门
outcome: 学完能做什么
order: 1
---

# 正文内容（重新用中文表达，不照搬原文）
## 前提条件
## 步骤一：xxx
## 步骤二：xxx
## 常见问题
```

内容要求：
- 用中文重新表达，不照搬原文
- 代码块保留真实命令
- 每篇至少600字，结构清晰
- 加上「常见问题」章节

### Step 3: 创建详情页模板
创建 `src/pages/tutorials/[slug].astro`：
- 从 Content Collections 读取内容
- 显示 title/difficulty/duration/outcome
- 渲染 Markdown 正文
- 左上角「← 返回教程列表」按钮
- 样式风格和现有页面一致（Tailwind）

### Step 4: 更新 site-content.ts 中的 href
把3篇教程对应的 href 改为内部路由：
- `href: '/tutorials/openclaw-install'`
- `href: '/tutorials/install-skills'`
- `href: '/tutorials/setup-cron'`

## 验收标准
- `npm run build` 零报错
- 访问 `/tutorials/openclaw-install` 有完整教程内容
- 教程列表页对应卡片点击能跳转到详情页
- 详情页有返回按钮

## 注意
- 不要改现有的 `src/pages/tutorials/index.astro`（列表页）
- 不要改其他教程的 href（只改这3篇）
- 内容集合配置文件是 `src/content.config.ts`（不是 src/content/config.ts）
