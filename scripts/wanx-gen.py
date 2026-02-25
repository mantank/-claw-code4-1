#!/usr/bin/env python3
"""
万相2.6 图片生成脚本
用法: python3 wanx-gen.py "prompt内容" 输出文件名.png [宽*高]
默认尺寸: 1920*1080 (公众号封面横版)
"""
import urllib.request, json, sys, urllib.parse, os

API_KEY = "sk-3e086717facd4d88a573260d127a15b0"
URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

prompt = sys.argv[1] if len(sys.argv) > 1 else "卡通风格插画"
output = sys.argv[2] if len(sys.argv) > 2 else "output.png"
size = sys.argv[3] if len(sys.argv) > 3 else "1920*1080"

payload = {
    "model": "wan2.6-t2i",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ]
    },
    "parameters": {
        "size": size,
        "n": 1,
        "prompt_extend": True,
        "watermark": False
    }
}

data = json.dumps(payload, ensure_ascii=False).encode()
req = urllib.request.Request(URL, data=data, headers={
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
})

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
except urllib.error.HTTPError as e:
    print("Error:", e.code, e.read().decode())
    sys.exit(1)

img_url = result["output"]["choices"][0]["message"]["content"][0]["image"]

# 下载图片
save_path = os.path.join("/root/.openclaw/workspace/tmp", output)
os.makedirs(os.path.dirname(save_path), exist_ok=True)
urllib.request.urlretrieve(img_url, save_path)
print(f"MEDIA:{save_path}")
print(f"Saved: {save_path}")
