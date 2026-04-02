# hooks-system skill

> 基于 claw-code hooks.json 重新设计 OpenClaw 生命周期钩子
> 状态：v1.0 设计文档，Hook 点已定义

---

## claw-code 原始设计

104 个 hook 模块，覆盖：
- **通知钩子**：IDE状态、插件安装、LSP初始化、速率限制警告
- **工具权限钩子**：coordinatorHandler / interactiveHandler / swarmWorkerHandler
- **建议钩子**：fileSuggestions、unifiedSuggestions
- **渲染钩子**：fileSuggestions.ts、renderPlaceholder.ts

命名风格：`use{做什么}{何时/什么状态}.{ts|tsx}`

---

## OpenClaw 6点 Hook 设计

OpenClaw 当前只有 `hooks.system.session-memory` 一个内部 hook。
扩展到 6 个标准化拦截点：

### 事件定义

| 事件名 | 时机 | 传入数据 | 用途 |
|--------|------|---------|------|
| `pre_prompt` | 用户消息发出前 | `{prompt, context}` | 内容审核、敏感词过滤、上下文补充 |
| `post_prompt` | 用户消息已发送 | `{prompt, context, routing}` | 路由日志、意图预判 |
| `pre_tool` | 工具执行前 | `{tool_name, args}` | 权限检查、安全确认、参数改写 |
| `post_tool` | 工具执行后 | `{tool_name, result}` | 结果校验、日志记录、异常处理 |
| `pre_response` | 回复发出前 | `{response, context}` | 格式检查、内容过滤 |
| `post_response` | 回复已发出 | `{response, sent_at}` | 推送记录、归档 |

### 触发链

```
用户消息
  → pre_prompt[hook] → [模型处理] → post_prompt[hook]
                                         ↓
                                   [工具执行]
                                         ↓
pre_tool[hook] → [工具] → post_tool[hook]
                                         ↓
                                  pre_response[hook] → [发送] → post_response[hook]
```

### 配置格式

```yaml
hooks:
  internal:
    enabled: true
    entries:
      session-memory:
        enabled: true
      # 新增 6 点
      pre_prompt_audit:
        enabled: true
        hook: pre_prompt
        script: scripts/hooks/pre-prompt-audit.js
      pre_tool_check:
        enabled: true
        hook: pre_tool
        script: scripts/hooks/pre-tool-check.js
      post_tool_log:
        enabled: true
        hook: post_tool
        script: scripts/hooks/post-tool-log.js
```

### 脚本模板

```javascript
// scripts/hooks/pre-tool-check.js
// 传入：{ tool_name, args, context }
// 返回：{ allowed: boolean, modified_args?, reason? }

function pre_tool_check(input) {
  const dangerous = ['rm', 'dd', 'shutdown'];
  if (dangerous.includes(input.tool_name)) {
    return { allowed: false, reason: `危险工具: ${input.tool_name}` };
  }
  return { allowed: true };
}
```

---

## 当前 OpenClaw Hook 状态

```json
"hooks": {
  "internal": {
    "enabled": true,
    "entries": {
      "session-memory": {
        "enabled": true
      }
    }
  }
}
```

**仅支持 `internal` 类型 entry，`pre_prompt` 等尚未实现**

---

## 迁移路径

1. **Phase 1（当前）**：定义 hook 规范，写入文档
2. **Phase 2**：实现 `pre_tool_check` 作为第一个真实 hook
3. **Phase 3**：扩展到全部 6 点

---

## 参考：claw-code 通知钩子映射

| claw-code hook | OpenClaw 等价 |
|----------------|--------------|
| `useInstallMessages` | skill 安装完成通知 |
| `useAutoModeUnavailableNotification` | exec 权限不足警告 |
| `useRateLimitWarningNotification` | API 速率限制预警 |
| `usePluginInstallationStatus` | 插件状态变更通知 |
| `useLspInitializationNotification` | MCP 服务连接通知 |
