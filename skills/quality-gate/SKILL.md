# quality-gate skill

> 基于 claw-code 架构设计推断的操作分级授权机制
> 状态：v1.0

---

## 设计目标

不同风险等级的操作，使用不同的验证严格程度：

| 级别 | 操作类型 | 验证 | 示例 |
|------|---------|------|------|
| **Basic** | 读取、非破坏 | 无验证，直接执行 | read / web_fetch / sessions_list |
| **Standard** | 写入、工具调用 | 结果校验 + 异常捕获 | write / edit / exec |
| **Strict** | 删除、外部发布 | 二次确认 + 执行日志 | rm / 推公众号 / 发Telegram |

---

## 风险操作清单

### Strict 级（必须二次确认）

| 操作 | 风险 | 确认方式 |
|------|------|---------|
| `rm` / `trash` | 文件删除 | 确认文件路径 + 显示将删除的内容 |
| `exec` with `rm\|dd\|shutdown` | 危险命令 | 列出具体命令，等 "yes" |
| 推送到公众号/外部平台 | 不可逆发布 | 显示内容摘要，等确认 |
| 修改 SESSION-STATE.md / MEMORY.md | 状态破坏 | 列出改动点 |

### Standard 级（自动校验）

| 操作 | 校验方式 |
|------|---------|
| `write` / `edit` | 写入后读取验证内容非空 |
| `exec` | 检查 exit code，为0才算成功 |
| `sessions_send` | 验证发送成功（检查 reply） |

### Basic 级（直接执行）

所有读取操作、查询操作、只读工具。

---

## 实现：操作分类函数

```javascript
// quality-gate.js
function classify_operation(tool_name, args) {
    const strict = ['rm', 'dd', 'shutdown', 'reboot', 'mkfs'];
    const standard_write = ['write', 'edit', 'exec', 'sessions_send'];
    
    if (strict.includes(tool_name)) return 'strict';
    if (standard_write.includes(tool_name)) return 'standard';
    return 'basic';
}

function validate_operation(tool_name, args, level) {
    switch(level) {
        case 'strict':
            return { needs_confirm: true, reason: `Strict操作: ${tool_name}` };
        case 'standard':
            return { needs_validation: true, check: 'result_not_empty' };
        case 'basic':
            return { allowed: true };
    }
}
```

---

## 心跳集成

在 HEARTBEAT.md 的任务7（claw-code升级）中，Quality Gate 作为第三阶段 3.1。

验证脚本路径：`~/.openclaw/workspace/scripts/quality-gate-check.sh`

---

## claw-code 对应

claw-code 源码中未找到显式的 "Quality Gate" 命名，但：
- `permissions.py` 的 `ToolPermissionContext` 提供了工具级别的过滤
- 工具执行结果通过 `TurnResult` 返回，包含 `stop_reason`
- 这是从架构推断出来的增强设计

---

## 待办

- [ ] `quality-gate-check.sh` 验证脚本
- [ ] 与 hooks.pre_tool 的集成
- [ ] 操作日志记录（谁在什么时间做了 Strict 操作）
