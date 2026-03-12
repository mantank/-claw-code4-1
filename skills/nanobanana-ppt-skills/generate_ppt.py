#!/usr/bin/env python3
"""
PPT Generator - Generate PPT slide images using Google Gemini API.

This script generates PPT slide images based on a slide plan and style template,
then creates an HTML viewer for playback.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# dotenv not needed - API key is hardcoded for Nano Banana 2 (gemini-3.1-flash-image-preview)


# =============================================================================
# Constants
# =============================================================================

DEFAULT_RESOLUTION = "2K"
DEFAULT_TEMPLATE_PATH = "templates/viewer.html"
OUTPUT_BASE_DIR = "outputs"

# Style template markers
TEMPLATE_START_MARKER = "## "
TEMPLATE_END_MARKER = "## "


# =============================================================================
# Environment Configuration
# =============================================================================

def find_and_load_env() -> bool:
    """No-op: API key is built-in for Nano Banana 2 (gemini-3.1-flash-image-preview)."""
    return True


# =============================================================================
# Style Template
# =============================================================================

def load_style_template(style_path: str) -> str:
    """
    Load style template - extract '## 基础提示词模板' section,
    or fall back to full file content.
    """
    with open(style_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Try to extract '## 基础提示词模板' section
    marker = "## 基础提示词模板"
    start_idx = content.find(marker)
    if start_idx != -1:
        start_idx += len(marker)
        # Find next ## section
        end_idx = content.find("\n## ", start_idx)
        if end_idx == -1:
            end_idx = len(content)
        return content[start_idx:end_idx].strip()

    # Fallback: return full content
    print("Warning: '## 基础提示词模板' not found, using full content")
    return content


# =============================================================================
# Prompt Generation
# =============================================================================

def generate_prompt(
    style_template: str,
    page_type: str,
    content_text: str,
    slide_number: int,
    total_slides: int,
) -> str:
    """
    Generate a prompt for a single slide.

    Args:
        style_template: Base style template text.
        page_type: Type of page (cover, data, content).
        content_text: Text content for the slide.
        slide_number: Current slide number (1-indexed).
        total_slides: Total number of slides.

    Returns:
        Complete prompt string for image generation.
    """
    prompt_parts = [style_template, "\n\n"]

    # Determine page type based on slide position or explicit type
    is_cover = page_type == "cover" or slide_number == 1
    is_data = page_type == "data" or slide_number == total_slides

    if is_cover:
        prompt_parts.append(
            f"""Please generate a cover page based on visual balance aesthetics.
Place a large complex 3D glass object in the center, overlaid with bold text:

{content_text}

Background with extended aurora waves."""
        )
    elif is_data:
        prompt_parts.append(
            f"""Please generate a data/summary page using split-screen design.
Left side: typeset the following text.
Right side: floating large glowing 3D data visualization:

{content_text}"""
        )
    else:
        prompt_parts.append(
            f"""Please generate a content page using Bento grid layout.
Organize the following content in modular rounded rectangle containers.
Container material must be frosted glass with blur effect:

{content_text}"""
        )

    return "".join(prompt_parts)


# =============================================================================
# Image Generation
# =============================================================================

QWEN_API_KEY = "sk-3e086717facd4d88a573260d127a15b0"

# 分辨率映射（16:9）
RESOLUTION_MAP = {
    "2K": "1664*936",
    "4K": "3328*1872",
}


def generate_slide(
    prompt: str,
    slide_number: int,
    output_dir: str,
    resolution: str = DEFAULT_RESOLUTION,
) -> Optional[str]:
    """
    Generate a single PPT slide image using Nano Banana 2 (gemini-3.1-flash-image-preview) API.
    ¥0.04/张，替代 Gemini。
    """
    import urllib.request
    import urllib.error

    size = RESOLUTION_MAP.get(resolution, "1664*936")
    print(f"  生成第 {slide_number} 页 (Nano Banana 2 (gemini-3.1-flash-image-preview), {size})...")

    payload = {
        "model": "Nano Banana 2 (gemini-3.1-flash-image-preview)",
        "input": {
            "messages": [{"role": "user", "content": [{"text": prompt}]}]
        },
        "parameters": {
            "negative_prompt": "低分辨率，低画质，文字模糊，扭曲，AI感",
            "watermark": False,
            "size": size
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        QWEN_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {QWEN_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"  第 {slide_number} 页失败: HTTP {e.code}: {e.read().decode()}")
        return None
    except Exception as e:
        print(f"  第 {slide_number} 页失败: {e}")
        return None

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
        print(f"  第 {slide_number} 页失败: 无法提取图片URL\n{body[:300]}")
        return None

    if not image_url:
        print(f"  第 {slide_number} 页失败: 响应中无图片")
        return None

    # 下载图片
    image_path = os.path.join(output_dir, "images", f"slide-{slide_number:02d}.png")
    try:
        import urllib.request as ur
        ur.urlretrieve(image_url, image_path)
        print(f"  ✅ 第 {slide_number} 页保存: {image_path}")
        return image_path
    except Exception as e:
        print(f"  第 {slide_number} 页下载失败: {e}")
        return None


# =============================================================================
# Output Generation
# =============================================================================

def generate_viewer_html(
    output_dir: str,
    slide_count: int,
    template_path: str,
) -> str:
    """
    Generate HTML viewer for slides playback.

    Args:
        output_dir: Output directory path.
        slide_count: Total number of slides.
        template_path: Path to HTML template.

    Returns:
        Path to generated HTML file.
    """
    with open(template_path, "r", encoding="utf-8") as f:
        html_template = f.read()

    # Generate image list
    slides_list = [f"'images/slide-{i:02d}.png'" for i in range(1, slide_count + 1)]

    # Replace placeholder
    html_content = html_template.replace(
        "/* IMAGE_LIST_PLACEHOLDER */",
        ",\n            ".join(slides_list),
    )

    html_path = os.path.join(output_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"  Viewer HTML generated: {html_path}")
    return html_path


def save_prompts(output_dir: str, prompts_data: Dict[str, Any]) -> str:
    """
    Save all prompts to JSON file.

    Args:
        output_dir: Output directory path.
        prompts_data: Dictionary containing all prompts and metadata.

    Returns:
        Path to saved JSON file.
    """
    prompts_path = os.path.join(output_dir, "prompts.json")
    with open(prompts_path, "w", encoding="utf-8") as f:
        json.dump(prompts_data, f, ensure_ascii=False, indent=2)
    print(f"  Prompts saved: {prompts_path}")
    return prompts_path


# =============================================================================
# Main Entry Point
# =============================================================================

def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="PPT Generator - Generate PPT images using Gemini API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python generate_ppt.py --plan slides_plan.json --style styles/gradient-glass.md --resolution 2K

Environment variables:
  GEMINI_API_KEY: Google AI API key (required)
""",
    )

    parser.add_argument(
        "--plan",
        required=True,
        help="Path to slides plan JSON file (generated by Skill)",
    )
    parser.add_argument(
        "--style",
        required=True,
        help="Path to style template file",
    )
    parser.add_argument(
        "--resolution",
        choices=["2K", "4K"],
        default=DEFAULT_RESOLUTION,
        help=f"Image resolution (default: {DEFAULT_RESOLUTION})",
    )
    parser.add_argument(
        "--output",
        help="Output directory path (default: outputs/TIMESTAMP)",
    )
    parser.add_argument(
        "--template",
        default=DEFAULT_TEMPLATE_PATH,
        help=f"HTML template path (default: {DEFAULT_TEMPLATE_PATH})",
    )

    return parser


def main() -> None:
    """Main entry point for PPT generation."""
    # Load environment variables
    find_and_load_env()

    # Parse arguments
    parser = create_argument_parser()
    args = parser.parse_args()

    # Load slides plan
    with open(args.plan, "r", encoding="utf-8") as f:
        slides_plan = json.load(f)

    # Load style template
    style_template = load_style_template(args.style)

    # Create output directory
    if args.output:
        output_dir = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"{OUTPUT_BASE_DIR}/{timestamp}"

    os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)

    # Print configuration
    slides = slides_plan["slides"]
    total_slides = len(slides)

    print("=" * 60)
    print("PPT Generator Started")
    print("=" * 60)
    print(f"Style: {args.style}")
    print(f"Resolution: {args.resolution}")
    print(f"Slides: {total_slides}")
    print(f"Output: {output_dir}")
    print("=" * 60)
    print()

    # Initialize prompts data
    prompts_data: Dict[str, Any] = {
        "metadata": {
            "title": slides_plan.get("title", "Untitled Presentation"),
            "total_slides": total_slides,
            "resolution": args.resolution,
            "style": args.style,
            "generated_at": datetime.now().isoformat(),
        },
        "slides": [],
    }

    # Generate each slide
    for slide_info in slides:
        slide_number = slide_info["slide_number"]
        page_type = slide_info.get("page_type", "content")
        content_text = slide_info["content"]

        # Generate prompt
        prompt = generate_prompt(
            style_template,
            page_type,
            content_text,
            slide_number,
            total_slides,
        )

        # Generate image
        image_path = generate_slide(prompt, slide_number, output_dir, args.resolution)

        # Record prompt data
        prompts_data["slides"].append({
            "slide_number": slide_number,
            "page_type": page_type,
            "content": content_text,
            "prompt": prompt,
            "image_path": image_path,
        })

        print()

    # Save prompts
    save_prompts(output_dir, prompts_data)

    # Generate viewer HTML
    generate_viewer_html(output_dir, total_slides, args.template)

    # Print completion summary
    print()
    print("=" * 60)
    print("Generation Complete!")
    print("=" * 60)
    print(f"Output directory: {output_dir}")
    print(f"Viewer HTML: {os.path.join(output_dir, 'index.html')}")
    print()
    print("Open viewer in browser:")
    print(f"  open {os.path.join(output_dir, 'index.html')}")
    print()


if __name__ == "__main__":
    main()
