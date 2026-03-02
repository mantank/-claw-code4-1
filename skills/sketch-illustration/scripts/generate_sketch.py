#!/usr/bin/env python3
"""
Generate a sketch-style illustration using qwen-image-max (Dashscope API).
¥0.04/张，替代 ZenMux/Gemini。
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

DASHSCOPE_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
API_KEY = "sk-3e086717facd4d88a573260d127a15b0"


def generate_image(prompt: str, output_path: str, size: str = "1664*936") -> bool:
    payload = {
        "model": "qwen-image-max",
        "input": {
            "messages": [{"role": "user", "content": [{"text": prompt}]}]
        },
        "parameters": {
            "negative_prompt": "低分辨率，低画质，文字模糊，扭曲，AI感，丑陋",
            "watermark": False,
            "size": size
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        DASHSCOPE_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    print(f"调用 qwen-image-max 生成图片...")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()}")
        return False

    result = json.loads(body)

    # 提取图片URL
    image_url = None
    try:
        content = result["output"]["choices"][0]["message"]["content"]
        for item in content:
            if "image" in item:
                image_url = item["image"]
                break
    except (KeyError, IndexError):
        print(f"错误：无法从响应中提取图片\n{json.dumps(result, ensure_ascii=False)[:500]}")
        return False

    if not image_url:
        print(f"错误：响应中没有图片URL\n{body[:500]}")
        return False

    # 下载图片
    print(f"下载图片: {image_url[:80]}...")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    try:
        urllib.request.urlretrieve(image_url, output_path)
    except Exception as e:
        print(f"下载失败: {e}")
        return False

    print(f"✅ 成功！图片保存到: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="用 qwen-image-max 生成插画配图")
    parser.add_argument("--prompt", required=True, help="图片生成提示词")
    parser.add_argument("--output", default="/root/.openclaw/workspace/assets/sketch_output.png", help="输出路径")
    parser.add_argument("--size", default="1664*936", help="尺寸 (默认16:9 PPT配图)")
    args = parser.parse_args()

    success = generate_image(args.prompt, args.output, args.size)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
