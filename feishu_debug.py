import requests, json

APP_ID = "cli_a908765086b85bc6"
APP_SECRET = "4HZ5OiOueIU1PYCy59T48fpYvomTWELl"
DOC_TOKEN = "Gy8mdZqtboDgVkxjgPlcDCXznTe"
BASE = "https://open.feishu.cn"

r = requests.post(f"{BASE}/open-apis/auth/v3/tenant_access_token/internal", json={"app_id": APP_ID, "app_secret": APP_SECRET})
token = r.json()["tenant_access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Get current blocks to see existing format
r = requests.get(f"{BASE}/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks?page_size=500", headers=headers)
blocks = r.json()["data"]["items"]
for b in blocks[:10]:
    print(json.dumps(b, indent=2, ensure_ascii=False))
    print("---")

# Try creating heading with "heading1" key instead of "text"
print("\n\nTrying heading with heading2 key:")
test = {
    "children": [
        {
            "block_type": 4,
            "heading2": {
                "elements": [
                    {"text_run": {"content": "Test Heading", "text_element_style": {}}}
                ],
                "style": {}
            }
        }
    ],
    "index": -1
}
r = requests.post(f"{BASE}/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks/{DOC_TOKEN}/children", headers=headers, json=test)
print(json.dumps(r.json(), indent=2, ensure_ascii=False))
