# tools-filter skill

> 基于 claw-code permissions.py 的 deny_prefixes 工具过滤扩展
> 状态：v1.0 — 配置文件级，运行时行为依赖 OpenClaw schema 支持

---

## 功能

扩展 OpenClaw 的工具过滤能力，支持：
- **deny_names**：精确匹配黑名单（已有）
- **deny_prefixes**：前缀匹配黑名单（新，支持 glob 风格）

### claw-code 原始设计

```python
@dataclass(frozen=True)
class ToolPermissionContext:
    deny_names: frozenset[str]       # 精确阻止："rm", "dd"
    deny_prefixes: tuple[str, ...]   # 前缀阻止："bash*", "eval*", "mcp_*"

    def blocks(self, tool_name: str) -> bool:
        lowered = tool_name.lower()
        return lowered in self.deny_names or \
               any(lowered.startswith(prefix) for prefix in self.deny_prefixes)
```

---

## 当前 OpenClaw 配置

```json
"tools": {
    "profile": "coding",
    "allow": [...],
    "deny": [...],
    "agentToAgent": {...}
}
```

**缺失功能：`denyPrefixes` 字段（OpenClaw schema 尚未支持）**

---

## 降级方案

### 方式一：配置级（立即可用）

在 `openclaw.json` 的 `channels.{telegram}.allowFrom` 之外，
通过 `tools.deny` 字段阻止危险工具：

```json
"tools": {
    "profile": "coding",
    "deny": ["Bash", "Write", "Edit"]
}
```

### 方式二：前缀过滤（未来支持）

当 OpenClaw schema 支持 `denyPrefixes` 后，可配置：

```json
"tools": {
    "profile": "coding",
    "denyPrefixes": ["mcp_*", "eval*", "dangerous_*"],
    "deny": ["rm", "dd"]
}
```

---

## 验证脚本

运行工具过滤检查：

```bash
bash ~/.openclaw/workspace/scripts/tools-filter-check.sh <tool_name>
```

返回：
- `ALLOW` — 工具未被阻止
- `DENY_EXACT` — 精确匹配阻止
- `DENY_PREFIX` — 前缀匹配阻止

---

## 前缀过滤实现（shell版）

```bash
# 检查工具是否被 deny_prefixes 阻止
check_deny_prefix() {
    local tool="$1"
    local prefixes=("mcp_" "eval" "dangerous_")
    
    for prefix in "${prefixes[@]}"; do
        if [[ "${tool,,}" == "${prefix}"* ]]; then
            return 0  # 被阻止
        fi
    done
    return 1  # 未被阻止
}
```

---

## 使用场景

1. **MCP 工具隔离**：前缀 `mcp_` 阻止所有 MCP 工具
2. **危险命令过滤**：前缀 `eval` 阻止 eval 类操作
3. **临时禁用某类工具**：前缀 `temp_off_*` 快速禁用

---

## 待 OpenClaw 支持的功能

- [ ] `tools.denyPrefixes` schema 字段
- [ ] 前缀匹配的运行时执行
- [ ] 前缀规则的动态更新（无需重启）
