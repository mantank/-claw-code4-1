# PROJECT_STATUS.md — 当前项目状态

> 所有Agent共享。每次重要进展后更新。
> 最后更新：2026-03-04 23:22（001心跳更新）

---

## 🎯 本月战略方向（2026年3月）

### 两条变现路径
- **路径A（长期）**：公众号/小红书 → 私信引流 → OpenClaw Agent World网站 → 付费社群
- **路径B（短期）**：闲鱼 ¥99 远程部署 → 赚第一笔钱 + 积累案例

### 网站规划
- 名称：OpenClaw Agent World（暂定）
- 参考：https://www.waytoagi.com/zh（结构布局）+ sanwan.ai（技能包一键复制）
- 技术方案：v0搭框架 → Claude Code + Codex CLI 填充优化
- 核心板块：每日精选 + 技能商店 + 行业套装 + 用户案例 + 教程

---

## 🏃 进行中

### 公众号「深夜开发者LND」
- 当前粉丝：~30（估算）
- 发布节奏：每周2-3篇（周二/周四/周六）
- 已发布：「生产力恐慌」(2026-03-04，lapis主题，9张白板配图)
- 上篇数据：DeepSeek V4文章 公众号1600+阅读，小红书1.5万浏览
- 待发草稿：article-12~15（4篇）
- 配图规则：仅用 nanobanana-ppt-skills，其他图片技能已全部删除

### 小红书
- 计划：每天1篇短内容（图片为主）
- xiaohongshu-mcp 已安装
- 风险：反自动化检测强，可能需要半自动

### 闲鱼变现（明天启动）
- [ ] 冷启动：发3-5个低价商品（¥0.1会员/Key码），跑成交积累信誉
- [ ] 正式商品：¥99远程部署 + ¥9.9-29.9教程

---

## 🤖 AI团队现状

| 编号 | 角色 | 模型 | 状态 | 当前任务 |
|------|------|------|------|---------|
| 001 | 总指挥/日常助理 | Claude Opus 4.6 | ✅活跃 | 协调+指挥Claude Code开发+配图 |
| 002 | 内容官 | Claude Sonnet 4.6 (OpenRouter) | ⚠️待激活 | 需要跑通完整文章流水线 |
| 003 | 情报官 | Gemini 3 Flash (OpenRouter) | ✅完工 | OpenClaw生态玩法情报库8分类全部完成（2026-03-05 04:09） |

### 003模型问题
- Antigravity反代已配置（frp隧道：Mac:8045 → 服务器:38045）
- 但Google账号要求验证（403 PERMISSION_DENIED），实际无法调用Gemini
- 003实际在用 MiniMax M2.5 → Claude Sonnet fallback
- 待旭去Antigravity重新验证Google账号

### 编程能力升级（刘小排模式）
- Claude Code CLI ✅ 已安装已登录（v2.1.68）
- Codex CLI ✅ 已安装（v0.107.0），待登录
- Gemini CLI ❌ 未安装
- 模式：001用tmux指挥多Agent协作开发

---

## 🔧 基础设施

### Cron自动化体系

| 任务 | ID | 时间 | 状态 |
|------|-----|------|------|
| AI日报 | - | 8:00 | ✅正常 |
| 每日热点简报 | ef870079 | 8:30 | ✅正常 |
| 公众号选题推送（旧版）| aa62b1e0 | 9:00 | ✅正常 |
| 选题情报-新版 | 0d8c3469 | 9:30 | ✅新建，跑一周对比 |
| 生财有术推送 | bcbc6376 | 19:00 | ✅正常 |
| X大佬动态-午间 | aa8e717f | 11:00 | ⚠️超时error |
| X大佬动态-晚间 | bf1bfd8f | 19:00 | ⚠️超时error |

### 搜索工具（Agent Reach，2026-03-04）
- ✅ Twitter/X（xreach CLI + Cookie）
- ✅ 任意网页（Jina Reader）
- ✅ 全网语义搜索（Exa）
- ✅ 小红书（mcporter）
- ✅ YouTube字幕（yt-dlp）
- ✅ RSS订阅
- ⬜ Reddit（需代理）
- ⬜ B站（服务器被封）

### 服务器
- 时区：Asia/Shanghai（CST +0800）
- frps服务：端口37890（systemd，开机自启）
- 腾讯云防火墙已开放：37890、38045

---

## ✅ 最近完成（2026-03-04）

- 发布「生产力恐慌」文章（公众号草稿箱）
- Agent Reach 安装（7/12渠道可用）
- Twitter/X Cookie配置（xreach可用）
- 003搜索工具升级（xreach替代Grok API）
- Antigravity + frp隧道配置（Mac↔服务器）
- 飞书知识库上传（X/OpenClaw 7天情报报告，301 blocks）
- 新建「选题情报-新版-9点30」cron任务
- 服务器时区改为 Asia/Shanghai
- HEARTBEAT.md修正（禁止主动推消息+强制获取北京时间）
- 删除过期技能（nano-banana-ppt/sketch-illustration/weather）
- 003生态情报库完成（10分类，298条记录）

---

## 📅 明天待办（2026-03-05）

详见 `memory/2026-03-05-todo.md`

**必做：**
1. 闲鱼冷启动（低价商品出成交）
2. 闲鱼正式商品发布（¥99部署+教程）

**待旭确认：**
- 网站名字
- Codex CLI登录
- Antigravity Google账号验证

---

## 🔴 当前最大卡点

1. **002从未跑过完整流水线**：选题→初稿→图片→发布，本周必须验证
2. **Antigravity/Gemini 403**：003无法用Gemini，需要旭重新验证Google账号
3. **X大佬动态cron超时**：待排查
