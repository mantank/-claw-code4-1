import requests, json, time, sys

APP_ID = "cli_a908765086b85bc6"
APP_SECRET = "4HZ5OiOueIU1PYCy59T48fpYvomTWELl"

r = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    json={"app_id": APP_ID, "app_secret": APP_SECRET})
TOKEN = r.json()["tenant_access_token"]
H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

DOC = "RhlidyP0EoNLosxjC44cyCCwn0m"
URL = f"https://open.feishu.cn/open-apis/docx/v1/documents/{DOC}/blocks/{DOC}/children?document_revision_id=-1"

def text_el(content, bold=False, italic=False):
    style = {}
    if bold: style["bold"] = True
    if italic: style["italic"] = True
    return {"text_run": {"content": content, "text_element_style": style}}

def text_block(elements):
    return {"block_type": 2, "text": {"elements": elements, "style": {}}}

def heading(level, content):
    key = f"heading{level}"
    return {"block_type": 2 + level, key: {"elements": [text_el(content)], "style": {}}}

def bullet(elements):
    return {"block_type": 12, "bullet": {"elements": elements, "style": {}}}

def ordered(elements):
    return {"block_type": 13, "ordered": {"elements": elements, "style": {}}}

def divider():
    return {"block_type": 22, "divider": {}}

def callout(emoji="💡"):
    return {"block_type": 19, "callout": {"background_color": 2, "border_color": 2, "emoji_id": emoji}}

def send(blocks):
    for i in range(0, len(blocks), 50):
        batch = blocks[i:i+50]
        r = requests.post(URL, headers=H, json={"children": batch})
        if r.status_code != 200 or r.json().get("code") != 0:
            print(f"Error at batch {i}: {r.text[:200]}")
            return False
        time.sleep(0.3)
    return True

# Build all blocks
blocks = []

# Intro
blocks.append(text_block([text_el("每个工具都经过实测，不需要翻墙，注册就能用。", bold=True)]))
blocks.append(text_block([text_el("作者：深夜开发者LND | 更新时间：2026年2月", italic=True)]))
blocks.append(divider())

# === Section 1 ===
blocks.append(heading(1, "一、AI对话助手 — 有问题先问它们"))

for name, desc, who, cost, stars, tip, warn in [
    ("豆包（字节跳动）", "日常问答、写文案、翻译、头脑风暴", "所有人，尤其是刚接触AI的新手", "免费，额度很大", "⭐⭐⭐⭐⭐",
     "装手机App，随时随地用。回答质量在国产里属于第一梯队，中文理解很好", "偶尔会编造信息，重要内容需要二次验证"),
    ("Kimi（月之暗面）", "长文档分析、论文阅读、网页总结", "需要处理大量文字的人（学生、文案、运营）", "免费版够用，Pro版按需", "⭐⭐⭐⭐⭐",
     "杀手锏是超长上下文，丢一整本PDF进去让它总结，效果炸裂", "免费版有每日次数限制，重度使用建议升级"),
    ("通义千问（阿里）", "写作、代码、数据分析、多模态（看图说话）", "需要多功能AI的用户", "免费额度非常大方", "⭐⭐⭐⭐",
     "阿里生态集成好，如果你用钉钉/阿里云，体验更顺。图片理解能力不错", "创意写作能力略弱于豆包和Kimi"),
    ("元宝（腾讯）", "微信生态内的AI助手，搜索+对话+公众号内容理解", "微信重度用户", "免费", "⭐⭐⭐⭐",
     "直接在微信里用，不用额外装App。适合快速查资料、总结公众号文章", "能力上限不如豆包和Kimi，胜在方便"),
    ("DeepSeek", "深度推理、复杂问题分析、代码能力强", "对AI输出质量要求高的用户", "免费", "⭐⭐⭐⭐⭐",
     "推理能力是国产模型里最强的之一，复杂问题优先用它", "高峰期可能排队，官网有时不稳定"),
]:
    blocks.append(heading(3, name))
    blocks.append(bullet([text_el("干嘛用的：", bold=True), text_el(desc)]))
    blocks.append(bullet([text_el("适合谁：", bold=True), text_el(who)]))
    blocks.append(bullet([text_el("费用：", bold=True), text_el(cost)]))
    blocks.append(bullet([text_el("推荐指数：", bold=True), text_el(stars)]))
    blocks.append(bullet([text_el("使用建议：", bold=True), text_el(tip)]))
    blocks.append(bullet([text_el("⚠️ 踩坑提醒：", bold=True), text_el(warn)]))

blocks.append(divider())

# === Section 2 ===
blocks.append(heading(1, "二、AI图片生成 — 不会PS也能出图"))

for name, desc, who, cost, stars, tip, warn in [
    ("即梦AI（字节跳动）", "文字生成图片、AI写真、海报设计", "自媒体、电商、需要配图的所有人", "免费额度充足", "⭐⭐⭐⭐⭐",
     "中文提示词理解最好的国产图片工具，说人话就能出好图。做封面、小红书配图首选", "生成人物偶尔会有AI味，多试几次"),
    ("通义万相（阿里）", "图片生成、图片编辑、AI换背景", "需要简单图片编辑的用户", "免费", "⭐⭐⭐⭐",
     "除了生图，还能改图（换背景、去水印、扩图），实用性很强", "艺术风格不如即梦丰富"),
    ("Canva可画", "模板化设计+AI辅助，做海报、PPT、社交媒体图", "设计小白、运营、自媒体", "免费版够基础使用", "⭐⭐⭐⭐",
     "不是纯AI工具，但AI功能在模板基础上锦上添花。做统一风格的系列图效率极高", "中文模板数量不如英文多"),
]:
    blocks.append(heading(3, name))
    blocks.append(bullet([text_el("干嘛用的：", bold=True), text_el(desc)]))
    blocks.append(bullet([text_el("适合谁：", bold=True), text_el(who)]))
    blocks.append(bullet([text_el("费用：", bold=True), text_el(cost)]))
    blocks.append(bullet([text_el("推荐指数：", bold=True), text_el(stars)]))
    blocks.append(bullet([text_el("使用建议：", bold=True), text_el(tip)]))
    blocks.append(bullet([text_el("⚠️ 踩坑提醒：", bold=True), text_el(warn)]))

blocks.append(divider())

# === Section 3 ===
blocks.append(heading(1, "三、AI视频 — 从0到成片"))

for name, desc, who, cost, stars, tip, warn in [
    ("即梦视频（字节跳动）", "文字/图片生成视频、AI动画", "短视频创作者、自媒体", "免费体验，按量计费", "⭐⭐⭐⭐",
     "国内AI视频生成效果最好的之一，适合做短视频素材", "生成时间较长，商用需注意版权"),
    ("剪映（字节跳动）", "视频剪辑+AI字幕+AI脚本+数字人", "所有做视频的人", "基础功能免费", "⭐⭐⭐⭐⭐",
     "AI自动加字幕、AI写脚本、AI数字人三个功能能帮你省80%时间", "数字人效果还不够自然，适合做讲解类视频"),
]:
    blocks.append(heading(3, name))
    blocks.append(bullet([text_el("干嘛用的：", bold=True), text_el(desc)]))
    blocks.append(bullet([text_el("适合谁：", bold=True), text_el(who)]))
    blocks.append(bullet([text_el("费用：", bold=True), text_el(cost)]))
    blocks.append(bullet([text_el("推荐指数：", bold=True), text_el(stars)]))
    blocks.append(bullet([text_el("使用建议：", bold=True), text_el(tip)]))
    blocks.append(bullet([text_el("⚠️ 踩坑提醒：", bold=True), text_el(warn)]))

blocks.append(divider())

# === Section 4 ===
blocks.append(heading(1, "四、AI办公提效 — 打工人必备"))

for name, desc, who, cost, stars, tip, warn in [
    ("飞书智能伙伴", "文档AI总结、表格AI分析、会议纪要自动生成", "用飞书办公的团队和个人", "飞书用户免费", "⭐⭐⭐⭐",
     "开会录音后自动出纪要+待办事项，太香了。写文档时可以让AI帮你扩写、缩写、改语气", "需要在飞书生态内使用"),
    ("WPS AI", "Word/Excel/PPT的AI助手", "日常用WPS办公的人", "WPS会员内置", "⭐⭐⭐⭐",
     "Excel公式不会写？让AI写。PPT不会排版？让AI排。直接在你熟悉的环境里用AI", "需要WPS会员，免费版AI功能有限"),
    ("钉钉AI助理", "企业办公AI化，消息总结、日程管理、审批辅助", "用钉钉的企业用户", "基础功能免费", "⭐⭐⭐⭐",
     "群消息太多看不过来？让AI帮你总结重点。适合管理者和项目负责人", "生态绑定强"),
]:
    blocks.append(heading(3, name))
    blocks.append(bullet([text_el("干嘛用的：", bold=True), text_el(desc)]))
    blocks.append(bullet([text_el("适合谁：", bold=True), text_el(who)]))
    blocks.append(bullet([text_el("费用：", bold=True), text_el(cost)]))
    blocks.append(bullet([text_el("推荐指数：", bold=True), text_el(stars)]))
    blocks.append(bullet([text_el("使用建议：", bold=True), text_el(tip)]))
    blocks.append(bullet([text_el("⚠️ 踩坑提醒：", bold=True), text_el(warn)]))

blocks.append(divider())

# === Section 5 ===
blocks.append(heading(1, "五、AI编程/建站 — 不写代码也能做产品"))

for name, desc, who, cost, stars, tip, warn in [
    ("Cursor", "AI辅助写代码的编辑器，对话式编程", "想学编程的新手、独立开发者", "免费版每月有额度，Pro版$20/月", "⭐⭐⭐⭐⭐",
     "不需要会编程！用中文描述你想要什么功能，它帮你写代码", "需要翻墙下载，安装后国内可用。零基础需配合教程"),
    ("即时设计AI", "AI生成UI设计稿、设计转代码", "想做App/网站但不会设计的人", "免费", "⭐⭐⭐",
     "描述你想要的页面，AI帮你出设计稿，还能导出代码", "AI生成的设计需要手动调整"),
]:
    blocks.append(heading(3, name))
    blocks.append(bullet([text_el("干嘛用的：", bold=True), text_el(desc)]))
    blocks.append(bullet([text_el("适合谁：", bold=True), text_el(who)]))
    blocks.append(bullet([text_el("费用：", bold=True), text_el(cost)]))
    blocks.append(bullet([text_el("推荐指数：", bold=True), text_el(stars)]))
    blocks.append(bullet([text_el("使用建议：", bold=True), text_el(tip)]))
    blocks.append(bullet([text_el("⚠️ 踩坑提醒：", bold=True), text_el(warn)]))

blocks.append(divider())

# === Section 6 ===
blocks.append(heading(1, "六、AI搜索 — 比百度好用100倍"))

for name, desc, who, cost, stars, tip, warn in [
    ("秘塔AI搜索", "AI驱动的搜索引擎，直接给答案而不是链接", "所有人，替代百度的最佳选择", "免费", "⭐⭐⭐⭐⭐",
     "搜任何问题，直接出结构化答案+信息来源。做调研、查资料效率提升10倍", "偶尔信息不够新，时效性强的内容建议交叉验证"),
    ("天工AI搜索（昆仑万维）", "AI搜索+对话，支持多模态", "需要搜索+对话二合一的用户", "免费", "⭐⭐⭐⭐",
     "和秘塔类似但多了对话能力，可以追问细节", "搜索结果质量略不如秘塔稳定"),
]:
    blocks.append(heading(3, name))
    blocks.append(bullet([text_el("干嘛用的：", bold=True), text_el(desc)]))
    blocks.append(bullet([text_el("适合谁：", bold=True), text_el(who)]))
    blocks.append(bullet([text_el("费用：", bold=True), text_el(cost)]))
    blocks.append(bullet([text_el("推荐指数：", bold=True), text_el(stars)]))
    blocks.append(bullet([text_el("使用建议：", bold=True), text_el(tip)]))
    blocks.append(bullet([text_el("⚠️ 踩坑提醒：", bold=True), text_el(warn)]))

blocks.append(divider())

# === Section 7 ===
blocks.append(heading(1, "七、AI学习资源 — 持续进阶"))

blocks.append(heading(3, "公众号「深夜开发者LND」"))
blocks.append(bullet([text_el("保姆级AI实操教程，非程序员视角，每篇都是真实踩坑记录")]))
blocks.append(heading(3, "通往AGI之路（waytoagi.com）"))
blocks.append(bullet([text_el("AI知识体系化学习路线图，适合想系统了解AI全貌的入门者")]))

blocks.append(divider())

# === Quick pick table (as text since table blocks are complex) ===
blocks.append(heading(1, "怎么选？速查表"))
blocks.append(bullet([text_el("日常问答写文案 → ", bold=True), text_el("豆包（备选：Kimi、DeepSeek）")]))
blocks.append(bullet([text_el("读长文档/论文 → ", bold=True), text_el("Kimi（备选：通义千问）")]))
blocks.append(bullet([text_el("复杂问题深度分析 → ", bold=True), text_el("DeepSeek（备选：通义千问）")]))
blocks.append(bullet([text_el("做图做封面 → ", bold=True), text_el("即梦AI（备选：通义万相）")]))
blocks.append(bullet([text_el("剪视频 → ", bold=True), text_el("剪映")]))
blocks.append(bullet([text_el("办公提效 → ", bold=True), text_el("飞书/WPS/钉钉（看你用哪个）")]))
blocks.append(bullet([text_el("搜索查资料 → ", bold=True), text_el("秘塔AI搜索")]))
blocks.append(bullet([text_el("学编程做产品 → ", bold=True), text_el("Cursor")]))

blocks.append(divider())
blocks.append(text_block([text_el("最后更新：2026年2月14日", italic=True)]))
blocks.append(text_block([text_el("作者：深夜开发者LND — 不会写代码的普通人，用AI搭出了一人公司", italic=True)]))

print(f"Total blocks: {len(blocks)}")
ok = send(blocks)
print("Done!" if ok else "Failed!")
