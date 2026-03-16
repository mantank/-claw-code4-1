# Coding Agent 长任务模式（来源：刘小排公众号 2026-03-02）

## 核心模式：tmux + 定时汇报 + 自动重启

### 问题
OpenClaw调用外部Coding Agent（Codex/Claude Code/Gemini CLI）有超时限制，长任务会被杀死。

### 解法
1. **tmux隔离进程** — 在tmux session里启动Coding Agent，与OpenClaw生命周期解耦
2. **定时汇报** — OpenClaw每10分钟读tmux日志，向用户汇报进度
3. **自动重启** — 如果Coding Agent进程死了，OpenClaw自动重新启动
4. **完成后互审** — OpenClaw审核代码，与Coding Agent讨论，达成一致再提交

### Prompt模板
```
我即将给你布置一个需要长时间完成的编程任务。
请你使用tmux打开[Codex CLI/Claude Code]完成任务，使用最强模型、最大推理力度，授予Full Access权限。
每10分钟给我汇报进度。如果进程死了，重新启动。
写完代码后进行Review，发现问题跟它讨论，直到达成一致。
```

### 关键洞察
- "说人话"：不需要编排流程，直接说目标
- 多Agent互审：OpenClaw提意见 → Codex可以采纳也可以反驳 → 达成一致才提交
- 后续复用只需一句："用tmux里的Codex写代码"
