import requests
import json
import time

APP_ID = "cli_a908765086b85bc6"
APP_SECRET = "4HZ5OiOueIU1PYCy59T48fpYvomTWELl"
DOC_TOKEN = "Gy8mdZqtboDgVkxjgPlcDCXznTe"
BASE = "https://open.feishu.cn"

r = requests.post(f"{BASE}/open-apis/auth/v3/tenant_access_token/internal", json={"app_id": APP_ID, "app_secret": APP_SECRET})
token = r.json()["tenant_access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# First delete the test block and any existing content
r = requests.get(f"{BASE}/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks?page_size=500", headers=headers)
blocks = r.json()["data"]["items"]
child_count = len(blocks) - 1
if child_count > 0:
    r = requests.delete(
        f"{BASE}/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks/{DOC_TOKEN}/children/batch_delete",
        headers=headers,
        json={"start_index": 0, "end_index": child_count}
    )
    print(f"Deleted {child_count} blocks: {r.json().get('code')}")

def te(content, bold=False):
    style = {"bold": bold} if bold else {}
    return {"text_run": {"content": content, "text_element_style": style}}

def txt(*elements):
    return {"block_type": 2, "text": {"elements": list(elements), "style": {}}}

def h1(t): return {"block_type": 3, "text": {"elements": [te(t)], "style": {}}}
def h2(t): return {"block_type": 4, "text": {"elements": [te(t)], "style": {}}}
def h3(t): return {"block_type": 5, "text": {"elements": [te(t)], "style": {}}}
def div(): return {"block_type": 14, "divider": {}}

# New homepage design
all_blocks = [
    h1("🚀 OPENA知识库"),
    txt(te("一个人 + AI，也能改变世界。", bold=True)),
    txt(te("专注 AI 工具实战，帮你从小白到超级个体。非程序员视角，真实经验，拿来即用。")),
    txt(te("")),
    div(),
    h2("📂 核心板块"),
    txt(te("")),
    h3("🔧 OpenClaw 实战"),
    txt(te("从零部署到高级玩法，最完整的中文 OpenClaw 教程。")),
    txt(te("")),
    h3("🤖 AI 工具教程"),
    txt(te("Claude Code、Cursor、Kimi……主流 AI 工具的上手指南与深度技巧。")),
    txt(te("")),
    h3("✍️ 内容创作方法论"),
    txt(te("用 AI 做内容、做 IP，从写作到分发的完整方法论。")),
    txt(te("")),
    h3("🌱 超级个体成长"),
    txt(te("非程序员如何借助 AI 打造个人商业系统，一个人活成一支队伍。")),
    txt(te("")),
    div(),
    h2("⭐ 推荐阅读"),
    txt(te("• Claude Code 10个隐藏技巧")),
    txt(te("• 云端部署 OpenClaw 保姆级教程")),
    txt(te("• OpenClaw + Kimi 2.5 部署教程")),
    txt(te("")),
    div(),
    h2("📢 最新动态"),
    txt(te("2月6日", bold=True), te(" — OpenClaw 专区 MVP 正式上线")),
    txt(te("2月5日", bold=True), te(" — Claude Code 完全指南整理中")),
    txt(te("1月31日", bold=True), te(" — 知识库创建，开始系统整理")),
    txt(te("")),
    div(),
    h2("💬 关于"),
    txt(te("我是旭，一个非程序员出身的 AI 探索者。")),
    txt(te("这个知识库记录我用 AI 工具创业、创作、成长的全过程。")),
    txt(te("如果你也想用 AI 放大自己，欢迎一起。")),
]

# Send in batches of 5
for i in range(0, len(all_blocks), 5):
    batch = all_blocks[i:i+5]
    r = requests.post(
        f"{BASE}/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks/{DOC_TOKEN}/children",
        headers=headers,
        json={"children": batch, "index": -1}
    )
    resp = r.json()
    code = resp.get('code')
    if code != 0:
        print(f"Batch {i//5} FAILED: {json.dumps(resp, indent=2, ensure_ascii=False)}")
        # Try one by one for this batch
        for j, block in enumerate(batch):
            r2 = requests.post(
                f"{BASE}/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks/{DOC_TOKEN}/children",
                headers=headers,
                json={"children": [block], "index": -1}
            )
            r2j = r2.json()
            if r2j.get('code') != 0:
                print(f"  Block {i+j} type={block['block_type']} FAILED: {r2j.get('msg')}")
                print(f"  {json.dumps(block, ensure_ascii=False)}")
            else:
                print(f"  Block {i+j} OK")
            time.sleep(0.2)
    else:
        print(f"Batch {i//5} OK ({len(batch)} blocks)")
    time.sleep(0.3)

print("\n✅ Done!")
