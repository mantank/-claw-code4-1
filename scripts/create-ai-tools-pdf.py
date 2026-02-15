#!/usr/bin/env python3
"""Generate AI工具清单 PDF"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import os

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
CN = "STSong-Light"

# Colors
PRIMARY = HexColor("#1a1a2e")
ACCENT = HexColor("#0f3460")
HIGHLIGHT = HexColor("#e94560")
LIGHT_BG = HexColor("#f5f5f5")
CATEGORY_COLORS = {
    "对话助手": HexColor("#2196F3"),
    "图片生成": HexColor("#9C27B0"),
    "视频": HexColor("#FF5722"),
    "办公提效": HexColor("#4CAF50"),
    "编程/建站": HexColor("#FF9800"),
    "AI搜索": HexColor("#00BCD4"),
    "学习资源": HexColor("#795548"),
}

WIDTH, HEIGHT = A4

# Styles
s_cover_title = ParagraphStyle("CT", fontName=CN, fontSize=30, leading=40, textColor=white, alignment=TA_CENTER)
s_cover_sub = ParagraphStyle("CS", fontName=CN, fontSize=14, leading=22, textColor=HexColor("#cccccc"), alignment=TA_CENTER)
s_h1 = ParagraphStyle("H1", fontName=CN, fontSize=20, leading=28, textColor=PRIMARY, spaceBefore=24, spaceAfter=12)
s_h2 = ParagraphStyle("H2", fontName=CN, fontSize=14, leading=22, textColor=ACCENT, spaceBefore=16, spaceAfter=6)
s_body = ParagraphStyle("B", fontName=CN, fontSize=10.5, leading=18, textColor=black, alignment=TA_JUSTIFY, spaceAfter=4)
s_bullet = ParagraphStyle("BL", fontName=CN, fontSize=10, leading=17, textColor=black, leftIndent=15, spaceAfter=3)
s_tool_name = ParagraphStyle("TN", fontName=CN, fontSize=13, leading=20, textColor=HIGHLIGHT, spaceBefore=14, spaceAfter=6)
s_tip = ParagraphStyle("TIP", fontName=CN, fontSize=9.5, leading=16, textColor=HexColor("#444"), leftIndent=12, spaceAfter=6, backColor=HexColor("#fff3cd"), borderPadding=6)
s_warn = ParagraphStyle("WARN", fontName=CN, fontSize=9.5, leading=16, textColor=HexColor("#721c24"), leftIndent=12, spaceAfter=6, backColor=HexColor("#f8d7da"), borderPadding=6)
s_toc = ParagraphStyle("TOC", fontName=CN, fontSize=12, leading=24, textColor=ACCENT, leftIndent=20, spaceAfter=2)
s_footer = ParagraphStyle("FT", fontName=CN, fontSize=10, leading=16, textColor=HexColor("#999"), alignment=TA_CENTER)

# Data
tools_data = [
    {
        "category": "一、AI对话助手 — 有问题先问它们",
        "cat_key": "对话助手",
        "tools": [
            {"name": "豆包（字节跳动）", "用途": "日常问答、写文案、翻译、头脑风暴",
             "适合谁": "所有人，尤其是刚接触AI的新手。写周报总结、起活动名称、给客户写回复邮件、翻译英文文档",
             "费用": "免费，额度很大", "推荐指数": "⭐⭐⭐⭐⭐",
             "使用建议": "装手机App，随时随地用。回答质量在国产里属于第一梯队，中文理解很好",
             "踩坑提醒": "偶尔会编造信息，重要内容需要二次验证"},
            {"name": "Kimi（月之暗面）", "用途": "长文档分析、论文阅读、网页总结",
             "适合谁": "需要处理大量文字的人。把50页PDF合同丢进去找关键条款、读行业报告出摘要",
             "费用": "免费版够用，Pro版按需", "推荐指数": "⭐⭐⭐⭐⭐",
             "使用建议": "杀手锏是超长上下文，丢一整本PDF进去让它总结，效果炸裂",
             "踩坑提醒": "免费版有每日次数限制，重度使用建议升级"},
            {"name": "通义千问（阿里）", "用途": "写作、代码、数据分析、多模态（看图说话）",
             "适合谁": "需要多功能AI的用户。拍图表让AI分析数据、写Python脚本处理Excel",
             "费用": "免费额度非常大方", "推荐指数": "⭐⭐⭐⭐",
             "使用建议": "阿里生态集成好，图片理解能力不错",
             "踩坑提醒": "创意写作能力略弱于豆包和Kimi"},
            {"name": "元宝（腾讯）", "用途": "微信生态内的AI助手，搜索+对话+公众号内容理解",
             "适合谁": "微信重度用户。公众号长文不想读、微信里快速查资料",
             "费用": "免费", "推荐指数": "⭐⭐⭐⭐",
             "使用建议": "直接在微信里用，不用额外装App。适合快速查资料",
             "踩坑提醒": "能力上限不如豆包和Kimi，胜在方便"},
            {"name": "DeepSeek", "用途": "深度推理、复杂问题分析、代码能力强",
             "适合谁": "对AI输出质量要求高的用户。分析商业方案可行性、写自动化脚本",
             "费用": "免费", "推荐指数": "⭐⭐⭐⭐⭐",
             "使用建议": "推理能力是国产模型里最强的之一，复杂问题优先用它",
             "踩坑提醒": "高峰期可能排队，官网有时不稳定"},
        ]
    },
    {
        "category": "二、AI图片生成 — 不会PS也能出图",
        "cat_key": "图片生成",
        "tools": [
            {"name": "即梦AI（字节跳动）", "用途": "文字生成图片、AI写真、海报设计",
             "适合谁": "自媒体、电商、需要配图的所有人。公众号封面图、小红书配图、电商产品展示图",
             "费用": "免费额度充足", "推荐指数": "⭐⭐⭐⭐⭐",
             "使用建议": "中文提示词理解最好的国产图片工具，说人话就能出好图",
             "踩坑提醒": "生成人物偶尔会有AI味，多试几次"},
            {"name": "通义万相（阿里）", "用途": "图片生成、图片编辑、AI换背景",
             "适合谁": "需要简单图片编辑的用户。产品图换白底/场景背景、去水印、图片扩展",
             "费用": "免费", "推荐指数": "⭐⭐⭐⭐",
             "使用建议": "除了生图还能改图，实用性很强",
             "踩坑提醒": "艺术风格不如即梦丰富"},
            {"name": "Canva可画", "用途": "模板化设计+AI辅助，做海报、PPT、社交媒体图",
             "适合谁": "设计小白、运营、自媒体。做系列统一风格的小红书图、快速出一套PPT",
             "费用": "免费版够基础使用", "推荐指数": "⭐⭐⭐⭐",
             "使用建议": "不是纯AI工具，但AI功能在模板基础上锦上添花。做统一风格的系列图效率极高",
             "踩坑提醒": "中文模板数量不如英文多"},
        ]
    },
    {
        "category": "三、AI视频 — 从0到成片",
        "cat_key": "视频",
        "tools": [
            {"name": "即梦视频（字节跳动）", "用途": "文字/图片生成视频、AI动画",
             "适合谁": "短视频创作者、自媒体。把产品图变成动态展示视频、生成创意开场动画",
             "费用": "免费体验，按量计费", "推荐指数": "⭐⭐⭐⭐",
             "使用建议": "国内AI视频生成效果最好的之一",
             "踩坑提醒": "生成时间较长，商用需注意版权"},
            {"name": "剪映（字节跳动）", "用途": "视频剪辑+AI字幕+AI脚本+数字人",
             "适合谁": "所有做视频的人。录课程视频自动加字幕、文案自动生成视频脚本、数字人做产品讲解",
             "费用": "基础功能免费，AI功能部分付费", "推荐指数": "⭐⭐⭐⭐⭐",
             "使用建议": "AI自动加字幕、AI写脚本、AI数字人三个功能能帮你省80%时间",
             "踩坑提醒": "数字人效果还不够自然，适合做讲解类视频"},
        ]
    },
    {
        "category": "四、AI办公提效 — 打工人必备",
        "cat_key": "办公提效",
        "tools": [
            {"name": "飞书智能伙伴", "用途": "文档AI总结、表格AI分析、会议纪要自动生成",
             "适合谁": "用飞书办公的团队和个人。开完会自动出纪要+待办事项、文档缩写摘要",
             "费用": "飞书用户免费", "推荐指数": "⭐⭐⭐⭐",
             "使用建议": "开会录音后自动出纪要+待办事项，太香了",
             "踩坑提醒": "需要在飞书生态内使用"},
            {"name": "WPS AI", "用途": "Word/Excel/PPT的AI助手",
             "适合谁": "日常用WPS办公的人。Excel公式不会写让AI帮你写、PPT让AI排版美化",
             "费用": "WPS会员内置", "推荐指数": "⭐⭐⭐⭐",
             "使用建议": "直接在你熟悉的环境里用AI，学习成本几乎为零",
             "踩坑提醒": "需要WPS会员，免费版AI功能有限"},
            {"name": "钉钉AI助理", "用途": "企业办公AI化，消息总结、日程管理、审批辅助",
             "适合谁": "用钉钉的企业用户。群消息200+条让AI总结重点、排会议找空闲时间",
             "费用": "基础功能免费", "推荐指数": "⭐⭐⭐⭐",
             "使用建议": "群消息总结功能对管理者和项目负责人特别有用",
             "踩坑提醒": "生态绑定强"},
        ]
    },
    {
        "category": "五、AI编程/建站 — 不写代码也能做产品",
        "cat_key": "编程/建站",
        "tools": [
            {"name": "Cursor", "用途": "AI辅助写代码的编辑器，对话式编程",
             "适合谁": "想学编程的新手、独立开发者。用中文描述功能它帮你写代码、做个人网站",
             "费用": "免费版每月有额度，Pro版$20/月", "推荐指数": "⭐⭐⭐⭐⭐",
             "使用建议": "不需要会编程！用中文描述你想要什么功能，它帮你写",
             "踩坑提醒": "需要翻墙下载，安装后国内可用。零基础需配合教程"},
            {"name": "即时设计AI", "用途": "AI生成UI设计稿、设计转代码",
             "适合谁": "想做App/网站但不会设计的人。描述页面效果，AI出设计稿并导出前端代码",
             "费用": "免费", "推荐指数": "⭐⭐⭐",
             "使用建议": "适合原型验证，快速看到效果图",
             "踩坑提醒": "AI生成的设计需要手动调整"},
        ]
    },
    {
        "category": "六、AI搜索 — 比百度好用100倍",
        "cat_key": "AI搜索",
        "tools": [
            {"name": "秘塔AI搜索", "用途": "AI驱动的搜索引擎，直接给答案而不是链接",
             "适合谁": "所有人，替代百度的最佳选择。搜行业报告直接出摘要、做竞品调研一搜就有结构化报告",
             "费用": "免费", "推荐指数": "⭐⭐⭐⭐⭐",
             "使用建议": "搜任何问题，直接出结构化答案+信息来源。做调研效率提升10倍",
             "踩坑提醒": "偶尔信息不够新，时效性强的内容建议交叉验证"},
            {"name": "天工AI搜索（昆仑万维）", "用途": "AI搜索+对话，支持多模态",
             "适合谁": "需要搜索+对话二合一的用户。搜完结果后继续追问细节",
             "费用": "免费", "推荐指数": "⭐⭐⭐⭐",
             "使用建议": "和秘塔类似但多了对话能力，可以追问细节",
             "踩坑提醒": "搜索结果质量略不如秘塔稳定"},
        ]
    },
]

quick_ref = [
    ("日常问答写文案", "豆包（备选：Kimi、DeepSeek）"),
    ("读长文档/论文", "Kimi（备选：通义千问）"),
    ("复杂问题深度分析", "DeepSeek（备选：通义千问）"),
    ("做图做封面", "即梦AI（备选：通义万相）"),
    ("剪视频", "剪映"),
    ("办公提效", "飞书/WPS/钉钉（看你用哪个）"),
    ("搜索查资料", "秘塔AI搜索"),
    ("学编程做产品", "Cursor"),
]

def build_pdf():
    output = "/root/.openclaw/workspace/assets/AI工具清单-深夜开发者LND.pdf"
    os.makedirs(os.path.dirname(output), exist_ok=True)

    doc = SimpleDocTemplate(output, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm, topMargin=20*mm, bottomMargin=25*mm,
        title="2026年普通人AI工具清单", author="深夜开发者LND")

    story = []

    # === Cover ===
    story.append(Spacer(1, 60*mm))
    story.append(Paragraph("2026年", ParagraphStyle("Y", fontName=CN, fontSize=18, leading=24, textColor=HexColor("#e94560"), alignment=TA_CENTER)))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("普通人AI工具清单", s_cover_title))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("国内可用版 v2", ParagraphStyle("V", fontName=CN, fontSize=16, leading=22, textColor=HexColor("#aaaaaa"), alignment=TA_CENTER)))
    story.append(Spacer(1, 15*mm))
    story.append(Paragraph("每个工具都经过实测，不需要翻墙，注册就能用", s_cover_sub))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("6大类别 · 18款工具 · 真实踩坑记录", s_cover_sub))
    story.append(Spacer(1, 40*mm))
    info = ParagraphStyle("I", parent=s_cover_sub, fontSize=10)
    story.append(Paragraph("深夜开发者LND | 2026年2月", info))
    story.append(Paragraph("一个人 + AI，也能改变世界。", info))
    story.append(PageBreak())

    # === TOC ===
    story.append(Paragraph("目录", s_h1))
    story.append(Spacer(1, 5*mm))
    for cat in tools_data:
        story.append(Paragraph(cat["category"], s_toc))
        for tool in cat["tools"]:
            story.append(Paragraph(f"    · {tool['name']}", ParagraphStyle("TOCI", fontName=CN, fontSize=10, leading=18, textColor=HexColor("#666"), leftIndent=40)))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("速查表：怎么选？", s_toc))
    story.append(Paragraph("学习资源推荐", s_toc))
    story.append(PageBreak())

    # === Content ===
    for cat in tools_data:
        color = CATEGORY_COLORS.get(cat["cat_key"], ACCENT)
        story.append(Paragraph(cat["category"], ParagraphStyle("CH", fontName=CN, fontSize=20, leading=28, textColor=color, spaceBefore=10, spaceAfter=12)))

        # Decorative line
        line_data = [["",""]]
        line_table = Table(line_data, colWidths=[WIDTH - 40*mm, 0])
        line_table.setStyle(TableStyle([
            ("LINEABOVE", (0,0), (0,0), 2, color),
            ("TOPPADDING", (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ]))
        story.append(line_table)

        for tool in cat["tools"]:
            story.append(Paragraph(tool["name"], s_tool_name))

            # Info table
            fields = [
                ("用途", tool["用途"]),
                ("适合谁", tool["适合谁"]),
                ("费用", tool["费用"]),
                ("推荐指数", tool["推荐指数"]),
            ]
            tdata = [[Paragraph(f"<b>{k}</b>", ParagraphStyle("TK", fontName=CN, fontSize=9, leading=14, textColor=ACCENT)),
                       Paragraph(v, ParagraphStyle("TV", fontName=CN, fontSize=9.5, leading=15, textColor=black))]
                      for k, v in fields]
            t = Table(tdata, colWidths=[70, WIDTH - 110*mm])
            t.setStyle(TableStyle([
                ("VALIGN", (0,0), (-1,-1), "TOP"),
                ("TOPPADDING", (0,0), (-1,-1), 3),
                ("BOTTOMPADDING", (0,0), (-1,-1), 3),
                ("LEFTPADDING", (0,0), (0,-1), 8),
                ("BACKGROUND", (0,0), (-1,-1), HexColor("#fafafa")),
                ("BOX", (0,0), (-1,-1), 0.5, HexColor("#e0e0e0")),
                ("LINEBELOW", (0,0), (-1,-2), 0.3, HexColor("#eeeeee")),
            ]))
            story.append(t)
            story.append(Spacer(1, 3*mm))

            story.append(Paragraph(f"💡 使用建议：{tool['使用建议']}", s_tip))
            story.append(Paragraph(f"⚠ 踩坑提醒：{tool['踩坑提醒']}", s_warn))
            story.append(Spacer(1, 4*mm))

        story.append(Spacer(1, 6*mm))

    # === Quick reference ===
    story.append(PageBreak())
    story.append(Paragraph("速查表：怎么选？", s_h1))
    story.append(Spacer(1, 5*mm))
    qr_data = [
        [Paragraph("<b>需求场景</b>", ParagraphStyle("QH", fontName=CN, fontSize=10, textColor=white)),
         Paragraph("<b>推荐工具</b>", ParagraphStyle("QH2", fontName=CN, fontSize=10, textColor=white))]
    ] + [
        [Paragraph(s, ParagraphStyle("QR", fontName=CN, fontSize=10, leading=16)),
         Paragraph(t, ParagraphStyle("QR2", fontName=CN, fontSize=10, leading=16))]
        for s, t in quick_ref
    ]
    qt = Table(qr_data, colWidths=[150, WIDTH - 190*mm])
    qt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), ACCENT),
        ("TEXTCOLOR", (0,0), (-1,0), white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, LIGHT_BG]),
        ("GRID", (0,0), (-1,-1), 0.5, HexColor("#ddd")),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(qt)

    # === Learning resources ===
    story.append(Spacer(1, 15*mm))
    story.append(Paragraph("学习资源推荐", s_h1))
    story.append(Paragraph("公众号「深夜开发者LND」", s_tool_name))
    story.append(Paragraph("保姆级AI实操教程，非程序员视角，每篇都是真实踩坑记录", s_body))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("通往AGI之路（waytoagi.com）", s_tool_name))
    story.append(Paragraph("AI知识体系化学习路线图，适合想系统了解AI全貌的入门者", s_body))

    # === End ===
    story.append(Spacer(1, 20*mm))
    story.append(Paragraph("—— 完 ——", s_footer))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("本清单由「深夜开发者LND」出品", ParagraphStyle("BR", fontName=CN, fontSize=11, leading=18, textColor=ACCENT, alignment=TA_CENTER)))
    story.append(Paragraph("一个人 + AI，也能改变世界。", s_footer))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("最后更新：2026年2月14日", ParagraphStyle("DT", fontName=CN, fontSize=9, leading=14, textColor=HexColor("#bbb"), alignment=TA_CENTER)))

    def on_cover(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(PRIMARY)
        canvas.rect(0, 0, WIDTH, HEIGHT, fill=1)
        # Decorative lines
        canvas.setStrokeColor(HIGHLIGHT)
        canvas.setLineWidth(3)
        canvas.line(WIDTH/2 - 80*mm, HEIGHT - 80*mm, WIDTH/2 + 80*mm, HEIGHT - 80*mm)
        canvas.setLineWidth(1)
        canvas.line(WIDTH/2 - 40*mm, HEIGHT - 190*mm, WIDTH/2 + 40*mm, HEIGHT - 190*mm)
        canvas.restoreState()

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont(CN, 8)
        canvas.setFillColor(HexColor("#999"))
        canvas.drawCentredString(WIDTH/2, 15*mm, f"— {doc.page} —")
        canvas.drawRightString(WIDTH - 20*mm, 15*mm, "深夜开发者LND")
        # Top accent line
        canvas.setStrokeColor(HIGHLIGHT)
        canvas.setLineWidth(1.5)
        canvas.line(20*mm, HEIGHT - 12*mm, WIDTH - 20*mm, HEIGHT - 12*mm)
        canvas.restoreState()

    doc.build(story, onFirstPage=on_cover, onLaterPages=on_page)
    print(f"PDF generated: {output}")
    print(f"Size: {os.path.getsize(output) / 1024:.1f} KB")
    return output

if __name__ == "__main__":
    path = build_pdf()
    import shutil
    shutil.copy2(path, "/tmp/ai-tools-list.pdf")
    print("Copied to /tmp/ai-tools-list.pdf")
