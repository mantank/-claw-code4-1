# 工具/命令路由 — 设计规范
## 第三阶段 3.5 产出

## 核心问题
用户说一句话，OpenClaw 需要知道：
1. **谁来干** — 哪个 Agent / 哪个 Skill
2. **怎么干** — 调用什么工具、传什么参数
3. **结果给谁** — 汇报给用户还是继续 pipeline

## 路由策略

### Level 1：关键词匹配（intent-router.sh）
```
if msg contains "文章" → AGENT:002|content
if msg contains "网站" → AGENT:004|website
if msg contains "情报" → AGENT:003|research
...
```

### Level 2：模式匹配（更精确）
```
"帮我发布" → 识别为 content + publish 动作
"帮我新建" → 识别为 create 动作 + 目标对象
```

### Level 3：LLM 分类（精确但慢）
用 MiniMax 对用户消息做意图分类，输出结构化路由结果。

## 路由表

| 意图关键词 | 路由目标 | Skill/工具 |
|-----------|---------|-----------|
| 文章/公众号/草稿/发布 | AGENT:002 | content pipeline |
| 配图/封面/图片 | AGENT:002 | image generation |
| 网站/案例库/上传 | AGENT:004 | xiaolongxia |
| 情报/调研/竞品 | AGENT:003 | intel pipeline |
| 安装/配置/升级 | AGENT:001 | openclaw tools |
| 会议/日程 | SKILL:feishu-calendar | calendar |
| 审批 | SKILL:feishu-approval | approval |
| 发消息/建群 | SKILL:feishu-im | im |
| 待办/任务 | SKILL:wecom-edit-todo | todo |
| 文档 | SKILL:wecom-doc-manager | doc |

## 实施方式

### 轻量方案（当前）
intent-router.sh 脚本 + case/grep 关键词匹配
适用于：已知意图、明确关键词的场景

### 进阶方案
HEARTBEAT.md 中内置路由决策逻辑：
```
读取用户消息 → 调用 intent-router.sh → 获取路由目标 →
通过 sessions_send 发给对应 Agent → 追踪结果
```

### 完整方案（长期）
LLM-based intent classification：
```
用户消息 → MiniMax 分类 → {agent, action, params} → 执行
```
需要维护：意图分类模型 + 路由规则库

## 当前实现
scripts/intent-router.sh — 关键词级路由，Shell 脚本

## 待扩展
- [ ] 路由日志（记录每个意图的路由历史）
- [ ] 路由学习（根据用户反馈修正路由规则）
- [ ] 与 sessions_send 集成（自动分发任务）
- [ ] 置信度（当多个规则匹配时选择最确定的）
