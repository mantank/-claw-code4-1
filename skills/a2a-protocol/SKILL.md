# A2A 协作协议 — 小龙虾互联指南

> 研究来源：OpenClaw 官方文档 + opencrew 开源项目（AlexAnys/opencrew）
> 整理时间：2026-03-01
> 适用场景：001（总指挥）↔ 002（内容官）协同工作

---

## 一、核心原理

### 为什么需要 A2A？

一个 Agent 承担所有任务会导致：
- 上下文无限膨胀，越用越迟钝
- 踩过的坑下次还踩（经验没有沉淀）
- 不同领域任务相互干扰

**A2A 的本质：让 Agent 像人一样协作——001 是总指挥，002 是执行员，各管各的上下文，按需传递任务。**

### 关键限制（必须知道）

> ⚠️ **所有 Agent 共用同一个 Bot 身份**。Bot 自己发的消息不会触发对方 Agent 自动运行（OpenClaw 默认忽略 bot-authored inbound 避免死循环）。

因此：**跨 Agent 触发必须通过 `sessions_send` 工具**，不能只是"发一条消息"。

---

## ⚡ 快速参考（最常用）

**001→002 发任务，最简单的方式：**
```python
message.send(
    channel="telegram",
    target="-5165950284",  # 一人公司群组
    message="@linglinger_002_bot [任务内容]"
)
```
002 有 requireMention:true，必须@才触发。

**002 关键配置（不要再失忆）：**
- 状态目录：`/root/.openclaw-002/`
- Gateway 端口：18790
- systemd：`openclaw-002-gateway.service`（用户级）
- Telegram Bot：@linglinger_002_bot
- 群组 ID：-5165950284

**⚠️ sessions_send 不能用于跨 gateway**：visibility=tree 限制，只能在同一 gateway 内用。

---

## 二、我们当前的架构现状

```
服务器上：
├── main（001 零零壹）← 你在这里
│   └── workspace: ~/.openclaw/workspace
│   └── channel: Telegram @chenxu1988
└── default（002 零零贰）← 需要配置
    └── workspace: 待配置
    └── channel: 待绑定
```

**当前问题**：`openclaw agents list` 只显示一个 `main` agent。002 还没有在本机作为独立 Agent 注册，需要配置后才能实现真正的 A2A 协同。

---

## 三、配置步骤（001 执行）

### Step 1：确认 002 的 workspace 位置

```bash
# 002 的 workspace 应该是一个独立目录，不和 001 共享
ls ~/.openclaw/agents/
# 如果只有 main，需要添加 002
```

### Step 2：添加 002 为独立 Agent

```bash
# 添加 002 agent，指定 workspace（旭需要告知 002 的 workspace 路径）
openclaw agents add 002 --workspace <002的workspace路径>

# 示例（假设 002 在 ~/clawd）：
openclaw agents add 002 --workspace ~/clawd
```

### Step 3：绑定路由

```bash
# 把 Telegram 群组绑定到对应 Agent
# 或者通过 channel/account/peer 路由
openclaw agents bind --agent 002 --channel telegram --account <002的botToken账号>
```

### Step 4：验证 Agent 注册成功

```bash
openclaw agents list
# 应该看到 main 和 002 两个 agent
```

---

## 四、A2A 触发协议（配置成功后使用）

### 标准触发流程（两步）

**Step 1：发可见锚点消息**（让旭知道任务在跑）

```python
# 001 在 Telegram 发一条任务说明
message.send(
    target="旭的Telegram",
    message="📤 A2A | 001→002 | 内容任务：...\n已派单给002，预计完成时间：xx分钟"
)
```

**Step 2：用 `sessions_send` 真正触发 002**

```python
# 001 用 sessions_send 把任务发给 002
sessions_send(
    sessionKey="agent:002:main",  # 002 的 session key
    message="""
# 任务派单 | 来自 001

## 目标（Objective）
写一篇公众号文章初稿：[选题名称]

## 完成标准（DoD）
- 1500-2000 字
- 符合深夜开发者 LND 风格（参考 SOUL.md 和写作风格指南）
- 包含：开头钩子 + 核心内容 3 点 + 行动结尾
- 产出路径：articles/[文件名].md

## 输入资料（Inputs）
- 选题参考：[链接或描述]
- 今日热点背景：[背景信息]
- 风格指南：~/.openclaw/workspace/templates/writing-style-guide.md

## 约束（Constraints）
- 不要调用 message 工具（不要直接发给旭）
- 完成后把文件路径汇报给 001

## 输出格式
完成后回复：文章已完成，路径：[路径]，字数：[字数]
""",
    timeoutSeconds=300
)
```

---

## 五、任务分工矩阵（我们的版本）

| 触发方 | 接收方 | 典型任务 |
|--------|--------|---------|
| 旭 | 001 | 定方向、定目标、审稿 |
| 001 | 002 | 写文章初稿、生成选题、做研究 |
| 002 | 001 | 汇报完成、请求确认 |
| 001 | 旭 | 阶段性汇报、需要决策时 |

**禁止**：002 直接给旭推未审核的文章；001 绕过旭做重大决策。

---

## 六、任务包标准格式（每次 A2A 都用这个）

```markdown
# 任务派单 TID:[YYYYMMDD-HHMM]-[短标识]
来自：[发单方]
发给：[接单方]

## 目标（Objective）
[一句话描述要完成什么]

## 完成标准（DoD）
- [可验证的条件1]
- [可验证的条件2]

## 输入资料（Inputs）
- [文件路径 / 链接 / 背景信息]

## 约束（Constraints）
- [不能做什么]
- [边界条件]

## 输出格式
[期望的产出是什么，放在哪里]
```

---

## 七、自主等级规则（L0-L3）

| 等级 | 含义 | 001 的例子 | 002 的例子 |
|------|------|-----------|-----------|
| L1 | 可逆，直接做 | 搜索资料、写研究笔记 | 写文章草稿 |
| L2 | 有影响但可回滚，做完汇报 | 更新 Cron 配置 | 修改已有文章 |
| L3 | 不可逆，必须旭确认 | 发布文章、对外发消息 | 任何发布操作 |

---

## 八、知识沉淀三层机制

```
Layer 0：原始对话（审计用）
     ↓ 001/002 自动提炼
Layer 1：任务 Closeout（10-15行结构化总结）
     ↓ 001 周期性整理
Layer 2：可复用 Skill 文件（放进 skills/ 目录）
```

每次 A2A 任务完成后，002 必须产出 Closeout：
```markdown
## Closeout [TID:xxx]
- 完成了什么：
- 产出路径：
- 遇到的问题：
- 可复用的经验：
- 验证方式：`cat [路径]`
```

---

## 九、当前行动项（001 待执行）

- [ ] 确认 002 的 workspace 路径（问旭）
- [ ] `openclaw agents add 002 --workspace <路径>` 注册 002
- [ ] 验证 `openclaw agents list` 出现两个 agent
- [ ] 测试 `sessions_send` 到 002 的 sessionKey
- [ ] 跑一次最小 A2A 测试：001 给 002 发"pwd"任务，002 回复结果

---

## 十、参考资料

- OpenClaw 官方 Multi-Agent 文档：https://docs.openclaw.ai/
- opencrew 开源项目：https://github.com/AlexAnys/opencrew
- A2A 协议原文：https://github.com/AlexAnys/opencrew/blob/main/shared/A2A_PROTOCOL.md
