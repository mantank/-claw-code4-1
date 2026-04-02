# session-init skill

> 基于 claw-code system_init.py 的会话初始化报告
> 功能：每次 session 开始时生成完整的系统状态报告

---

## claw-code 设计

```python
def build_system_init_message(trusted: bool = True) -> str:
    setup = run_setup(trusted=trusted)
    commands = get_commands()
    tools = get_tools()
    return f"""# System Init
Trusted: {setup.trusted}
Built-in command names: {len(built_in_command_names())}
Loaded command entries: {len(commands)}
Loaded tool entries: {len(tools)}

Startup steps:
- {setup.setup.startup_steps()}
"""
```

**核心思想：新 session 开始时，先把所有可用资源、配置、状态都报告出来，让后续决策有据可依**

---

## OpenClaw Session 初始化内容

每次 session 开始（心跳触发），应生成：

### 1. 模型状态
```
- 当前模型：minimax-portal/MiniMax-M2.7-highspeed
- Fallback 模型：gpt-5.4 / Claude / GLM-5 等
```

### 2. 资源状态
```
- Context 使用：30%
- Token 消耗：39k in / 1.6k out
- Compaction 次数：0
```

### 3. 工具状态
```
- 可用工具：exec/read/write/sessions_*/image/web_*/memory_*
- 活跃 Skills：44个
- 活跃 Plugins：7个
```

### 4. 团队状态
```
- 002: 最近活跃 2h前（任务：公众号流水线）
- 003: 维护模式（情报库8分类完成）
- 004: 正常（xiaolongxia.app，案例425个）
```

### 5. 升级进度
```
- 第二阶段：9/10 模块已完成
- 下次心跳：2.10 system_init
```

---

## 运行会话初始化报告

在心跳开始时自动运行（已集成到 HEARTBEAT.md）。

如需手动触发：

```bash
echo "=== Session Init Report ===" && \
bash ~/.openclaw/workspace/scripts/system-check.sh && \
bash ~/.openclaw/workspace/scripts/workspace-scan.sh && \
bash ~/.openclaw/workspace/scripts/tool-registry-report.sh
```

---

## 与 claw-code 的差异

| claw-code | OpenClaw |
|-----------|---------|
| 启动时自动触发 | 心跳触发（每30分钟） |
| 命令+工具快照 | Skills + Plugins |
| 固定 markdown 格式 | 多脚本组合 |
| 运行时注入 system message | 作为参考文档存在 |
