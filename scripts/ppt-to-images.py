#!/usr/bin/env python3
"""
PPT HTML幻灯片转图片
用法: python3 ppt-to-images.py <html文件> <输出目录>
"""
import sys, os
from pathlib import Path
from playwright.sync_api import sync_playwright

def html_to_slides(html_path, output_dir):
    html_path = Path(html_path).resolve()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto(f"file://{html_path}")
        page.wait_for_timeout(1000)
        
        # 获取总页数
        total = page.evaluate("""() => {
            const slides = document.querySelectorAll('.slide, section, .page, [data-slide]');
            return slides.length || 1;
        }""")
        
        if total <= 1:
            # 尝试用键盘翻页
            page.screenshot(path=str(output_dir / "slide-01.png"))
            count = 1
            for i in range(2, 20):
                page.keyboard.press("ArrowRight")
                page.wait_for_timeout(300)
                new_shot = str(output_dir / f"slide-{i:02d}.png")
                page.screenshot(path=new_shot)
                # 检查是否到末尾（简单判断：连续两张一样则停止）
                if i > 1:
                    import hashlib
                    prev = open(str(output_dir / f"slide-{i-1:02d}.png"), 'rb').read()
                    curr = open(new_shot, 'rb').read()
                    if hashlib.md5(prev).hexdigest() == hashlib.md5(curr).hexdigest():
                        os.remove(new_shot)
                        break
                count = i
        else:
            count = total
            for i in range(total):
                page.evaluate(f"() => {{ const s=document.querySelectorAll('.slide,section,.page,[data-slide]'); s[{i}]?.scrollIntoView(); }}")
                page.wait_for_timeout(300)
                page.screenshot(path=str(output_dir / f"slide-{i+1:02d}.png"))
        
        browser.close()
        print(f"✅ 共截图 {count} 张，保存到 {output_dir}")
        return count

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 ppt-to-images.py <html文件> <输出目录>")
        sys.exit(1)
    html_to_slides(sys.argv[1], sys.argv[2])
