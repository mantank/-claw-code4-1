import requests
import json

TOKEN = "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"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}
DB_ID = "bf0b46f5-90d9-4308-9e75-8c61c0a7b0e7"

def p(text, bold=False):
    """paragraph block"""
    rt = [{"type": "text", "text": {"content": text}}]
    if bold:
        rt[0]["annotations"] = {"bold": True}
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rt}}

def p_mixed(parts):
    """paragraph with mixed formatting. parts = [(text, bold), ...]"""
    rt = []
    for text, bold in parts:
        item = {"type": "text", "text": {"content": text}}
        if bold:
            item["annotations"] = {"bold": True}
        rt.append(item)
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": rt}}

def h1(text):
    return {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def h2(text):
    return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def h3(text):
    return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def bullet(text):
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

def callout(text, emoji="📷"):
    return {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": text}}], "icon": {"type": "emoji", "emoji": emoji}}}

def numbered(text):
    return {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]}}

# 文章内容
blocks_part1 = [
    h1("我让AI接管了我的知识库，它比我自己整理得还好"),
    divider(),

    # 第一段
    h2("一、你的知识库，是不是也长这样？"),
    p("你收藏过多少篇文章？"),
    p("微信收藏200多条，浏览器书签5个文件夹，Notion里建了3个数据库，聊天记录里还有一堆\u201c回头看\u201d的链接。"),
    p("加起来可能有500篇。"),
    p("但你真正用到过几篇？", bold=True),
    p("上周开会，老板问：\u201c上次你看的那篇竞品分析呢？\u201d你翻了5分钟微信收藏，又翻了3分钟浏览器书签，最后在Notion的某个角落找到了\u2014\u2014但格式乱七八糟，当时只是随手粘进去的，关键数据根本没标出来。"),
    p("这不是你不努力。你试过Notion、语雀、Obsidian，每次都信誓旦旦\u201c这次一定好好整理\u201d。"),
    p_mixed([("结局都一样：", False), ("用了三天，然后变成新的数字垃圾场。", True)]),
    p_mixed([("问题不是工具不好。问题是\u2014\u2014", False), ("你根本没时间整理。", True)]),
    p("白天上班，晚上还有一堆事要干。让你花2小时把这周看的文章分类、提炼、归档？算了吧。"),

    # 第二段
    divider(),
    h2("二、转折：我把这件事甩给了AI"),
    p("我有一个AI助手，叫零零壹。"),
    p("之前它已经能帮我写文章、每天早上发AI日报、管理我的待办清单。"),
    p_mixed([("但有一天我突然想到：", False), ("它最擅长的事情，其实是整理和归档。", True)]),
    p("AI不会累，不会偷懒，不会\u201c先收藏回头看\u201d。给它10篇文章，它真的会全部读完。"),
    p_mixed([("所以我做了一个决定：", False), ("让AI直接操作我的知识库。", True)]),
    p("不是让它\u201c建议\u201d我怎么整理\u2014\u2014是让它自己动手，读文章、提炼要点、分好类、放到该放的位置。"),
    p("我选了飞书知识库当阵地。原因很简单：免费、结构清晰、支持API（就是让AI能\u201c进去干活\u201d的接口）。"),
    p("接下来发生的事，让我彻底放弃了自己整理知识库这个念头。"),

    # 第三段
    divider(),
    h2("三、效果展示：10分钟 vs 4小时"),
    p("先看结果。"),
    p("我给了AI一个任务：\u201c帮我把这7篇AGI相关的长文全部读完，提炼核心观点，放进知识库。\u201d"),
    p_mixed([("这7篇文章加起来", False), ("14万字", True), ("。如果我自己读，按正常阅读速度，光是读完就要5-6个小时，还不算整理。", False)]),
    p("AI用了10分钟。", bold=True),
    p("它做了什么："),
    bullet("每篇文章提炼出3-5个核心观点"),
    bullet("自动按主题分类（技术路线、行业影响、风险争议）"),
    bullet("统一了格式（标题、摘要、原文链接、关键引用）"),
    bullet("全部归档到知识库对应板块"),
    callout("\U0001f4f8\u3010截图位置\u2460\u3011知识库整理后的效果\u2014\u2014分类清晰、摘要完整的页面"),
    p("然后我又说了一句：\u201c重新设计一下知识库首页。\u201d"),
    p("它直接改好了。分好板块，写好每个板块的简介，连排版都调好了。"),
    callout("\U0001f4f8\u3010截图位置\u2461\u3011知识库首页\u2014\u2014板块分明、简介完整"),
    p("如果这些事全部我自己来做，保守估计3-4个小时。而我只花了打两行字的时间。"),
]

blocks_part2 = [
    # 第四段 - 教程
    divider(),
    h2("四、完整教程：从零搭建你的AI知识库助手"),
    p("你不需要会编程。不需要买服务器。只需要一台能上网的电脑，大概20-30分钟。"),
    p_mixed([("核心思路就一句话：", False), ("让AI获得你知识库的\u201c编辑权限\u201d。", True)]),
    p("我用的是飞书知识库 + OpenClaw（开源AI助手平台）。下面是完整步骤。"),

    h3("第1步：注册飞书，创建知识库"),
    p("如果你还没有飞书账号，先注册一个（个人免费版就够用）。"),
    numbered("打开飞书，点击左侧\u300c知识库\u300d"),
    numbered("点击\u300c创建知识空间\u300d"),
    numbered("给你的知识库起个名字（比如\u201c我的AI知识库\u201d）"),
    numbered("创建完成"),
    callout("\U0001f4f8\u3010截图位置\u2462\u3011飞书创建知识空间的界面"),

    h3("第2步：创建飞书应用（让AI有\u201c钥匙\u201d进来）"),
    p("这一步是关键\u2014\u2014你需要在飞书开放平台创建一个\u201c应用\u201d，相当于给AI配一把钥匙。"),
    numbered("打开飞书开放平台（open.feishu.cn），用你的飞书账号登录"),
    numbered("点击\u300c创建企业自建应用\u300d"),
    numbered("填写应用名称（比如\u201cAI知识库助手\u201d），上传一个图标"),
    numbered("创建完成后，进入应用详情页"),
    numbered("在左侧菜单找到\u300c凭证与基础信息\u300d，记下 App ID 和 App Secret\u2014\u2014这就是AI的\u201c钥匙\u201d"),
    callout("\U0001f4f8\u3010截图位置\u2463\u3011飞书开放平台-创建应用界面"),
    callout("\U0001f4f8\u3010截图位置\u2464\u3011App ID 和 App Secret 的位置"),

    h3("第3步：给应用开通权限"),
    p("AI要能读写你的知识库，需要开通对应的权限。"),
    numbered("在应用详情页，左侧菜单找到\u300c权限管理\u300d"),
    numbered("搜索并开通以下权限：wiki:wiki（知识库读写）、docx:document（文档读写）、drive:drive（云空间读写）"),
    numbered("开通后需要发布应用版本，点击\u300c版本管理与发布\u300d\u2192\u300c创建版本\u300d\u2192 提交审核"),
    numbered("因为是自建应用，审核秒过"),
    callout("\U0001f4f8\u3010截图位置\u2465\u3011权限管理页面，搜索并开通权限"),
    callout("\U0001f4f8\u3010截图位置\u2466\u3011发布应用版本"),

    h3("第4步：把应用添加为知识库成员"),
    p("应用创建好了，但它还不是你知识库的\u201c成员\u201d，进不去。"),
    numbered("回到飞书，打开你刚创建的知识空间"),
    numbered("点击知识空间的\u300c设置\u300d\u2192\u300c成员管理\u300d"),
    numbered("添加成员，搜索你刚创建的应用名称"),
    numbered("权限选择\u300c管理员\u300d（这样AI才能创建和编辑页面）"),
    callout("\U0001f4f8\u3010截图位置\u2467\u3011知识空间添加应用为成员"),

    h3("第5步：连接AI助手"),
    p("现在AI有钥匙了，也有权限了。最后一步是让你的AI助手知道怎么用这把钥匙。"),
    p("如果你用的是OpenClaw（和我一样）："),
    numbered("把App ID和App Secret配置到OpenClaw的飞书插件里"),
    numbered("安装飞书相关的Skills（技能包）"),
    numbered("对AI说一句：\u201c帮我把这篇文章总结一下，放进知识库\u201d"),
    p("如果你用其他AI工具（比如Coze、Dify等）：核心逻辑一样，把飞书API的凭证配进去，让AI能调用飞书的接口。"),
    callout("\U0001f4f8\u3010截图位置\u2468\u3011OpenClaw配置飞书的界面"),

    h3("第6步：测试一下"),
    p("配置完成，来测试："),
    p("对AI说：\u201c帮我在知识库里创建一个页面，标题叫\u2018测试页面\u2019，内容写\u2018Hello World\u2019。\u201d"),
    p_mixed([("如果知识库里出现了这个页面\u2014\u2014", False), ("恭喜，你的AI知识库助手搭好了。", True)]),
    callout("\U0001f4f8\u3010截图位置\u2469\u3011测试成功的截图\u2014\u2014知识库里出现了AI创建的页面"),
]

blocks_part3 = [
    # 第五段
    divider(),
    h2("五、为什么AI整理得比你好？"),
    p("用了一周之后，我想明白了一件事："),
    p("AI整理知识库，不是比我\u201c快一点\u201d，是从根上比我强。", bold=True),
    p_mixed([("它不会偷懒。", True), ("14万字，它真的每个字都读了。你呢？你收藏的文章有多少是\u201c先存着回头看\u201d，然后再也没打开过？", False)]),
    p_mixed([("它有结构化思维。", True), ("同样一篇文章，你可能随手粘进去就完了。AI会自动提炼要点、分好层级、统一格式。每次都一样，不会今天用一种分类明天换一种。", False)]),
    p_mixed([("它不需要意志力。", True), ("整理知识库这件事，对人来说是\u201c重要但不紧急\u201d\u2014\u2014永远排在待办清单的最后面。但AI没有这个问题，你说干它就干，不需要先喝杯咖啡找找状态。", False)]),
    p_mixed([("它24小时在线。", True), ("我睡觉的时候它还在干活。早上醒来，昨晚让它整理的内容已经静静地躺在知识库里了。", False)]),
    p("这不是AI替代你思考\u2014\u2014是AI帮你把\u201c想做但没时间做\u201d的事做了。", bold=True),

    # 第六段
    divider(),
    h2("六、今晚就开始"),
    p("知识管理的终极形态，不是\u201c整理得更好\u201d。"),
    p("而是不需要你整理。", bold=True),
    p("当AI能直接操作你的知识库，你的工作流变成了："),
    bullet("看到好文章\u2192转给AI\u2192自动归档"),
    bullet("需要某个信息\u2192问AI\u2192它从知识库里找给你"),
    bullet("想要某个主题的综述\u2192AI从你积累的内容里自动生成"),
    p("从\u201c人找信息\u201d变成\u201c信息找人\u201d。", bold=True),
    p("这不是什么未来黑科技。这是我前天晚上花20分钟搭好的东西。"),
    p("今晚花20分钟，照着上面的步骤搭好。明天开始，你的知识库就自己长了。", bold=True),
    p("如果搭建过程中遇到问题，评论区告诉我，我帮你看。"),
    divider(),
    p("我是深夜开发者，一个非程序员出身、正在用AI重建工作流的普通人。关注我，一起探索普通人也能用好的AI。"),
]

# 创建页面（带第一批blocks）
page_data = {
    "parent": {"database_id": DB_ID},
    "properties": {
        "名称": {"title": [{"text": {"content": "【第6篇】我让AI接管了我的知识库，它比我自己整理得还好"}}]},
        "日期": {"date": {"start": "2026-02-12"}},
        "作者": {"rich_text": [{"text": {"content": "深夜开发者"}}]}
    },
    "children": blocks_part1
}

r = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=page_data)
d = r.json()
if "id" not in d:
    print(f"ERROR creating page: {d.get('message','')}")
    print(json.dumps(d, indent=2)[:1000])
    exit(1)

page_id = d["id"]
page_url = d["url"]
print(f"Page created: {page_id}")
print(f"URL: {page_url}")

# 追加第二批blocks
r2 = requests.patch(
    f"https://api.notion.com/v1/blocks/{page_id}/children",
    headers=HEADERS,
    json={"children": blocks_part2}
)
if r2.status_code == 200:
    print("Part 2 appended OK")
else:
    print(f"Part 2 error: {r2.json().get('message','')}")

# 追加第三批blocks
r3 = requests.patch(
    f"https://api.notion.com/v1/blocks/{page_id}/children",
    headers=HEADERS,
    json={"children": blocks_part3}
)
if r3.status_code == 200:
    print("Part 3 appended OK")
else:
    print(f"Part 3 error: {r3.json().get('message','')}")

print(f"\nDone! Open: {page_url}")
