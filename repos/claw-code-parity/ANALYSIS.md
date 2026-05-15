# claw-code-parity 架构分析

> 源码：ultraworkers/claw-code-parity（Python 移植版）
> 分析日期：2026-04-02

---

## 一、项目定位

这是 Claude Code 源码泄露后，社区用 Python 重新实现的"干净室版本"。
**不是直接复制**，而是通过读源码理解架构后，用 Python 重写核心模式。

当前状态：Python 实现已完成，Rust 移植进行中。
不是完整 1:1 等价替换，很多 runtime 逻辑还是 stub。

---

## 二、核心模块解析

### 1. query_engine.py — 引擎核心

**职责：** 对话轮次管理、路由、成本控制、session 持久化

**关键设计：**

```
QueryEnginePort
├── manifest: PortManifest（当前工作区结构快照）
├── config: QueryEngineConfig（max_turns/max_budget_tokens/compact_after）
├── mutable_messages: list[str]（当前轮次历史）
├── total_usage: UsageSummary（input/output tokens累计）
├── transcript_store: TranscriptStore（可压缩的历史）
└── permission_denials: list[PermissionDenial]
```

**Budget 控制：**
```python
# 每次submit_message前预估：
projected = total_usage.add_turn(prompt, output)
if projected.input_tokens + projected.output_tokens > max_budget_tokens:
    stop_reason = 'max_budget_reached'
```

**Compaction（对话压缩）：**
```python
# 超过compact_after_turns（默认12）时，截断旧消息
if len(mutable_messages) > config.compact_after_turns:
    mutable_messages[:] = mutable_messages[-compact_after_turns:]
    transcript_store.compact(compact_after_turns)
```

**Streaming（事件流）：**
```python
def stream_submit_message(...):
    yield {'type': 'message_start', 'session_id': ..., 'prompt': ...}
    yield {'type': 'command_match', 'commands': ...}
    yield {'type': 'tool_match', 'tools': ...}
    yield {'type': 'permission_denial', 'denials': [...]}
    yield {'type': 'message_delta', 'text': result.output}
    yield {'type': 'message_stop', 'usage': {...}, 'stop_reason': ...}
```
→ 这是一个标准的 6 步流式事件协议

---

### 2. runtime.py — 会话启动和路由

**职责：** 初始化 session → 路由 prompt → 执行命令/工具 → 记录历史

**路由算法（route_prompt）：**
```python
def route_prompt(self, prompt: str, limit: int = 5) -> list[RoutedMatch]:
    tokens = {token.lower() for token in prompt.replace('/', ' ').replace('-',' ').split()}
    by_kind = {
        'command': self._collect_matches(tokens, PORTED_COMMANDS, 'command'),
        'tool': self._collect_matches(tokens, PORTED_TOOLS, 'tool'),
    }
    # 优先各取一个最好的，然后按分数排序填满limit
```
→ 基于 token 匹配的轻量路由，不是 LLM 路由

**Bootstrap 流程：**
```python
def bootstrap_session(prompt):
    context = build_port_context()       # 扫描工作区
    setup_report = run_setup(trusted=True)  # Python/平台检测
    history = HistoryLog()                # 初始化历史
    matches = self.route_prompt(prompt)  # 路由
    # → 执行 matched commands + tools
    # → 提交给 QueryEnginePort
    # → 持久化 session
```

---

### 3. permissions.py — 工具权限模型

**设计：**
```python
@dataclass(frozen=True)
class ToolPermissionContext:
    deny_names: frozenset[str]       # 精确阻止的工具名
    deny_prefixes: tuple[str, ...]    # 前缀阻止（如 "bash*"）

    def blocks(self, tool_name: str) -> bool:
        lowered = tool_name.lower()
        return lowered in self.deny_names or \
               any(lowered.startswith(p) for p in self.deny_prefixes)
```

**过滤集成（tools.py）：**
```python
def get_tools(..., permission_context: ToolPermissionContext | None = None):
    tools = list(PORTED_TOOLS)
    if simple_mode: ...
    if not include_mcp: ...
    return filter_tools_by_permission_context(tuple(tools), permission_context)
```

---

### 4. models.py — 数据结构

```python
@dataclass(frozen=True)
class Subsystem:         # 模块/子系统元信息
    name: str
    path: str
    file_count: int
    notes: str

@dataclass(frozen=True)
class PortingModule:    # 可移植模块的元数据
    name: str
    responsibility: str  # 这个模块负责什么
    source_hint: str     # 来自原始源码的哪个文件
    status: str          # 'planned' / 'mirrored'

@dataclass(frozen=True)
class UsageSummary:      # token使用量
    input_tokens: int = 0
    output_tokens: int = 0

    def add_turn(self, prompt: str, output: str) -> 'UsageSummary':
        # 返回新的 UsageSummary（不可变）
```

---

### 5. context.py — 工作区上下文

```python
@dataclass(frozen=True)
class PortContext:
    source_root: Path
    tests_root: Path
    assets_root: Path
    archive_root: Path
    python_file_count: int
    test_file_count: int
    asset_file_count: int
    archive_available: bool
```

→ 在 bootstrap_session 时自动扫描工作区，生成结构化上下文快照

---

### 6. session_store.py — Session 持久化

```python
@dataclass(frozen=True)
class StoredSession:
    session_id: str
    messages: tuple[str, ...]
    input_tokens: int
    output_tokens: int

def save_session(session: StoredSession, directory: Path) -> Path:
    # 存为 .port_sessions/{session_id}.json

def load_session(session_id: str, directory: Path) -> StoredSession:
    # 从磁盘恢复
```

---

### 7. cost_tracker.py — 成本追踪

```python
@dataclass
class CostTracker:
    total_units: int = 0
    events: list[str] = field(default_factory=list)

    def record(self, label: str, units: int) -> None:
        self.total_units += units
        self.events.append(f'{label}:{units}')
```

→ 设计上比 OpenClaw 当前方案更轻量，events 记录适合生成消费报告

---

### 8. hooks/ — 生命周期钩子

**注意：** 这个模块在 parity 版本里是 placeholder，
真实实现在 reference_data/subsystems/hooks.json 快照里。
6 个标准钩子点：
1. pre-prompt
2. post-prompt  
3. pre-tool
4. post-tool
5. pre-response
6. post-response

---

## 三、设计模式总结

| # | 模式 | claw-code 实现 | OpenClaw 现状 |
|---|------|---------------|---------------|
| 1 | Hook 生命周期 | 6个拦截点，hooks.json 定义 | hooks.system 已有，entry 级别 |
| 2 | 三层权限模型 | deny_names + deny_prefixes 过滤 | tool filter 有，但 deny_prefixes 没有 |
| 3 | 质量门分级 | Basic/Standard/Strict（推断） | 无分级质量门 |
| 4 | 四层压缩策略 | compact_after_turns + max_budget_tokens + transcript_compact | contextPruning(mode=cache-ttl, ttl=1h) 较简单 |
| 5 | 记忆互斥提取 | 无重复处理的 PortingModule 机制 | 无对应设计 |
| 6 | Agent类型系统 | minimal/coding/messaging/full profile | tools.profile 已有 (minimal/coding/messaging/full) |
| 7 | 结构化通信 | 6步Streaming事件协议 | 无标准流式事件协议 |
| 8 | 跨会话交接 | session persist + load_session | SESSION-STATE.md 热缓存，但无标准化 handoff 文件 |

---

## 四、可借鉴的落地建议

### 高优先级（可立刻做）

1. **tools.exec.ask off** ✅ 已完成

2. **Session 持久化增强** — 当前 SESSION-STATE.md 是纯文本，claw-code 用 JSON schema + 路径存储，可更结构化

3. **cost_tracker 集成** — 在 HEARTBEAT.md 里加入 token 消耗记录，参考 UsageSummary 模式

4. **Compaction 策略升级** — 当前 ttl=1h 过于简单，可参考 compact_after_turns + budget_tokens 双触发

### 中优先级（需规划）

5. **Streaming 事件协议** — 定义 6 步标准事件格式，让工具执行可被前端订阅

6. **deny_prefixes 工具过滤** — 在 permissions.py 模式上扩展，支持 glob 匹配

7. **Quality Gate 分级** — Basic/Standard/Strict 三级，对应不同可信度的操作

### 低优先级（长期）

8. **Hook 6 点扩展** — 当前只有 session-memory，可增加 tool pre/post、response pre/post

9. **记忆互斥** — 跨会话检查"这件事上次谁做的"，避免重复劳动
