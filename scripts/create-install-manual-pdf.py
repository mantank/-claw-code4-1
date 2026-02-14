#!/usr/bin/env python3
"""Generate OpenClaw安装手册 PDF - 引流钩子物料"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, ListFlowable, ListItem, Preformatted
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Use CID font for Chinese support
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

CN_FONT = "STSong-Light"
CN_FONT_BOLD = "STSong-Light"
print(f"Using font: {CN_FONT}")

# Colors
PRIMARY = HexColor("#1a1a2e")
ACCENT = HexColor("#0f3460")
HIGHLIGHT = HexColor("#e94560")
LIGHT_BG = HexColor("#f5f5f5")
CODE_BG = HexColor("#2d2d2d")
BLUE_LINK = HexColor("#16537e")

WIDTH, HEIGHT = A4

# Styles
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    "CoverTitle", fontName=CN_FONT, fontSize=28, leading=36,
    textColor=white, alignment=TA_CENTER, spaceAfter=10
)
style_subtitle = ParagraphStyle(
    "CoverSub", fontName=CN_FONT, fontSize=14, leading=20,
    textColor=HexColor("#cccccc"), alignment=TA_CENTER
)
style_h1 = ParagraphStyle(
    "H1", fontName=CN_FONT, fontSize=20, leading=28,
    textColor=PRIMARY, spaceBefore=20, spaceAfter=12
)
style_h2 = ParagraphStyle(
    "H2", fontName=CN_FONT, fontSize=15, leading=22,
    textColor=ACCENT, spaceBefore=16, spaceAfter=8
)
style_body = ParagraphStyle(
    "Body", fontName=CN_FONT, fontSize=10.5, leading=18,
    textColor=black, alignment=TA_JUSTIFY, spaceAfter=6
)
style_tip = ParagraphStyle(
    "Tip", fontName=CN_FONT, fontSize=10, leading=16,
    textColor=HexColor("#444444"), leftIndent=15, spaceAfter=8,
    backColor=HexColor("#fff3cd"), borderPadding=8
)
style_warning = ParagraphStyle(
    "Warning", fontName=CN_FONT, fontSize=10, leading=16,
    textColor=HexColor("#721c24"), leftIndent=15, spaceAfter=8,
    backColor=HexColor("#f8d7da"), borderPadding=8
)
style_code = ParagraphStyle(
    "Code", fontName="Courier", fontSize=9, leading=14,
    textColor=HexColor("#d4d4d4"), backColor=CODE_BG,
    leftIndent=10, rightIndent=10, spaceBefore=4, spaceAfter=8,
    borderPadding=8
)
style_bullet = ParagraphStyle(
    "Bullet", fontName=CN_FONT, fontSize=10.5, leading=18,
    textColor=black, leftIndent=20, bulletIndent=8, spaceAfter=4
)
style_footer_text = ParagraphStyle(
    "Footer", fontName=CN_FONT, fontSize=8, leading=12,
    textColor=HexColor("#999999"), alignment=TA_CENTER
)
style_toc = ParagraphStyle(
    "TOC", fontName=CN_FONT, fontSize=12, leading=22,
    textColor=ACCENT, leftIndent=20, spaceAfter=4
)

def make_cover(story):
    """Cover page"""
    story.append(Spacer(1, 80*mm))
    story.append(Paragraph("OpenClaw", style_title))
    story.append(Spacer(1, 5*mm))
    
    title2 = ParagraphStyle("T2", parent=style_title, fontSize=22, leading=30)
    story.append(Paragraph("零基础安装手册", title2))
    story.append(Spacer(1, 15*mm))
    story.append(Paragraph("从零开始，30分钟搞定你的AI私人助手", style_subtitle))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("适用人群：完全不会写代码的普通人", style_subtitle))
    story.append(Spacer(1, 30*mm))
    
    info = ParagraphStyle("Info", parent=style_subtitle, fontSize=10)
    story.append(Paragraph("深夜开发者LND | 2026年2月", info))
    story.append(Paragraph("版本 v1.0", info))
    story.append(PageBreak())

def make_toc(story):
    """Table of contents"""
    story.append(Paragraph("目录", style_h1))
    story.append(Spacer(1, 5*mm))
    
    toc_items = [
        "一、OpenClaw是什么？为什么要装？",
        "二、准备工作清单",
        "三、第一步：买服务器",
        "四、第二步：装Node.js和Git",
        "五、第三步：装OpenClaw",
        "六、第四步：配置AI模型和Telegram",
        "七、第五步：配对你的手机",
        "八、常用命令速查表",
        "九、踩坑指南（我替你踩过的坑）",
        "十、下一步：装技能让它更强"
    ]
    for item in toc_items:
        story.append(Paragraph(item, style_toc))
    
    story.append(PageBreak())

def p(text):
    return Paragraph(text, style_body)

def h1(text):
    return Paragraph(text, style_h1)

def h2(text):
    return Paragraph(text, style_h2)

def code(text):
    return Paragraph(f"<font face='Courier' color='#d4d4d4'>{text}</font>", style_code)

def tip(text):
    return Paragraph(f"💡 {text}", style_tip)

def warn(text):
    return Paragraph(f"⚠️ {text}", style_warning)

def bullet(text):
    return Paragraph(f"• {text}", style_bullet)

def make_content(story):
    # Section 1
    story.append(h1("一、OpenClaw是什么？为什么要装？"))
    story.append(p("简单说：装好OpenClaw，你就有了一个<b>24小时在线</b>的AI私人助手。"))
    story.append(p("它是一个开源框架，能把Claude、GPT这些AI大模型接到你的Telegram、WhatsApp上。不用开网页，手机上随时跟AI聊。"))
    story.append(Spacer(1, 3*mm))
    story.append(p("<b>装了之后能干什么？</b>"))
    story.append(bullet("随时随地跟AI对话（手机、电脑都行）"))
    story.append(bullet("让AI帮你写文章、整理笔记、分析数据"))
    story.append(bullet("装各种技能插件，让AI帮你管飞书、读邮件、生成图片"))
    story.append(bullet("设置定时任务，AI自动帮你抓新闻、发日报"))
    story.append(bullet("24小时不关机，随叫随到"))
    story.append(Spacer(1, 5*mm))
    
    # Section 2
    story.append(h1("二、准备工作清单"))
    story.append(p("开始之前，你需要准备这四样东西："))
    story.append(Spacer(1, 3*mm))
    
    checklist = [
        ["准备项", "怎么获取", "预计耗时"],
        ["Linux服务器", "腾讯云/阿里云，最便宜的就行", "10分钟"],
        ["Anthropic API Key", "console.anthropic.com 注册", "5分钟"],
        ["Telegram账号", "手机装Telegram App", "2分钟"],
        ["Telegram Bot Token", "找 @BotFather 创建机器人", "3分钟"],
    ]
    t = Table(checklist, colWidths=[100, 220, 80])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), CN_FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 3*mm))
    story.append(tip("费用：服务器约30-50元/月，API按量付费（日常使用每月约几十元）"))
    story.append(Spacer(1, 5*mm))
    
    # Section 3
    story.append(h1("三、第一步：买服务器"))
    story.append(p("推荐腾讯云或阿里云，选最便宜的Linux服务器就够了。"))
    story.append(p("<b>配置要求：</b>"))
    story.append(bullet("系统：CentOS / Ubuntu / Debian 都行"))
    story.append(bullet("配置：1核1G内存起步（够用了）"))
    story.append(bullet("带宽：1Mbps就行"))
    story.append(Spacer(1, 3*mm))
    story.append(p("买好之后，用SSH登录到服务器。推荐工具："))
    story.append(bullet("Windows：MobaXterm（免费，好用）"))
    story.append(bullet("Mac：自带终端就行"))
    story.append(bullet("手机：Termux / JuiceSSH"))
    story.append(Spacer(1, 3*mm))
    story.append(tip("不知道怎么SSH？搜「腾讯云 SSH 登录教程」跟着做就行，5分钟的事"))
    story.append(Spacer(1, 5*mm))
    
    # Section 4
    story.append(h1("四、第二步：装Node.js和Git"))
    story.append(p("OpenClaw跑在Node.js上，所以得先装。"))
    story.append(Spacer(1, 3*mm))
    story.append(h2("方法一：用nvm安装（推荐）"))
    story.append(code("curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash"))
    story.append(code("source ~/.bashrc"))
    story.append(code("nvm install --lts"))
    story.append(Spacer(1, 3*mm))
    story.append(h2("方法二：用系统包管理器"))
    story.append(p("CentOS / OpenCloudOS："))
    story.append(code("dnf install -y nodejs npm git"))
    story.append(p("Ubuntu / Debian："))
    story.append(code("apt update &amp;&amp; apt install -y nodejs npm git"))
    story.append(Spacer(1, 3*mm))
    story.append(p("验证安装成功："))
    story.append(code("node -v    # 应该显示 v18 以上<br/>git --version"))
    story.append(Spacer(1, 3*mm))
    story.append(warn("如果 node -v 显示版本低于18，用nvm重新装一个LTS版本"))
    story.append(Spacer(1, 5*mm))
    
    # Section 5
    story.append(h1("五、第三步：装OpenClaw"))
    story.append(p("一行命令搞定："))
    story.append(code("npm install -g openclaw@latest"))
    story.append(Spacer(1, 3*mm))
    story.append(p("中间会有一堆黄色的deprecated警告，<b>别管它</b>，看到「added XXX packages」就是成功了。"))
    story.append(Spacer(1, 3*mm))
    story.append(p("验证："))
    story.append(code("openclaw --version"))
    story.append(tip("如果报command not found，退出终端重新登录一次"))
    story.append(Spacer(1, 5*mm))
    
    # Section 6
    story.append(h1("六、第四步：配置AI模型和Telegram"))
    story.append(p("运行配置向导："))
    story.append(code("openclaw onboard"))
    story.append(Spacer(1, 3*mm))
    story.append(p("会弹出交互式菜单，按提示填四个东西："))
    story.append(Spacer(1, 2*mm))
    story.append(bullet("<b>模型和API Key</b> — 选Claude模型，填Anthropic的Key"))
    story.append(bullet("<b>Telegram Bot Token</b> — BotFather给你的那串token"))
    story.append(bullet("<b>你的Telegram ID</b> — 用 @userinfobot 查"))
    story.append(bullet("<b>工作目录</b> — 默认就行，直接回车"))
    story.append(Spacer(1, 3*mm))
    
    story.append(h2("模型怎么选？"))
    model_table = [
        ["模型", "价格（输入/输出）", "建议"],
        ["Sonnet 4.5", "$3 / $15", "新手首选，性价比高"],
        ["Opus 4.5", "$5 / $25", "旗舰级，能力最强"],
        ["Haiku 3.5", "$0.8 / $4", "最便宜，简单任务够用"],
    ]
    t2 = Table(model_table, colWidths=[100, 130, 170])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), CN_FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t2)
    story.append(Spacer(1, 3*mm))
    story.append(tip("建议先用Sonnet 4.5跑通流程，确认没问题再换Opus"))
    story.append(Spacer(1, 3*mm))
    
    story.append(p("配置完启动服务："))
    story.append(code("openclaw gateway start"))
    story.append(Spacer(1, 5*mm))
    
    # Section 7
    story.append(h1("七、第五步：配对你的手机"))
    story.append(p("打开Telegram，找到你刚创建的Bot，发一条消息（随便打个「你好」）。"))
    story.append(Spacer(1, 3*mm))
    story.append(p("Bot会回复一串配对码，类似："))
    story.append(code("Pairing code: KW39NZUZ"))
    story.append(Spacer(1, 3*mm))
    story.append(p("回到服务器，运行："))
    story.append(code("openclaw pairing approve telegram KW39NZUZ"))
    story.append(Spacer(1, 3*mm))
    story.append(p("搞定！现在你可以在Telegram上正常跟AI对话了。🎉"))
    story.append(Spacer(1, 3*mm))
    story.append(tip("Telegram默认英文界面？点这个链接一键换中文：t.me/setlanguage/zh-hans-raw"))
    story.append(Spacer(1, 5*mm))
    
    # Section 8
    story.append(h1("八、常用命令速查表"))
    cmd_table = [
        ["命令", "用途"],
        ["openclaw status", "查看运行状态"],
        ["openclaw gateway start", "启动服务"],
        ["openclaw gateway restart", "重启服务"],
        ["openclaw gateway stop", "停止服务"],
        ["openclaw logs --follow", "实时查看日志"],
        ["openclaw doctor", "出问题时先跑这个诊断"],
        ["npm update -g openclaw", "更新到最新版"],
    ]
    t3 = Table(cmd_table, colWidths=[180, 220])
    t3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, -1), CN_FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#dddddd")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("FONTNAME", (0, 1), (0, -1), "Courier"),
    ]))
    story.append(t3)
    story.append(Spacer(1, 5*mm))
    
    # Section 9
    story.append(h1("九、踩坑指南"))
    story.append(p("这些坑我替你踩过了，照着避开就行："))
    story.append(Spacer(1, 3*mm))
    
    story.append(h2("坑1：API Key 404报错"))
    story.append(p("配好之后发消息，回了个HTTP 404。先用curl测试Key是否正常："))
    story.append(code("curl -X POST https://api.anthropic.com/v1/messages \\<br/>  -H \"x-api-key: 你的KEY\" \\<br/>  -H \"content-type: application/json\" \\<br/>  -H \"anthropic-version: 2023-06-01\" \\<br/>  -d '{\"model\":\"claude-sonnet-4-5-20250929\",\"max_tokens\":100,\"messages\":[{\"role\":\"user\",\"content\":\"hello\"}]}'"))
    story.append(p("返回authentication_error就是Key有问题，去重新生成一个。"))
    story.append(Spacer(1, 3*mm))
    
    story.append(h2("坑2：Node.js版本太低"))
    story.append(p("OpenClaw需要Node.js 18以上。如果系统自带的版本太低："))
    story.append(code("nvm install --lts<br/>nvm use --lts"))
    story.append(Spacer(1, 3*mm))
    
    story.append(h2("坑3：npm报错找不到git"))
    story.append(p("装OpenClaw时报 npm error path git，就是没装git："))
    story.append(code("dnf install -y git  # 或 apt install -y git"))
    story.append(Spacer(1, 3*mm))
    
    story.append(h2("坑4：服务器重启后Bot不回消息"))
    story.append(p("OpenClaw服务需要手动启动。设置开机自启："))
    story.append(code("openclaw gateway start  # 先手动启动<br/># 设置systemd自启（可选）"))
    story.append(Spacer(1, 5*mm))
    
    # Section 10
    story.append(h1("十、下一步：装技能让它更强"))
    story.append(p("OpenClaw装好了只是起点。通过安装Skills（技能插件），它能做更多事："))
    story.append(Spacer(1, 3*mm))
    story.append(bullet("天气查询 — 随时问天气"))
    story.append(bullet("网页搜索 — 帮你搜信息、读网页"))
    story.append(bullet("PDF处理 — 读PDF、合并拆分"))
    story.append(bullet("飞书集成 — 帮你管文档、发消息"))
    story.append(bullet("定时任务 — 每天自动帮你做事"))
    story.append(Spacer(1, 3*mm))
    story.append(p("关注「<b>深夜开发者LND</b>」公众号，后续会出Skills安装教程和更多实战玩法。"))
    story.append(Spacer(1, 8*mm))
    
    # Footer section
    story.append(Paragraph("—— 完 ——", ParagraphStyle("End", parent=style_body, alignment=TA_CENTER, fontSize=12, textColor=HexColor("#999999"))))
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph("本手册由「深夜开发者LND」出品", ParagraphStyle("Brand", parent=style_body, alignment=TA_CENTER, fontSize=10, textColor=ACCENT)))
    story.append(Paragraph("一个人 + AI，也能改变世界。", ParagraphStyle("Slogan", parent=style_body, alignment=TA_CENTER, fontSize=10, textColor=HexColor("#999999"))))

def on_page(canvas, doc):
    """Add page number footer"""
    canvas.saveState()
    canvas.setFont(CN_FONT, 8)
    canvas.setFillColor(HexColor("#999999"))
    canvas.drawCentredString(WIDTH/2, 15*mm, f"— {doc.page} —")
    canvas.drawRightString(WIDTH - 20*mm, 15*mm, "深夜开发者LND")
    canvas.restoreState()

def on_cover(canvas, doc):
    """Cover page background"""
    canvas.saveState()
    canvas.setFillColor(PRIMARY)
    canvas.rect(0, 0, WIDTH, HEIGHT, fill=1)
    # Decorative line
    canvas.setStrokeColor(HIGHLIGHT)
    canvas.setLineWidth(3)
    canvas.line(WIDTH/2 - 60*mm, HEIGHT - 95*mm, WIDTH/2 + 60*mm, HEIGHT - 95*mm)
    canvas.restoreState()

# Build PDF
output_path = "/root/.openclaw/workspace/assets/OpenClaw安装手册-深夜开发者LND.pdf"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=20*mm,
    rightMargin=20*mm,
    topMargin=20*mm,
    bottomMargin=25*mm,
    title="OpenClaw零基础安装手册",
    author="深夜开发者LND"
)

story = []
make_cover(story)
make_toc(story)
make_content(story)

# Use different templates for cover vs content
doc.build(story, onFirstPage=on_cover, onLaterPages=on_page)
print(f"PDF generated: {output_path}")
print(f"Size: {os.path.getsize(output_path) / 1024:.1f} KB")
