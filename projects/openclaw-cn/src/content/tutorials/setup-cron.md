---
title: 配置定时任务（Cron）
description: 让 AI 每天按时自动干活：发日报、提醒、整理信息，全自动不用你盯。
duration: 30 分钟
difficulty: 进阶
outcome: 建立一个每天早上自动推送 AI 日报的定时任务，真正实现「AI 自动上班」
order: 3
---

## 为什么要配置 Cron

没有 Cron，你的 AI 助手是「被动响应型」：你发消息，它才回复。

有了 Cron，它变成「主动执行型」：
- 每天早 6 点，自动整理行业动态发给你
- 每天晚 10 点，自动生成当日复盘
- 每周一上午，自动推送本周任务清单
- 有工具版本更新，第一时间通知你

这就是「AI 员工模式」的核心：**你定规则，AI 自动上班。**

---

## 基础概念：Cron 表达式

Cron 用 5 个数字描述「什么时候运行」：

```
分钟 小时 日期 月份 星期
 *    *    *    *    *
```

常用示例：
```
0 6 * * *        每天早上 6:00
30 9 * * 1-5     工作日早上 9:30
0 22 * * *       每天晚上 22:00
*/30 * * * *     每 30 分钟一次
0 9 * * 1        每周一早上 9:00
```

不懂没关系，下面都有现成的命令直接复制。

---

## 第一步：创建你的第一个定时任务

最实用的入门任务：**每天早上 7 点，让 AI 整理今日 AI 行业动态发给你**

```bash
openclaw cron add \
  --name "AI日报" \
  --cron "0 7 * * *" \
  --message "请搜索今天的 AI 行业重要动态，整理成 3-5 条简报，每条包含事件、影响和你的评价，发送给我"
```

创建成功后会显示任务 ID，记下来方便后续管理。

---

## 第二步：验证任务创建成功

```bash
openclaw cron list
```

输出示例：
```
ID          名称        计划          下次运行
ab12cd34    AI日报      0 7 * * *     明天 07:00
```

---

## 立刻试运行一次（不用等到预定时间）

```bash
openclaw cron run ab12cd34
```

把 `ab12cd34` 换成你的任务 ID。几秒内就会执行并发送消息，验证效果。

---

## 实用场景模板

直接复制，改一下名字就能用：

### 场景 1：每日早报（推荐新手先装这个）
```bash
openclaw cron add \
  --name "每日早报" \
  --cron "0 8 * * *" \
  --message "帮我整理：①今日 AI 行业重要动态 3 条；②今天适合写的公众号选题 2 个（带理由）；③一句今日激励。格式简洁，适合早上快速浏览"
```

### 场景 2：每日晚间复盘
```bash
openclaw cron add \
  --name "晚间复盘" \
  --cron "0 22 * * *" \
  --message "今天是 $(date '+%Y年%m月%d日')。请帮我做今日复盘：①我今天做了什么（根据我们的对话记录）；②做得好的 1 件事；③明天最重要的 1 件事。格式简短有力"
```

### 场景 3：工作日提醒
```bash
openclaw cron add \
  --name "工作日午间提醒" \
  --cron "0 12 * * 1-5" \
  --message "现在是工作日午休时间。提醒我：①今天下午要完成什么；②有没有快到期的事项；③推荐一件下午可以做的小事"
```

### 场景 4：工具更新监控
```bash
openclaw cron add \
  --name "工具更新监控" \
  --every "6h" \
  --message "检查 OpenClaw、Claude Code、Cursor 是否有新版本更新，如果有新版本，告诉我更新了什么内容"
```

---

## 管理定时任务

```bash
# 查看所有任务
openclaw cron list

# 立即运行某个任务
openclaw cron run <任务ID>

# 暂停任务（不删除）
openclaw cron disable <任务ID>

# 重新启用
openclaw cron enable <任务ID>

# 删除任务
openclaw cron rm <任务ID>

# 查看运行历史
openclaw cron runs <任务ID>
```

---

## 进阶：用 `--every` 代替 Cron 表达式

嫌 Cron 表达式麻烦？用 `--every` 更直觉：

```bash
# 每 30 分钟运行
openclaw cron add --name "心跳检查" --every "30m" --message "..."

# 每 2 小时运行
openclaw cron add --name "定期汇报" --every "2h" --message "..."

# 每天运行（等同于 0 0 * * *）
openclaw cron add --name "日结" --every "1d" --message "..."
```

---

## 常见问题

**Q：到时间了但没收到消息**

1. 检查 Gateway 是否在运行：`openclaw gateway status`
2. 检查任务是否 enabled：`openclaw cron list`
3. 手动运行看报不报错：`openclaw cron run <任务ID>`

**Q：想让任务在特定时区运行**

```bash
openclaw cron add \
  --name "早报" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --message "..."
```

**Q：任务运行了但 AI 回答质量差**

把 `--message` 里的提示词写得更具体，说清楚：要什么格式、多少字、什么风格。

**Q：怎么让 Cron 任务的内容更聪明**

在 `HEARTBEAT.md` 文件里写好定时任务的规则和上下文，AI 运行时会自动读取，输出质量会好很多。

---

## 下一步

- 多建几个定时任务，找到最适合你日程的节奏
- 试试 [多 Agent 协作](/tutorials)，让不同的 AI 助手分工合作
