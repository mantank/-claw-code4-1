# tool-registry skill

> 基于 claw-code Tool.py + tool_pool.py 的工具注册表管理
> 功能：查看、分组、过滤 OpenClaw 当前已注册工具

---

## claw-code 设计

```python
@dataclass(frozen=True)
class ToolDefinition:
    name: str
    purpose: str  # 一句话说明工具用途

@dataclass(frozen=True)
class ToolPool:
    tools: tuple[PortingModule, ...]
    simple_mode: bool
    include_mcp: bool

def assemble_tool_pool(simple_mode=False, include_mcp=True, permission_context=None):
    return ToolPool(
        tools=get_tools(simple_mode=simple_mode, include_mcp=include_mcp),
        ...
    )
```

核心思想：**工具按用途分类注册，可按模式（simple/mcp）和权限上下文过滤**。

---

## OpenClaw 当前工具注册

OpenClaw 的工具由 runtime 驱动，配置在 `openclaw.json` 的 `agents` 和 `plugins` 部分。

**内置工具类型：**
- `exec` — Shell 命令执行
- `read` / `write` / `edit` — 文件操作
- `sessions_*` — 会话管理
- `image` / `image_generate` — 图像
- `web_search` / `web_fetch` — 网络
- `memory_*` — 记忆系统
- `subagents` — 子 Agent

**插件工具（MCP）：**
- `feishu-*` — 飞书套件
- `wecom-*` — 企业微信
- `xiaohongshu-*` — 小红书
- 等等

---

## 工具注册表报告

运行注册表扫描：

```bash
bash ~/.openclaw/workspace/scripts/tool-registry-report.sh
```

输出内容包括：
- 内置工具清单及描述
- 当前已安装 MCP 工具
- 工具分类（文件/网络/通信/媒体/系统）
- 最近注册的技能（skills/）

---

## 工具过滤模式

claw-code 的 `simple_mode` 等价于 OpenClaw 的 `tools.profile`：

| profile | 工具范围 |
|---------|---------|
| `minimal` | exec/read/write/sessions |
| `coding` | + edit/memory/subagents |
| `messaging` | sessions/web_fetch/image |
| `full` | 全部工具 |

---

## 用途说明（ToolDefinition 风格）

| 工具 | 用途 |
|------|------|
| exec | 执行Shell命令 |
| read/write/edit | 文件读写改 |
| web_search | 网络信息检索 |
| web_fetch | 页面内容抓取 |
| sessions_list/send | Agent间通信 |
| image_generate | AI图片生成 |
| memory_search | 长期记忆检索 |
| subagents | 并行任务执行 |
