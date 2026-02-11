import requests
import json

APP_ID = "cli_a908765086b85bc6"
APP_SECRET = "4HZ5OiOueIU1PYCy59T48fpYvomTWELl"
DOC_TOKEN = "Gy8mdZqtboDgVkxjgPlcDCXznTe"
BASE = "https://open.feishu.cn"

# 1. Get token
r = requests.post(f"{BASE}/open-apis/auth/v3/tenant_access_token/internal", json={"app_id": APP_ID, "app_secret": APP_SECRET})
token = r.json()["tenant_access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
print(f"Token obtained: {token[:20]}...")

# 2. Get all blocks
r = requests.get(f"{BASE}/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks?page_size=500", headers=headers)
data = r.json()
print(f"Get blocks response code: {data.get('code')}")
blocks = data.get("data", {}).get("items", [])
print(f"Total blocks: {len(blocks)}")

# Find document block and children to delete
doc_block_id = None
child_ids = []
for b in blocks:
    if b["block_type"] == 1:  # document
        doc_block_id = b["block_id"]
    else:
        child_ids.append(b["block_id"])

print(f"Document block: {doc_block_id}")
print(f"Children to delete: {len(child_ids)}")

# 3. Delete all children in batches
for i in range(0, len(child_ids), 50):
    batch = child_ids[i:i+50]
    r = requests.delete(
        f"{BASE}/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks/{doc_block_id}/children/batch_delete",
        headers=headers,
        json={"start_index": 0, "end_index": len(child_ids)}
    )
    print(f"Delete response: {r.json().get('code')} {r.json().get('msg')}")
    break  # one batch delete with index range

# Helper functions
def text_run(text, bold=False, link=None):
    style = {}
    if bold:
        style["bold"] = True
    if link:
        style["link"] = {"url": link}
    return {"text_run": {"content": text, "text_element_style": style}}

def text_block(elements):
    return {"block_type": 2, "text": {"style": {}, "elements": elements}}

def heading(level, text):
    # 3=h1, 4=h2, 5=h3
    return {"block_type": level, "text": {"style": {}, "elements": [text_run(text)]}}

def divider():
    return {"block_type": 14, "divider": {}}

# 4. Build new content
new_blocks = [
    # 愿景
    heading(3, "🚀 OPENA知识库"),
    text_block([text_run("一个人 + AI，也能改变世界。", bold=True)]),
    text_block([text_run("专注 AI 工具实战，帮你从小白到超级个体。非程序员视角，真实经验，拿来即用。")]),
    text_block([text_run("")]),
    
    divider(),
    
    # 核心板块
    heading(4, "📂 核心板块"),
    text_block([text_run("")]),
    heading(5, "🔧 OpenClaw 实战"),
    text_block([text_run("从零部署到高级玩法，最完整的中文 OpenClaw 教程。")]),
    text_block([text_run("")]),
    heading(5, "🤖 AI 工具教程"),
    text_block([text_run("Claude Code、Cursor、Kimi……主流 AI 工具的上手指南与深度技巧。")]),
    text_block([text_run("")]),
    heading(5, "✍️ 内容创作方法论"),
    text_block([text_run("用 AI 做内容、做 IP，从写作到分发的完整方法论。")]),
    text_block([text_run("")]),
    heading(5, "🌱 超级个体成长"),
    text_block([text_run("非程序员如何借助 AI 打造个人商业系统，一个人活成一支队伍。")]),
    text_block([text_run("")]),
    
    divider(),
    
    # 推荐阅读
    heading(4, "⭐ 推荐阅读"),
    text_block([text_run("• Claude Code 10个隐藏技巧")]),
    text_block([text_run("• 云端部署 OpenClaw 保姆级教程")]),
    text_block([text_run("• OpenClaw + Kimi 2.5 部署教程")]),
    text_block([text_run("")]),
    
    divider(),
    
    # 最新动态
    heading(4, "📢 最新动态"),
    text_block([text_run("2月6日", bold=True), text_run(" — OpenClaw 专区 MVP 正式上线")]),
    text_block([text_run("2月5日", bold=True), text_run(" — Claude Code 完全指南整理中")]),
    text_block([text_run("1月31日", bold=True), text_run(" — 知识库创建，开始系统整理")]),
    text_block([text_run("")]),
    
    divider(),
    
    # 关于
    heading(4, "💬 关于"),
    text_block([text_run("我是旭，一个非程序员出身的 AI 探索者。")]),
    text_block([text_run("这个知识库记录我用 AI 工具创业、创作、成长的全过程。")]),
    text_block([text_run("如果你也想用 AI 放大自己，欢迎一起。")]),
]

# 5. Write new blocks
r = requests.post(
    f"{BASE}/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks/{doc_block_id}/children",
    headers=headers,
    json={"children": new_blocks, "index": 0}
)
resp = r.json()
print(f"Create response: code={resp.get('code')} msg={resp.get('msg')}")
if resp.get('code') != 0:
    print(json.dumps(resp, indent=2, ensure_ascii=False))
else:
    print("✅ 首页重新设计完成！")
