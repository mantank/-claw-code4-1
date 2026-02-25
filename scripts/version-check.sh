#!/bin/bash
# OpenClaw 版本监控脚本
# 发现新版本只通知，不自动更新，等旭确认

CURRENT=$(openclaw --version 2>/dev/null)
LATEST=$(npm show openclaw version 2>/dev/null)
STATE_FILE="$HOME/.openclaw/workspace/memory/version-state.json"

if [ ! -f "$STATE_FILE" ]; then
  echo '{"last_checked":"","last_version":"","last_updated":""}' > "$STATE_FILE"
fi

LAST_VERSION=$(python3 -c "import json;print(json.load(open('$STATE_FILE')).get('last_version',''))" 2>/dev/null)

echo "当前版本: $CURRENT"
echo "最新版本: $LATEST"
echo "上次记录: $LAST_VERSION"

# 更新检查时间
python3 -c "
import json
from datetime import datetime
f='$STATE_FILE'
d=json.load(open(f))
d['last_checked']=datetime.utcnow().isoformat()+'Z'
json.dump(d,open(f,'w'),indent=2)
" 2>/dev/null

if [ "$CURRENT" = "$LATEST" ]; then
  echo "STATUS:NO_UPDATE"
  exit 0
fi

if [ "$CURRENT" != "$LATEST" ] && [ "$LATEST" = "$LAST_VERSION" ]; then
  # 已经通知过了，不重复
  echo "STATUS:ALREADY_NOTIFIED"
  exit 0
fi

# 发现新版本，只通知，不动
echo "发现新版本: $CURRENT → $LATEST"
echo "STATUS:NEW_VERSION"

# 记录已发现的新版本（防止重复通知）
python3 -c "
import json
from datetime import datetime
f='$STATE_FILE'
d=json.load(open(f))
d['last_version']='$LATEST'
json.dump(d,open(f,'w'),indent=2)
" 2>/dev/null
