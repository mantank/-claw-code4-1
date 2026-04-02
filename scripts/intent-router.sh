#!/bin/bash
# intent-router.sh
# 意图级别智能路由 — 第三阶段 3.5 产出
# 根据用户意图关键词，将任务路由到正确的 Agent/Skill

INTENT="$1"
shift
PARAMS="$*"

# 意图关键词 → 路由目标映射表
route_intent() {
    local intent="$1"
    
    case "$intent" in
        # 内容相关 → 002
        *文章*|*公众号*|*写*|*草稿*|*发布*|*小红书*|*笔记*)
            echo "AGENT:002|content"
            ;;
        *配图*|*封面*|*图片*)
            echo "AGENT:002|assets"
            ;;
        
        # 网站/案例库 → 004
        *网站*|*案例*|*xiaolongxia*|*上传*|*SEO*)
            echo "AGENT:004|website"
            ;;
        
        # 情报/调研 → 003
        *情报*|*调研*|*竞品*|*趋势*|*调查*)
            echo "AGENT:003|research"
            ;;
        
        # 系统/配置/安装 → 001
        *安装*|*配置*|*升级*|*系统*|*检查*|*帮我*)
            echo "AGENT:001|system"
            ;;
        
        # 会议/日程/飞书 → 001 (通过飞书skill)
        *会议*|*日程*|*calendar*)
            echo "SKILL:feishu-calendar|schedule"
            ;;
        
        # 审批 → 001 (通过飞书skill)
        *审批*|*approval*)
            echo "SKILL:feishu-approval|approval"
            ;;
        
        # 消息/群 → 001 (通过飞书skill)
        *发消息*|*建群*|*群管理*)
            echo "SKILL:feishu-im|im"
            ;;
        
        # 未知 → 001 自己处理
        *)
            echo "AGENT:001|unknown"
            ;;
    esac
}

# 解析参数
case "$INTENT" in
    publish|P)
        DEST=$(route_intent "发布公众号")
        echo "路由: $DEST"
        echo "动作: 发布内容"
        ;;
    write|W)
        DEST=$(route_intent "$PARAMS")
        echo "路由: $DEST"  
        echo "动作: 写作内容"
        ;;
    research|R)
        DEST=$(route_intent "$PARAMS")
        echo "路由: $DEST"
        echo "动作: 调研"
        ;;
    system|S)
        DEST=$(route_intent "$PARAMS")
        echo "路由: $DEST"
        echo "动作: 系统操作"
        ;;
    *)
        # 直接路由
        DEST=$(route_intent "$INTENT")
        echo "$DEST"
        ;;
esac
