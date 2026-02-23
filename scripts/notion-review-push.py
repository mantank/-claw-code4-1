#!/usr/bin/env python3
"""推送每日复盘到Notion，使用结构化blocks"""
import requests, json, sys
from datetime import datetime, timezone, timedelta

NOTION_KEY = "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"
DATABASE_ID = "bf0b46f590d943089e758c61c0a7b0e7"

def heading2(text):
    return {"object":"block","type":"heading_2","heading_2":{"rich_text":[{"type":"text","text":{"content":text}}]}}

def paragraph(text, bold=False):
    ann = {"bold":bold,"italic":False,"strikethrough":False,"underline":False,"code":False,"color":"default"}
    return {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"type":"text","text":{"content":text},"annotations":ann}]}}

def bullet(text):
    return {"object":"block","type":"bulleted_list_item","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":text}}]}}

def divider():
    return {"object":"block","type":"divider","divider":{}}

def quote(text):
    return {"object":"block","type":"quote","quote":{"rich_text":[{"type":"text","text":{"content":text}}]}}

def push_review(date_str, plan_items, summary_review, summary_reflect, summary_insight, tomorrow, extra_blocks=None):
    """
    date_str: "2026-02-23"
    plan_items: ["002调校", "闲鱼开号", ...]
    summary_review: "今天做得最好的事"
    summary_reflect: "最需要改进的事"
    summary_insight: "最重要的收获"
    tomorrow: "002调校完成"
    extra_blocks: optional list of additional blocks
    """
    blocks = []
    
    # 总目标
    blocks.append(heading2("总目标"))
    blocks.append(quote("打造能提效的 AI 实用产品与个人 IP，帮助中小企业通过 AI 提效，尤其是围绕「AI 工作流 / 智能体」落地场景。"))
    blocks.append(divider())
    
    # 今日计划
    blocks.append(heading2("今日计划"))
    for i, item in enumerate(plan_items[:3], 1):
        blocks.append(bullet(f"{item}"))
    blocks.append(divider())
    
    # 今日总结
    blocks.append(heading2("今日总结"))
    blocks.append(bullet(f"复盘：{summary_review}"))
    blocks.append(bullet(f"反省：{summary_reflect}"))
    blocks.append(bullet(f"思考：{summary_insight}"))
    blocks.append(divider())
    
    # 明日计划
    blocks.append(heading2("明日计划（最重要的1件事）"))
    blocks.append(paragraph(f"👉 {tomorrow}", bold=True))
    
    if extra_blocks:
        blocks.extend(extra_blocks)
    
    title = f"{date_str} 每日复盘"
    
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "名称": {"title": [{"text": {"content": title}}]},
            "日期": {"date": {"start": date_str}},
            "作者": {"rich_text": [{"text": {"content": "零零壹"}}]},
            "标签 个人成长": {"rich_text": [{"text": {"content": "日结复盘"}}]}
        },
        "children": blocks
    }
    
    r = requests.post(
        "https://api.notion.com/v1/pages",
        headers={
            "Authorization": f"Bearer {NOTION_KEY}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        },
        json=data
    )
    result = r.json()
    if result.get("id"):
        print(f"✅ 推送成功: {result['url']}")
    else:
        print(f"❌ 推送失败: {result.get('message', result)}")
    return result

if __name__ == "__main__":
    # 可以命令行调用测试
    # python3 notion-review-push.py
    gmt8 = timezone(timedelta(hours=8))
    today = datetime.now(gmt8).strftime("%Y-%m-%d")
    
    push_review(
        date_str=today,
        plan_items=["测试项1", "测试项2"],
        summary_review="测试复盘内容",
        summary_reflect="测试反省内容",
        summary_insight="测试思考内容",
        tomorrow="测试明日计划"
    )
