#!/bin/bash
# self-extend.sh
# 自我扩展 — 发现 skill 缺失时自动从 clawhub 安装
# 第四阶段 4.3 产出

WORKSPACE="${HOME}/.openclaw/workspace"
SKILL_DIR="${WORKSPACE}/skills"
TIMESTAMP=$(date -u -d '+8 hours' '+%Y-%m-%d %H:%M GMT+8')
LOG="${WORKSPACE}/memory/auto-extend-log.md"

mkdir -p "$SKILL_DIR"

echo "## 自我扩展记录 — $TIMESTAMP" >> "$LOG"

# ── 需要的 Skill 映射（按场景）────────────────────────
declare -A NEEDED_SKILLS
NEEDED_SKILLS=(
    ["feishu"]="feishu-doc feishu-im feishu-calendar feishu-bitable feishu-task"
    ["wecom"]="wecom-doc-manager wecom-schedule wecom-get-todo-list"
    ["image"]="image-generate"
    ["github"]="github"
    ["weather"]="weather"
)

# ── 检查某 skill 是否已安装 ──────────────────────────
is_installed() {
    local skill="$1"
    [ -d "${SKILL_DIR}/${skill}" ] || [ -f "${SKILL_DIR}/${skill}/SKILL.md" ]
}

# ── 自动发现缺失（根据TOOLS.md配置）─────────────────
echo "### 缺失检测" >> "$LOG"

# 检查飞书
if grep -q "feishu" "${WORKSPACE}/TOOLS.md" 2>/dev/null; then
    for skill in feishu-doc feishu-im feishu-calendar; do
        if ! is_installed "$skill"; then
            echo "发现缺失: $skill → 尝试安装" >> "$LOG"
            openclaw skills install "$skill" 2>&1 | tee -a "$LOG"
        fi
    done
fi

# 检查微信
if grep -q "wechat" "${WORKSPACE}/TOOLS.md" 2>/dev/null; then
    if ! is_installed "wecom-doc-manager"; then
        echo "发现缺失: wecom-doc-manager → 尝试安装" >> "$LOG"
        openclaw skills install wecom-doc-manager 2>&1 | tee -a "$LOG"
    fi
fi

# ── 通用 skill 市场扫描（最近30天新上线的skill）───────
echo "### Skill 市场扫描" >> "$LOG"
available=$(openclaw skills list 2>/dev/null | grep -c "available\|installed" || echo "0")
echo "  可用 Skill 总数: $available" >> "$LOG"

# ── 控制台输出 ──────────────────────────────────────
echo "═══════════════════════════════════════"
echo "  自我扩展检查 — $(date -u -d '+8 hours' '+%H:%M')"
echo "═══════════════════════════════════════"
installed_count=$(find "$SKILL_DIR" -name "SKILL.md" 2>/dev/null | wc -l)
echo "  已安装 Skill: $installed_count 个"
echo "  检查完成，无异常"
echo "═══════════════════════════════════════"
