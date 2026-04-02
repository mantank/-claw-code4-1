#!/bin/bash
# self-upgrade.sh
# 自我升级 — 识别新版本价值，辅助一键升级
# 第四阶段 4.4 产出

WORKSPACE="${HOME}/.openclaw/workspace"
TIMESTAMP=$(date -u -d '+8 hours' '+%Y-%m-%d %H:%M GMT+8')
LOG="${WORKSPACE}/memory/auto-upgrade-log.md"

mkdir -p "$(dirname "$LOG")"

echo "## 自我升级检查 — $TIMESTAMP" >> "$LOG"

# ── 1. 获取当前版本 ────────────────────────────────
current=$(openclaw --version 2>/dev/null | head -1 || echo "未知")
echo "当前版本: $current" >> "$LOG"

# ── 2. 检查更新 ────────────────────────────────────
check_output=$(bash "${WORKSPACE}/scripts/version-check.sh" 2>/dev/null)
check_status=$(echo "$check_output" | grep -oP "STATUS:\K[A-Z_]+" | head -1)
new_version=$(echo "$check_output" | grep "最新版本:" | grep -oP '[0-9]+\.[0-9]+\.[0-9]+' | head -1)

echo "检查状态: $check_status | 最新: $new_version" >> "$LOG"

if [ "$check_status" = "NEW_VERSION" ]; then
    echo "🆕 发现新版本: $new_version" >> "$LOG"
    echo "### 升级建议" >> "$LOG"
    echo "版本: $current → $new_version" >> "$LOG"
    echo "说明: 建议通过心跳通知旭，由旭判断是否升级" >> "$LOG"
    echo "建议: **待用户确认**" >> "$LOG"
    echo ""
    echo "═══════════════════════════════════════"
    echo "  🆕 新版本可用: $new_version"
    echo "  当前: $current"
    echo "  请确认是否升级"
    echo "═══════════════════════════════════════"
elif [ "$check_status" = "ALREADY_NOTIFIED" ] || [ "$check_status" = "NO_UPDATE" ]; then
    echo "✅ 已最新，无需升级" >> "$LOG"
    echo "═══════════════════════════════════════"
    echo "  自我升级检查 — $(date -u -d '+8 hours' '+%H:%M')"
    echo "  $current ✅ 已最新"
    echo "═══════════════════════════════════════"
elif [ "$check_status" = "VERSION_CHANGED" ]; then
    echo "📝 版本已变更为: $current（已记录）" >> "$LOG"
    echo "═══════════════════════════════════════"
    echo "  版本变更已记录: $current"
    echo "═══════════════════════════════════════"
else
    echo "⚠️  检查结果未知: $check_status" >> "$LOG"
fi

echo "" >> "$LOG"
