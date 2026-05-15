---
title: 如何安装 Skills 技能
description: 从 ClawHub 社区搜索技能、一键安装、验证生效，手把手搞定。
duration: 20 分钟
difficulty: 进阶
outcome: 成功安装 3 个实用技能，让助手能搜索网络、处理文件、发送消息
order: 2
---

## 什么是 Skill（技能）

Skills 是给 OpenClaw 添加新能力的插件。

没有 Skills，你的助手只能聊天。有了 Skills，它可以：
- 搜索最新资讯
- 读取和修改文件
- 发消息给微信/飞书
- 定时执行任务
- ...几乎任何你能想到的事

技能分为两种：
- **官方技能** — OpenClaw 团队维护，质量稳定
- **社区技能** — 开发者贡献，数量更多，涵盖各种场景

---

## 第一步：安装 ClawHub CLI

ClawHub 是 OpenClaw 的技能市场，通过它来搜索和安装技能：

```bash
npm install -g clawhub
```

验证：
```bash
clawhub --version
```

---

## 第二步：搜索你需要的技能

```bash
# 按关键词搜索
clawhub search "web search"

# 按分类浏览
clawhub browse --category content

# 查看热门技能
clawhub top
```

搜索结果会显示技能名称、描述、安装量和评分。

---

## 第三步：安装技能

找到想要的技能后，复制名称安装：

```bash
# 安装单个技能
clawhub install weather

# 安装多个技能
clawhub install weather web-search feishu-im
```

安装完会自动重启 Gateway，技能立即生效。

---

## 推荐新手先装这 3 个

### 1. `weather` — 天气查询
```bash
clawhub install weather
```
装完发送「今天上海天气」，助手会直接回复实时天气数据。

### 2. `web-search` — 网络搜索
```bash
clawhub install web-search
```
让助手能搜索最新资讯，不再局限于训练数据的知识截止日期。

### 3. `feishu-im` — 飞书消息
```bash
clawhub install feishu-im
```
让助手能发飞书消息，适合在企业场景里自动通知团队。

---

## 第四步：验证技能是否生效

```bash
openclaw skills list
```

会列出所有已安装的技能和状态：
```
✅ weather (v1.2.0) — active
✅ web-search (v2.0.1) — active
✅ feishu-im (v1.5.0) — active
```

直接测试：去 Telegram/微信找你的 Bot，发一条「帮我查一下北京今天的天气」，看看有没有正确回复。

---

## 管理已安装的技能

```bash
# 查看所有技能
openclaw skills list

# 更新某个技能
clawhub update weather

# 更新全部技能
clawhub update --all

# 卸载技能
clawhub uninstall weather

# 禁用技能（不卸载）
openclaw skills disable weather
```

---

## 常见问题

**Q：安装报错 `Network timeout`**

网络问题，加上代理或者多试几次：
```bash
clawhub install weather --retry 3
```

**Q：技能安装成功但不生效**

重启 Gateway：
```bash
openclaw gateway restart
```

**Q：技能装完 Gateway 没有自动重启**

手动重启：
```bash
openclaw gateway restart
openclaw skills reload
```

**Q：怎么找到适合自己业务的技能**

去 [clawhub.ai](https://clawhub.ai) 按分类浏览，有内容创作、电商、开发工具、办公自动化等分类，找到感兴趣的复制名称安装就行。

---

## 下一步

- [配置定时任务](/tutorials/setup-cron) — 让技能按计划自动运行
