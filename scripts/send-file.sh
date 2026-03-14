#!/bin/bash
# 001专用发文件脚本
# 用法: send-file.sh <文件路径> [标题说明]
FILE="$1"
CAPTION="${2:-文件}"
CHAT_ID="8526440826"
BOT_TOKEN="8560860105:AAHvzn2r1z73KCEIRYIoOrIEUHIPEGvaA0o"

curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendDocument" \
  -F chat_id="$CHAT_ID" \
  -F document=@"$FILE" \
  -F caption="$CAPTION" | python3 -c "import json,sys; d=json.load(sys.stdin); print('✅ 已发送' if d.get('ok') else '❌ 发送失败: ' + str(d))"
