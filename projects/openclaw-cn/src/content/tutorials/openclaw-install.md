---
title: 如何安装 OpenClaw
description: 手把手带你完成安装、配置和第一次连接，所有常见报错都有解法。
duration: 10 分钟
difficulty: 入门
outcome: 在本地跑通 OpenClaw，连上 Telegram 或微信，收到第一条 AI 回复
order: 1
---

## 你需要准备什么

安装之前，确认你的电脑上有这两样东西：

- **Node.js 18 或更高版本** — 没有的话去 [nodejs.org](https://nodejs.org) 下载 LTS 版本
- **Git** — Windows 用户去 [git-scm.com](https://git-scm.com) 下载，Mac 用户终端输入 `git --version` 确认有没有

验证 Node.js 安装：
```bash
node --version
# 应该显示 v18.x.x 或更高
```

---

## 第一步：安装 OpenClaw

打开终端（Mac 用 Terminal，Windows 用 PowerShell），执行：

```bash
npm install -g openclaw
```

装完验证一下：
```bash
openclaw --version
```

看到版本号就说明装成功了。

---

## 第二步：初始化配置

```bash
openclaw onboard
```

这个命令会引导你完成基础设置，包括：
- 选择你要连接的聊天渠道（Telegram / 微信 / Discord 等）
- 配置 AI 模型（默认用 Claude，也可以用 GPT 或 DeepSeek）
- 安装系统服务（让 OpenClaw 开机自启）

按照提示一步步来，大概 3 分钟完成。

---

## 第三步：启动 Gateway 网关

```bash
openclaw gateway start
```

看到这样的输出说明启动成功：
```
🦞 Gateway started on port 18789
✅ Connected to Telegram
```

---

## 第四步：连接 Telegram（最简单的渠道）

1. 在 Telegram 搜索 `@BotFather`
2. 发送 `/newbot`，按提示创建一个 Bot，拿到 Token（一串数字+字母）
3. 执行：
```bash
openclaw channel add telegram --token YOUR_BOT_TOKEN
```
4. 去 Telegram 找你的 Bot，发一条消息，收到回复就成功了 🎉

---

## 第五步：验证一切正常

```bash
openclaw status
```

正常状态应该显示：
- Gateway: ✅ Running
- Channels: ✅ Telegram connected
- Agent: ✅ Active

---

## 常见问题

**Q：安装时报 `EACCES permission denied`**

说明权限不够，换这个命令：
```bash
sudo npm install -g openclaw
```
或者用 nvm 管理 Node.js 就不需要 sudo。

**Q：`openclaw gateway start` 之后没有响应**

可能是端口被占用，试试：
```bash
openclaw gateway start --port 18790
```

**Q：Bot 没有回复我的消息**

1. 先检查 `openclaw status` 输出
2. 确认 Token 没有多余空格
3. 重启 Gateway：`openclaw gateway restart`

**Q：Windows 上运行报错**

确保用 **PowerShell 管理员模式** 运行，或者用 WSL2 + Ubuntu 环境。

---

## 下一步

安装完成后，推荐接着看：

- [如何安装技能](/tutorials/install-skills) — 给你的助手加更多能力
- [配置定时任务](/tutorials/setup-cron) — 让 AI 每天自动干活
