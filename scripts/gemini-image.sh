#!/bin/bash
# 用法: bash gemini-image.sh "prompt" "output.png"
PROMPT="$1"
OUTPUT="${2:-/tmp/test-image.png}"
API_KEY="AIzaSyDHiKNnvz71qzDIzk-I5ZVdyAwb2vuRxqo"

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent?key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"contents\":[{\"parts\":[{\"text\":\"$PROMPT\"}]}]}" \
  -o "$OUTPUT"

# Check if valid image
if file "$OUTPUT" | grep -q "image\|PNG\|JPEG"; then
    echo "OK: $OUTPUT"
else
    echo "FAIL: $(cat $OUTPUT | head -c 200)"
fi
