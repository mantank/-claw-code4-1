#!/bin/bash
# 安全重启 openclaw-gateway，保证老进程先死干净

echo "停止 systemd 服务..."
systemctl --user stop openclaw-gateway.service 2>/dev/null

echo "强杀所有残留 openclaw-gateway 进程..."
pkill -9 -f "openclaw-gateway" 2>/dev/null
sleep 2

echo "剩余进程检查..."
REMAINING=$(ps aux | grep openclaw-gateway | grep -v grep | wc -l)
if [ "$REMAINING" -gt 0 ]; then
    echo "还有 $REMAINING 个残留，继续清理..."
    ps aux | grep openclaw-gateway | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null
    sleep 1
fi

echo "启动 Gateway..."
systemctl --user start openclaw-gateway.service
sleep 3

echo "验证："
ps aux | grep openclaw-gateway | grep -v grep
openclaw gateway status 2>/dev/null | grep "Runtime\|RPC"
