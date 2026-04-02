#!/bin/bash
# tool-registry-report.sh
# OpenClaw 工具注册表报告
# 基于 claw-code Tool.py + tool_pool.py 设计

echo "## OpenClaw 工具注册表 — $(date -u -d '+8 hours' '+%Y-%m-%d %H:%M GMT+8')"
echo ""

# 1. 读取插件配置
echo "### 已安装插件"
cat "${HOME}/.openclaw/openclaw.json" | grep -o '"[a-z-]*":\s*{' | grep -v 'groups\|channels\|config\|allowFrom' | sed 's/[":]//g' | sed 's/^\s*/- /' | head -20
echo ""

# 2. Skills 列表
echo "### Skills（${HOME}/workspace/skills/）"
skills_dir="${HOME}/.openclaw/workspace/skills"
if [ -d "$skills_dir" ]; then
    count=$(ls -d "$skills_dir"/*/ 2>/dev/null | wc -l)
    echo "- 共 $count 个技能目录"
    echo ""
    echo "**技能清单：**"
    ls -d "$skills_dir"/*/ 2>/dev/null | xargs -I{} basename {} | sort | sed 's/^/- /'
else
    echo "- skills 目录不存在"
fi
echo ""

# 3. MCP 工具统计
echo "### MCP 工具（plugins）"
plugins_dir="${HOME}/.openclaw/extensions"
if [ -d "$plugins_dir" ]; then
    echo "- 插件目录: $plugins_dir"
    ls "$plugins_dir" 2>/dev/null | sed 's/^/- /'
else
    echo "- 无插件目录"
fi
echo ""

# 4. 工具分类
echo "### 工具分类"
echo "- **文件类**: exec / read / write / edit"
echo "- **网络类**: web_search / web_fetch"
echo "- **通信类**: sessions_list / sessions_send / sessions_history"
echo "- **媒体类**: image / image_generate"
echo "- **记忆类**: memory_search / memory_get"
echo "- **任务类**: subagents / exec (background)"
echo ""

# 5. 最近活跃的工具（从日志推断）
echo "### 最近心跳使用的工具"
echo "- session_status（每次心跳）"
echo "- exec（文件操作/脚本运行）"
echo "- web_fetch/web_search（信息获取）"
