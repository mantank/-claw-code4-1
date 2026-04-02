#!/bin/bash
# workspace-scan.sh
# 工作区自动扫描脚本
# 基于 claw-code context.py 设计

WORKSPACE="${HOME}/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

echo "## Workspace Context — $(date -u -d '+8 hours' '+%Y-%m-%d %H:%M GMT+8')"

# 代码文件统计
py_count=$(find . -name "*.py" -type f 2>/dev/null | wc -l)
js_count=$(find . -name "*.js" -type f 2>/dev/null | wc -l)
sh_count=$(find . -name "*.sh" -type f 2>/dev/null | wc -l)
ts_count=$(find . -name "*.ts" -type f 2>/dev/null | wc -l)
md_count=$(find . -name "*.md" -type f 2>/dev/null | wc -l)
json_count=$(find . -name "*.json" -type f 2>/dev/null | wc -l)

# 总文件数
total_files=$(find . -type f 2>/dev/null | wc -l)

# Git状态
if [ -d ".git" ]; then
    git_status="是"
    last_commit=$(git log -1 --format="%ci" 2>/dev/null | cut -d' ' -f1)
    days_since_commit=$((($(date +%s) - $(git log -1 --format=%ct 2>/dev/null)) / 86400))
    if [ -n "$days_since_commit" ]; then
        git_detail="，最后commit ${days_since_commit}天前 ($last_commit)"
    else
        git_detail=""
    fi
else
    git_status="否"
    git_detail=""
fi

# 依赖文件检测
has_req=false; has_pkg=false; has_pdm=false
[ -f "requirements.txt" ] && has_req=true
[ -f "package.json" ] && has_pkg=true
[ -f "Pipfile" ] || [ -f "pyproject.toml" ] && has_pdm=true

# 磁盘占用
disk_usage=$(du -sh . 2>/dev/null | cut -f1)

# 最近7天修改的文件
recent_files=$(find . -type f -mtime -7 ! -path './.git/*' 2>/dev/null | sort | tail -10)

# 最近24小时修改的文件
recent_24h=$(find . -type f -mtime -1 ! -path './.git/*' 2>/dev/null | sort | wc -l)

echo ""
echo "- 代码文件：$((py_count + js_count + sh_count + ts_count)) 个 (.py: $py_count / .js: $js_count / .sh: $sh_count / .ts: $ts_count)"
echo "- Markdown：$md_count 个"
echo "- 配置文件：$json_count 个 (.json)"
echo "- 总文件数：$total_files"
echo "- Git仓库：$git_status$git_detail"
echo "- 依赖：requirements.txt $([ "$has_req" = true ] && echo '✅' || echo '❌') | package.json $([ "$has_pkg" = true ] && echo '✅' || echo '❌')"
echo "- 磁盘占用：$disk_usage"
echo "- 今日活跃文件：$recent_24h 个"

if [ -n "$recent_files" ]; then
    echo ""
    echo "**最近7天修改：**"
    echo "$recent_files" | sed 's|^\./||' | head -5 | sed 's|^|- |'
fi
