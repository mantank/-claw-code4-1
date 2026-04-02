# execution-registry skill

> 基于 claw-code execution_registry.py 的工具/命令执行路由
> 功能：理解工具执行流程，设计多工具并发执行方案

---

## claw-code 设计

```python
@dataclass(frozen=True)
class MirroredCommand:
    name: str
    source_hint: str
    def execute(self, prompt: str) -> str:
        return execute_command(self.name, prompt).message

@dataclass(frozen=True)
class MirroredTool:
    name: str
    source_hint: str
    def execute(self, payload: str) -> str:
        return execute_tool(self.name, payload).message

@dataclass(frozen=True)
class ExecutionRegistry:
    commands: tuple[MirroredCommand, ...]
    tools: tuple[MirroredTool, ...]

    def command(self, name: str) -> MirroredCommand | None:
        # 按名字查找 command
    def tool(self, name: str) -> MirroredTool | None:
        # 按名字查找 tool
```

**核心思想：所有工具/命令都通过 registry 统一路由，按名字查找执行器**

---

## OpenClaw 的执行链路

```
用户消息
  → LLM 判断意图
     → 匹配工具（read/write/exec/subagents/...）
        → 执行器（tool handler）
           → 返回结果
```

OpenClaw 已有 `subagents` 工具支持**并发执行**多个任务：

```markdown
使用 subagents 同时执行：
- [task1] sessions_spawn agent=002 ...
- [task2] sessions_spawn agent=003 ...
```

---

## 多工具并发执行方案

### 场景：需要同时执行多个独立任务

**方案：用 subagents 并发**

```markdown
用 subagents 同时执行以下3个任务：

[task:文件扫描] exec: bash workspace-scan.sh
[task:成本检查] session_status
[task:版本检查] exec: version-check.sh

等待全部完成，汇总结果。
```

### 场景：按序执行，每个依赖前一个结果

**方案：sequential（已有）**

每个工具按顺序执行，下一个工具可以看到上一个的输出。

---

## 工具执行状态追踪

| 状态 | 含义 |
|------|------|
| `pending` | 已提交，未开始 |
| `running` | 执行中 |
| `completed` | 成功完成 |
| `failed` | 执行失败 |
| `timeout` | 执行超时 |

**OpenClaw subagents 已有状态追踪**（sessions_list 可查活跃状态）

---

## 注册表查询命令

```bash
# 查找当前可用工具
grep -r "tool\|Tool" "${HOME}/.openclaw/workspace/skills/" --include="*.md" -l | head -20

# 查看工具执行日志
cat "${HOME}/.openclaw/workspace/memory/$(date +%Y-%m-%d).md" | grep -i "exec\|tool" | tail -20
```
