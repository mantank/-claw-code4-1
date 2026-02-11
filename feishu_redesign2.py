import requests
import json

APP_ID = "cli_a908765086b85bc6"
APP_SECRET = "4HZ5OiOueIU1PYCy59T48fpYvomTWELl"
DOC_TOKEN = "Gy8mdZqtboDgVkxjgPlcDCXznTe"
BASE = "https://open.feishu.cn"

r = requests.post(f"{BASE}/open-apis/auth/v3/tenant_access_token/internal", json={"app_id": APP_ID, "app_secret": APP_SECRET})
token = r.json()["tenant_access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Try creating a single simple text block first to debug
test_block = {
    "children": [
        {
            "block_type": 2,
            "text": {
                "elements": [
                    {"text_run": {"content": "test", "text_element_style": {}}}
                ],
                "style": {}
            }
        }
    ],
    "index": 0
}

r = requests.post(
    f"{BASE}/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks/{DOC_TOKEN}/children",
    headers=headers,
    json=test_block
)
print(json.dumps(r.json(), indent=2, ensure_ascii=False))
