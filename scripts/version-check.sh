#!/bin/bash
# OpenClaw 版本监控脚本
# 用法: version-check.sh
# 功能: 检查是否有新版本，有则自动更新并输出变更内容

CURRENT=$(openclaw --version 2>/dev/null)
LATEST=$(npm show openclaw version 2>/dev/null)
STATE_FILE="$HOME/.openclaw/workspace/memory/version-state.json"

# 确保state文件存在
if [ ! -f "$STATE_FILE" ]; then
  echo '{"last_checked":"","last_version":"","last_updated":""}' > "$STATE_FILE"
fi

LAST_VERSION=$(python3 -c "import json;print(json.load(open('$STATE_FILE')).get('last_version',''))" 2>/dev/null)

echo "当前版本: $CURRENT"
echo "最新版本: $LATEST"
echo "上次记录: $LAST_VERSION"

if [ "$CURRENT" = "$LATEST" ] && [ "$CURRENT" = "$LAST_VERSION" ]; then
  echo "STATUS:NO_UPDATE"
  # 更新检查时间
  python3 -c "
import json
from datetime import datetime
f='$STATE_FILE'
d=json.load(open(f))
d['last_checked']=datetime.utcnow().isoformat()+'Z'
json.dump(d,open(f,'w'),indent=2)
"
  exit 0
fi

if [ "$CURRENT" != "$LATEST" ]; then
  echo "发现新版本！$CURRENT → $LATEST"
  echo "STATUS:NEW_VERSION"
  
  # 备份配置
  cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d%H%M%S)
  
  # 执行更新
  echo "开始更新..."
  npm install -g openclaw@latest 2>&1
  
  NEW_VERSION=$(openclaw --version 2>/dev/null)
  echo "更新后版本: $NEW_VERSION"
  
  # 验证认证是否正常
  echo "验证认证状态..."
  AUTH_CHECK=$(GEMINI_API_KEY=AIzaSyB3GsuTddVoxP5rGYce0F1285JjN3gHRYU openclaw models status 2>&1)
  if echo "$AUTH_CHECK" | grep -q "anthropic"; then
    echo "AUTH:OK"
  else
    echo "AUTH:FAILED - 可能需要重新配置"
    # 恢复备份
    LATEST_BAK=$(ls -t ~/.openclaw/openclaw.json.bak.* 2>/dev/null | head -1)
    if [ -n "$LATEST_BAK" ]; then
      echo "恢复配置备份: $LATEST_BAK"
      cp "$LATEST_BAK" ~/.openclaw/openclaw.json
    fi
  fi
  
  # 重启Gateway
  openclaw gateway restart 2>&1
  
  # 更新state
  python3 -c "
import json
from datetime import datetime
f='$STATE_FILE'
d=json.load(open(f))
d['last_checked']=datetime.utcnow().isoformat()+'Z'
d['last_version']='$NEW_VERSION'
d['last_updated']=datetime.utcnow().isoformat()+'Z'
json.dump(d,open(f,'w'),indent=2)
"
  echo "STATUS:UPDATED"
elif [ "$CURRENT" != "$LAST_VERSION" ]; then
  # 版本变了但不是通过我们更新的（可能老大手动更新了）
  echo "检测到版本变更: $LAST_VERSION → $CURRENT"
  echo "STATUS:VERSION_CHANGED"
  python3 -c "
import json
from datetime import datetime
f='$STATE_FILE'
d=json.load(open(f))
d['last_checked']=datetime.utcnow().isoformat()+'Z'
d['last_version']='$CURRENT'
json.dump(d,open(f,'w'),indent=2)
"
fi
