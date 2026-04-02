#!/bin/bash
# streaming-sim.sh
# 模拟 claw-code 6步 Streaming 事件协议

echo "=== Streaming 事件模拟 ==="
echo ""

EVENTS=(
    "message_start:session_id=abc123:prompt=帮我查一下天气"
    "command_match:commands=weather"
    "tool_match:tools=web_fetch,image"
    "permission_denial:denials=none"
    "message_delta:text=正在查询..."
    "message_stop:usage=input:500/output:1200:stop_reason=completed"
)

for event in "${EVENTS[@]}"; do
    IFS=':' read -r type rest <<< "$event"
    echo "📡 EVT: $type"
    echo "   数据: $rest"
    echo ""
    sleep 0.3
done

echo "✅ Streaming 完成"
echo ""
echo "=== 事件协议总结 ==="
echo "1. message_start       → Session开始，收到用户消息"
echo "2. command_match      → 命令路由结果"
echo "3. tool_match         → 工具路由结果"
echo "4. permission_denial  → 权限拦截（如有）"
echo "5. message_delta      → 流式输出片段"
echo "6. message_stop       → 回复结束，包含usage+stop_reason"
