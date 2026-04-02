# streaming-protocol skill

> 基于 claw-code query_engine.py 的 stream_submit_message 6步事件协议
> 状态：v1.0 设计文档

---

## claw-code 6步事件流

```python
def stream_submit_message(...):
    yield {'type': 'message_start', 'session_id': ..., 'prompt': ...}      # 1
    yield {'type': 'command_match', 'commands': ...}                        # 2
    yield {'type': 'tool_match', 'tools': ...}                            # 3
    yield {'type': 'permission_denial', 'denials': [...]}                  # 4
    yield {'type': 'message_delta', 'text': result.output}                # 5
    yield {'type': 'message_stop', 'usage': {...}, 'stop_reason': ...}    # 6
```

| 步骤 | 事件 | 触发时机 |
|------|------|---------|
| 1 | `message_start` | Session 收到用户消息 |
| 2 | `command_match` | 路由匹配到命令 |
| 3 | `tool_match` | 路由匹配到工具 |
| 4 | `permission_denial` | 工具/命令被权限拦截 |
| 5 | `message_delta` | 流式输出片段 |
| 6 | `message_stop` | 回复完成，包含 usage + stop_reason |

---

## OpenClaw 事件协议设计

### 6步标准化事件

```
EVT: session_start      → 开启新 session
EVT: message_received   → 用户消息到达
EVT: routing_complete   → 路由决策完成（工具/命令匹配）
EVT: tool_executing    → 工具执行中
EVT: tool_completed     → 工具执行完成
EVT: response_ready     → 最终回复就绪
EVT: session_end        → Session 结束
```

### 使用场景

**场景1：前端订阅工具执行过程**
```javascript
// 前端订阅 streaming 事件
socket.on('tool_executing', ({tool_name, args}) => {
    showLoading(tool_name);
});
socket.on('tool_completed', ({tool_name, result}) => {
    hideLoading(tool_name);
    showResult(result);
});
```

**场景2：监控慢工具**
```javascript
// 如果 tool_executing 超过 30s 不见 tool_completed
// → 触发超时警告
```

---

## 当前 OpenClaw 实现

OpenClaw 已有 streaming 能力（`channels.telegram.streaming: "partial"`），
但事件协议未标准化。以上为未来扩展设计。

---

## 验证

运行事件模拟：
```bash
bash ~/.openclaw/workspace/scripts/streaming-sim.sh
```

---

## 与 Quality Gate 的关系

- `routing_complete` 事件 → 可触发 pre_tool hook（Quality Gate Standard 级别）
- `tool_completed` 事件 → 可触发 post_tool hook（Quality Gate 结果校验）
- `permission_denial` 事件 → 记录到 audit log
