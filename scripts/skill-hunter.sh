#!/bin/bash
# 003号技能猎人 - 自动发现、评估、测试新技能
# 每30分钟运行一次，输出发现报告

set -e

WORKSPACE="/root/.openclaw/workspace"
SKILL_DB="$WORKSPACE/memory/skill-hunter-db.json"
REPORT_DIR="$WORKSPACE/tmp/skill-reports"
INSTALLED_DIR="$WORKSPACE/skills"

mkdir -p "$REPORT_DIR"

# 初始化技能数据库（如果不存在）
if [ ! -f "$SKILL_DB" ]; then
  echo '{"scanned":[],"installed":[],"rejected":[],"last_run":"","total_discovered":0}' > "$SKILL_DB"
fi

# 搜索关键词池（每次随机选3-5个搜索）
KEYWORDS=(
  "automation" "social" "content" "productivity" "data" 
  "monitor" "publish" "translate" "finance" "email"
  "calendar" "notion" "feishu" "wechat" "xiaohongshu"
  "image" "video" "audio" "scraper" "browser"
  "github" "deploy" "security" "backup" "analytics"
  "writing" "seo" "marketing" "crm" "workflow"
  "agent" "memory" "cron" "search" "api"
  "pdf" "excel" "database" "news" "rss"
)

# 随机选5个关键词
SELECTED=()
for i in $(shuf -i 0-$((${#KEYWORDS[@]}-1)) -n 5); do
  SELECTED+=("${KEYWORDS[$i]}")
done

echo "🔍 本轮搜索关键词: ${SELECTED[*]}"
echo "---"

# 获取已扫描过的技能列表
SCANNED=$(python3 -c "import json; d=json.load(open('$SKILL_DB')); print(' '.join(d['scanned']))" 2>/dev/null || echo "")

# 获取已安装的技能列表
ALREADY_INSTALLED=$(ls "$INSTALLED_DIR" 2>/dev/null | tr '\n' ' ')

DISCOVERIES=""
NEW_COUNT=0

for keyword in "${SELECTED[@]}"; do
  echo "搜索: $keyword"
  RESULTS=$(clawhub search "$keyword" 2>&1 | grep -v "^-" | head -10)
  
  while IFS= read -r line; do
    # 提取技能名称（第一个单词）
    SKILL_NAME=$(echo "$line" | awk '{print $1}')
    [ -z "$SKILL_NAME" ] && continue
    
    # 跳过已扫描过的
    if echo "$SCANNED" | grep -qw "$SKILL_NAME"; then
      continue
    fi
    
    # 跳过已安装的
    if echo "$ALREADY_INSTALLED" | grep -qw "$SKILL_NAME"; then
      continue
    fi
    
    # 提取描述
    DESC=$(echo "$line" | sed "s/^$SKILL_NAME//" | sed 's/([^)]*)$//' | xargs)
    SCORE=$(echo "$line" | grep -oP '\([\d.]+\)' | tr -d '()')
    
    if [ -n "$SKILL_NAME" ] && [ -n "$DESC" ]; then
      DISCOVERIES="$DISCOVERIES\n- **$SKILL_NAME** (相关度:$SCORE): $DESC"
      NEW_COUNT=$((NEW_COUNT + 1))
      
      # 记录为已扫描
      python3 -c "
import json
d=json.load(open('$SKILL_DB'))
if '$SKILL_NAME' not in d['scanned']:
    d['scanned'].append('$SKILL_NAME')
    d['total_discovered'] = d.get('total_discovered',0) + 1
json.dump(d, open('$SKILL_DB','w'), ensure_ascii=False, indent=2)
" 2>/dev/null
    fi
  done <<< "$RESULTS"
done

# 更新运行时间
python3 -c "
import json, datetime
d=json.load(open('$SKILL_DB'))
d['last_run'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
json.dump(d, open('$SKILL_DB','w'), ensure_ascii=False, indent=2)
"

# 输出报告
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
TOTAL_SCANNED=$(python3 -c "import json; d=json.load(open('$SKILL_DB')); print(len(d['scanned']))")
TOTAL_INSTALLED=$(ls "$INSTALLED_DIR" | wc -l)

echo ""
echo "=========================="
echo "🤖 003号技能猎人报告"
echo "⏰ $TIMESTAMP"
echo "=========================="
echo "本轮搜索: ${SELECTED[*]}"
echo "新发现: $NEW_COUNT 个"
echo "累计扫描: $TOTAL_SCANNED 个"
echo "已安装: $TOTAL_INSTALLED 个"
echo ""

if [ $NEW_COUNT -gt 0 ]; then
  echo "📋 新发现的技能:"
  echo -e "$DISCOVERIES"
  echo ""
  echo "STATUS:NEW_SKILLS"
else
  echo "本轮没有发现新技能"
  echo "STATUS:NO_NEW"
fi
