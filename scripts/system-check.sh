#!/bin/bash
# system-check.sh
# OpenClaw 系统环境检测
# 基于 claw-code setup.py 设计

echo "## OpenClaw 系统检测报告 — $(date -u -d '+8 hours' '+%Y-%m-%d %H:%M GMT+8')"
echo ""

echo "### 运行时版本"
echo "- OpenClaw: $(openclaw --version 2>/dev/null | head -1 || echo '❌ 未找到')"
echo "- Node: $(node --version 2>/dev/null || echo '❌ 未找到')"
echo "- Python: $(python3 --version 2>/dev/null || echo '❌ 未找到')"
echo "- NPM: $(npm --version 2>/dev/null || echo '❌ 未找到')"
echo "- Git: $(git --version 2>/dev/null | sed 's/git version //' || echo '❌ 未找到')"
echo ""

echo "### 配置文件"
if openclaw config validate 2>&1 | grep -q "valid"; then
    echo "✅ openclaw.json 语法有效"
else
    echo "⚠️ openclaw.json 验证输出："
    openclaw config validate 2>&1 | head -5 | sed 's/^/  /'
fi
echo ""

echo "### 插件状态"
ext_dir="${HOME}/.openclaw/extensions"
if [ -d "$ext_dir" ]; then
    echo "- 插件目录: $ext_dir"
    for plugin in $(ls "$ext_dir" 2>/dev/null); do
        echo "  - $plugin"
    done
else
    echo "- 插件目录不存在"
fi
echo ""

echo "### 磁盘与内存"
echo "- Workspace磁盘: $(du -sh "${HOME}/.openclaw/workspace" 2>/dev/null | cut -f1 || echo '未知')"
echo "- Extensions磁盘: $(du -sh "$ext_dir" 2>/dev/null | cut -f1 || echo '未知')"
echo "- 内存: $(free -h 2>/dev/null | awk '/Mem:/ {print $3 "/" $2}' || echo '未知')"
echo ""

echo "### API Key 状态"
TOOLS_CONFIG="${HOME}/.openclaw/workspace/TOOLS.md"
if [ -f "$TOOLS_CONFIG" ]; then
    echo "- TOOLS.md 存在 ✅"
    # 检查关键key是否存在（不暴露值）
    grep -q "API Key: " "$TOOLS_CONFIG" && echo "  - 至少一个API Key已配置"
else
    echo "- TOOLS.md 不存在 ⚠️"
fi
echo ""

echo "### Gateway 状态"
if pgrep -f "openclaw" > /dev/null 2>&1; then
    echo "✅ OpenClaw Gateway 进程运行中"
    echo "  PID: $(pgrep -f 'openclaw' | head -1)"
else
    echo "❌ OpenClaw Gateway 未运行"
fi
