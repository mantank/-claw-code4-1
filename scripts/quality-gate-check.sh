#!/bin/bash
# quality-gate-check.sh
# 操作风险分级检查
# Basic: 直接过 / Standard: 校验 / Strict: 二次确认

TOOL="$1"
ARGS="${2:-}"

# 风险分类
is_strict() {
    case "$1" in
        rm|dd|shutdown|reboot|mkfs|init)
            return 0 ;;
        *)
            return 1 ;;
    esac
}

is_standard() {
    case "$1" in
        write|edit|exec|sessions_send|subagents|write)
            return 0 ;;
        *)
            return 1 ;;
    esac
}

classify() {
    if is_strict "$1"; then
        echo "STRICT"
    elif is_standard "$1"; then
        echo "STANDARD"
    else
        echo "BASIC"
    fi
}

# 主逻辑
LEVEL=$(classify "$TOOL")

case "$LEVEL" in
    STRICT)
        echo "🔴 STRICT: $TOOL — 需要二次确认"
        echo "   操作: $TOOL"
        echo "   参数: $ARGS"
        echo "   风险: 危险操作"
        exit 2  # Strict 需要人工确认
        ;;
    STANDARD)
        echo "🟡 STANDARD: $TOOL — 将执行并验证结果"
        echo "   操作: $TOOL"
        echo "   参数: $ARGS"
        echo "   风险: 中等，将校验执行结果"
        exit 0
        ;;
    BASIC)
        echo "🟢 BASIC: $TOOL — 直接执行"
        exit 0
        ;;
esac
