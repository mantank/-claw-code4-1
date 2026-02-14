import requests, json

NOTION_KEY = "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"
H = {"Authorization": f"Bearer {NOTION_KEY}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}
DB_ID = "307453f1-8074-8125-8906-cb5156b3383a"

# Update DB title and description
r = requests.patch(f"https://api.notion.com/v1/databases/{DB_ID}", headers=H, json={
    "title": [{"type": "text", "text": {"content": "\U0001f916 AI\u65e5\u62a5 | \u6df1\u591c\u5f00\u53d1\u8005\u6bcf\u65e5\u7cbe\u9009"}}],
    "description": [{"type": "text", "text": {"content": "\u6bcf\u5929\u65e9\u4e0a6\u70b9\u81ea\u52a8\u66f4\u65b0\uff0cAI\u884c\u4e1a\u6700\u65b0\u52a8\u6001\u4e00\u7f51\u6253\u5c3d"}}],
    "properties": {
        "\u7c7b\u578b": {
            "select": {
                "options": [
                    {"name": "\U0001f525 \u70ed\u70b9\u65b0\u95fb", "color": "red"},
                    {"name": "\U0001f4e6 \u5f00\u6e90\u9879\u76ee", "color": "green"},
                    {"name": "\U0001f3e2 \u5927\u6a21\u578b\u52a8\u6001", "color": "blue"},
                    {"name": "\U0001f6e0\ufe0f \u5de5\u5177\u63a8\u8350", "color": "orange"},
                    {"name": "\U0001f4ca \u884c\u4e1a\u62a5\u544a", "color": "purple"}
                ]
            }
        },
        "\u91cd\u8981\u5ea6": {
            "select": {
                "options": [
                    {"name": "\u2b50\u2b50\u2b50 \u5fc5\u8bfb", "color": "red"},
                    {"name": "\u2b50\u2b50 \u63a8\u8350", "color": "yellow"},
                    {"name": "\u2b50 \u4e86\u89e3", "color": "gray"}
                ]
            }
        }
    }
})
print(f"Update DB: {r.status_code}")

# Create today's page
today_page = {
    "parent": {"database_id": DB_ID},
    "icon": {"type": "emoji", "emoji": "\U0001f4cb"},
    "properties": {
        "\u65e5\u671f": {"title": [{"text": {"content": "2026-02-14 \u5468\u516d | AI\u65e5\u62a5"}}]},
        "\u6765\u6e90\u6807\u7b7e": {"multi_select": [
            {"name": "GitHub"},
            {"name": "\u5a92\u4f53/\u535a\u5ba2"},
            {"name": "\u5b98\u65b9\u53d1\u5e03"},
            {"name": "\u884c\u4e1a\u52a8\u6001"}
        ]},
        "\u7c7b\u578b": {"select": {"name": "\U0001f525 \u70ed\u70b9\u65b0\u95fb"}},
        "\u91cd\u8981\u5ea6": {"select": {"name": "\u2b50\u2b50\u2b50 \u5fc5\u8bfb"}}
    }
}

r2 = requests.post("https://api.notion.com/v1/pages", headers=H, json=today_page)
res2 = r2.json()
page_id = res2["id"]
print(f"Page: {res2.get('url','')}")

# Helper functions
def rt(text, bold=False, italic=False, color="default"):
    return {"type": "text", "text": {"content": text}, "annotations": {"bold": bold, "italic": italic, "strikethrough": False, "underline": False, "code": False, "color": color}}

def p(elements): return {"object":"block","type":"paragraph","paragraph":{"rich_text": elements}}
def h1(t): return {"object":"block","type":"heading_1","heading_1":{"rich_text":[rt(t)]}}
def h2(t): return {"object":"block","type":"heading_2","heading_2":{"rich_text":[rt(t)]}}
def nl(elements): return {"object":"block","type":"numbered_list_item","numbered_list_item":{"rich_text": elements}}
def bl(elements): return {"object":"block","type":"bulleted_list_item","bulleted_list_item":{"rich_text": elements}}
def div(): return {"object":"block","type":"divider","divider":{}}
def callout(text, emoji, color="blue_background"):
    return {"object":"block","type":"callout","callout":{"rich_text":[rt(text)],"icon":{"type":"emoji","emoji":emoji},"color":color}}
def quote(elements):
    return {"object":"block","type":"quote","quote":{"rich_text": elements}}

blocks = [
    # Header
    callout("\u5feb\u901f\u626b\u5b8c\u8fd9 5 \u6761\u5c31\u591f\u4e86\uff0c\u6df1\u5ea6\u5185\u5bb9\u5c55\u5f00\u770b\u3002\u6bcf\u5929\u65e9\u4e0a 6 \u70b9\u81ea\u52a8\u66f4\u65b0\u3002", "\u26a1", "blue_background"),
    p([rt("\U0001f527 \u96f6\u96f6\u58f9 | 2026\u5e742\u670814\u65e5 \u5468\u516d", italic=True, color="gray")]),
    div(),

    # TOP 5
    h1("\U0001f525 \u4eca\u65e5\u5fc5\u8bfb TOP 5"),

    nl([rt("\u5b57\u8282\u8df3\u52a8\u81ea\u7814AI\u82af\u7247\uff0c\u627e\u4e09\u661f\u4ee3\u5de5", bold=True)]),
    p([rt("\u4ee3\u53f7SeedChip\uff0c\u5e74\u4ea710\u4e07\u9897\u8d77\uff0c2026 AI\u9884\u7b971600\u4ebfRMB\u3002\u4e2d\u56fd\u79d1\u6280\u5de8\u5934\u7684\u201c\u53bbNvidia\u5316\u201d\u52a0\u901f\u3002", color="gray")]),
    p([rt("\U0001f517 reuters.com", color="blue")]),

    nl([rt("Claude Opus 4.6 \u767b\u9876AI\u667a\u80fd\u6307\u6570\u699c\u9996", bold=True)]),
    p([rt("Agent\u4efb\u52a1\u548c\u7f16\u7a0b\u5168\u9762\u9886\u5148\uff0c\u4f60\u73b0\u5728\u7528\u7684\u5c31\u662f\u8fd9\u4e2a\u6a21\u578b\u3002\u4f46token\u6d88\u8017\u7ea6\u4e3aOpus 4.5\u76842\u500d\u3002", color="gray")]),
    p([rt("\U0001f517 the-decoder.com", color="blue")]),

    nl([rt("20+\u4e2aClaude Code Agent\u534f\u540c\u5de5\u4f5c\uff08\u5f00\u6e90\uff09", bold=True)]),
    p([rt("\u591aAgent\u7f16\u6392\u6846\u67b6\uff0c\u89e3\u51b3\u5355Agent\u4f1a\u5361\u6b7b/\u5faa\u73af\u7684\u95ee\u9898\u3002\u548c\u4f60\u7684\u201c\u591aAI\u5458\u5de5\u201d\u613f\u666f\u5b8c\u5168\u543b\u5408\u3002", color="gray")]),
    p([rt("\U0001f517 news.ycombinator.com", color="blue")]),

    nl([rt("GitHub\u535a\u5ba2\uff1aAI\u6b63\u5728\u91cd\u5851\u8f6f\u4ef6\u6784\u5efa\u65b9\u5f0f", bold=True)]),
    p([rt("Python\u4ece\u7b14\u8bb0\u672c\u8d70\u5411\u751f\u4ea7\u7ea7AI\u7cfb\u7edf\uff0c2026\u8d8b\u52bf\u786e\u8ba4\u3002", color="gray")]),
    p([rt("\U0001f517 github.blog", color="blue")]),

    nl([rt("\u53f0\u6e7e\u56e0AI\u9700\u6c42\u4e0a\u8c03GDP\u589e\u957f\u9884\u6d4b\u81f37.7%", bold=True)]),
    p([rt("AI\u82af\u7247\u9700\u6c42\u76f4\u63a5\u62c9\u52a8\u6574\u4e2a\u7ecf\u6d4e\u4f53\uff0cTSMC\u7ee7\u7eed\u6269\u4ea7\u3002", color="gray")]),
    p([rt("\U0001f517 reuters.com", color="blue")]),

    div(),

    # Open Source
    h1("\U0001f4e6 \u5f00\u6e90\u9879\u76ee\u63a8\u8350"),

    callout("claude-mem \u2014 AI Agent\u8bb0\u5fc6\u57fa\u7840\u8bbe\u65bd\n\u8fde\u7eed3\u5929GitHub Trending\u52a0\u901f\u589e\u957f\uff0c\u5b9e\u73b0\u4e86Agent\u8bb0\u5fc6\u7684\u4ea7\u54c1\u5e02\u573a\u5339\u914d\u3002\u548cOpenClaw\u7684memory\u7cfb\u7edf\u601d\u8def\u4e00\u81f4\u3002", "\u2b50", "yellow_background"),
    callout("\u591aAgent\u7f16\u6392\u6846\u67b6\n20+\u4e2aClaude Code Agent\u534f\u540c\u5de5\u4f5c\uff0c\u5f00\u6e90\u3002\u591aAgent\u534f\u4f5c\u662f2026\u5173\u952e\u8d8b\u52bf\u3002", "\u2b50", "yellow_background"),

    div(),

    # Company Updates
    h1("\U0001f3e2 \u5927\u6a21\u578b\u5b98\u65b9\u52a8\u6001"),

    bl([rt("Anthropic", bold=True), rt(" \u2014 Opus 4.6 \u767b\u9876Intelligence Index\uff0cAgent+\u7f16\u7a0b\u5168\u9762\u9886\u5148")]),
    bl([rt("OpenAI", bold=True), rt(" \u2014 GPT-5.3 Codex \u4e3b\u653b\u7f16\u7a0b\uff0c\u53ef\u80fd\u5728coding\u4e0a\u53cd\u8d85Opus 4.6")]),
    bl([rt("\u5b57\u8282\u8df3\u52a8", bold=True), rt(" \u2014 SeedChip\u81ea\u7814AI\u82af\u7247+\u4e09\u661f\u4ee3\u5de5\uff0c2026\u5e74AI\u9884\u7b971600\u4ebf")]),
    bl([rt("Nvidia", bold=True), rt(" \u2014 Q4\u8d22\u62a52/25\u53d1\u5e03\uff0cJensen\u5b9a\u4e492026\u4e3aPhysical AI\u5143\u5e74")]),

    div(),

    # Summary
    h1("\U0001f4ca \u4eca\u65e5\u603b\u7ed3"),

    quote([rt("\u4e09\u4e2a\u5173\u952e\u4fe1\u53f7\uff1a", bold=True)]),
    bl([rt("\u2460 AI\u7ade\u8d5b\u8fdb\u5165\u201c27\u5206\u949f\u7ea7\u201d\u54cd\u5e94\u901f\u5ea6 \u2014 Anthropic\u548cOpenAI\u540c\u65e5\u53d1\u6a21\u578b\u4e0d\u662f\u5de7\u5408")]),
    bl([rt("\u2461 \u4ece\u5b9e\u9a8c\u5230\u751f\u4ea7\u7684\u8f6c\u6298\u70b9 \u2014 Agent\u4e0d\u518d\u662fdemo\uff0c\u800c\u662f\u771f\u6b63\u80fd\u8dd1\u5b8c\u6574\u5de5\u4f5c\u6d41")]),
    bl([rt("\u2462 \u4e2d\u56fd\u7684\u201c\u53bbNvidia\u5316\u201d\u4e0d\u662f\u53e3\u53f7 \u2014 \u5b57\u82821600\u4ebf\u9884\u7b97+\u81ea\u7814\u82af\u7247")]),

    p([]),
    callout("\u5bf9\u4f60\u6700\u76f4\u63a5\u7684\u542f\u793a\uff1a\u4f60\u73b0\u5728\u7684\u201c\u591aAI\u5458\u5de5\u201d\u8def\u7ebf\u5b8c\u5168\u8e29\u5728\u8d8b\u52bf\u4e0a\u3002\u7ee7\u7eed\u5e72\u3002", "\U0001f4a1", "green_background"),
]

r3 = requests.patch(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=H, json={"children": blocks})
print(f"Blocks: {r3.status_code}")
if r3.status_code != 200:
    print(r3.text[:300])
else:
    print("Done!")
