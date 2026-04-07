#!/usr/bin/env bash
set -euo pipefail

# 腾讯新闻 CLI AI 日报过滤器 v3
# 用途：拉取 ai-daily，筛出适合进入 AI 日报的“硬核”条目，并给出三级判定：
# 1) 入正文 2) 待核验 3) 仅候选池
# 依赖：@tencentnews/cli（可通过 npx 调用）
# 用法：
#   export TENCENT_NEWS_APIKEY=xxxx
#   bash scripts/tencent-news-ai-filter.sh

if [[ -z "${TENCENT_NEWS_APIKEY:-}" ]]; then
  echo "❌ 未设置 TENCENT_NEWS_APIKEY"
  echo "先执行：export TENCENT_NEWS_APIKEY=你的key"
  exit 1
fi

TMP_RAW="$(mktemp)"
trap 'rm -f "$TMP_RAW"' EXIT

npx --yes @tencentnews/cli@latest ai-daily > "$TMP_RAW"

python3 - "$TMP_RAW" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding='utf-8', errors='ignore')

update_match = re.search(r'更新时间[:：]\s*(.+)', text)
update_time = update_match.group(1).strip() if update_match else '未知'
headline_match = re.search(r'速览[:：]\s*(.+)', text)
headline = headline_match.group(1).strip() if headline_match else ''

pattern = re.compile(r"###\s*(\d+)\.\s*(.+?)\n(.*?)(?=\n###\s*\d+\.|\n---|\Z)", re.S)

MODEL_PRODUCT = ['模型', '大模型', 'gemma', 'deepseek', 'openai', 'meta', 'anthropic', 'google', 'claude', 'gpt', '发布', '上线', '开源', '新版本', '产品', '功能', '工具', '平台', 'sora']
INFRA = ['芯片', '算力', 'gpu', 'tpu', '服务器', '推理', '训练', '网络组件', '昇腾', '寒武纪', '供应协议', '数据中心']
POLICY = ['政策', '白皮书', '标准', '工作组', '监管', '法规', '治理', '安全', '伦理', '国家标准', '委员会']
AUTOMATION = ['办公', '工作流', '自动化', 'agent', '智能体', '效率', '协同', '助手', 'cli', 'api']
SOFT_DROP = ['烈士', '纪念', '照片', '影视班', '极端主义', '故事', '人物', '情感', '营销', '招生']
MARKET = ['etf', 'ipo', '融资', '估值', '股价', '涨幅', '财报', '投资者', '上市']
LEGAL = ['法律', '诉讼', '反竞争', '调查']
TIER1_MEDIA = ['新华社', '界面新闻', '财联社', '澎湃', '36氪', 'techcrunch', 'venturebeat', 'reuters', 'the information', 'google', 'openai', 'anthropic']
TIER2_MEDIA = ['鞭牛士', '环球tech', '环球网', 'it之家', '财闻', 'agihunt', '新民晚报', '南方都市报']


def has_any(s, words):
    s_lower = s.lower()
    return any(w.lower() in s_lower for w in words)


def count_hits(s, words):
    s_lower = s.lower()
    return sum(1 for w in words if w.lower() in s_lower)


def media_tier(source):
    s = source.lower()
    if any(x.lower() in s for x in TIER1_MEDIA):
        return 1
    if any(x.lower() in s for x in TIER2_MEDIA):
        return 2
    if source == '未知来源' or not source.strip():
        return 9
    return 3


def bucket_of(full):
    if has_any(full, POLICY):
        return '核心大事件'
    if has_any(full, INFRA):
        return '核心大事件'
    if has_any(full, MODEL_PRODUCT):
        return '核心大事件'
    if has_any(full, AUTOMATION):
        return '生产力与自动化应用'
    return '候选观察'


def classify(title, summary, source, url):
    full = f"{title}\n{summary}"
    tier = media_tier(source)
    hard_score = count_hits(full, MODEL_PRODUCT + INFRA + POLICY + AUTOMATION)
    soft_score = count_hits(full, SOFT_DROP)
    market_flag = has_any(full, MARKET)
    legal_flag = has_any(full, LEGAL)
    policy_flag = has_any(full, POLICY)
    model_flag = has_any(full, MODEL_PRODUCT)
    infra_flag = has_any(full, INFRA)
    automation_flag = has_any(full, AUTOMATION)
    unknown_source = (source == '未知来源' or not url)

    if soft_score > 0 and not (policy_flag or model_flag or infra_flag or automation_flag):
        return ('仅候选池', '候选观察', '泛社会/故事应用，不进正文')

    bucket = bucket_of(full)

    # 入正文：硬核 + 来源相对可靠 + 非纯资本/八卦/诉讼
    if (policy_flag or model_flag or infra_flag or automation_flag) and hard_score >= 2 and tier <= 2 and not unknown_source:
        if market_flag and not (model_flag or infra_flag or policy_flag):
            return ('仅候选池', bucket, '纯资本市场信息，不进正文')
        if legal_flag and not policy_flag:
            return ('待核验', bucket, '法律/诉讼话题热度高，但建议回源核验')
        return ('入正文', bucket, f'硬核度高，来源可靠度T{tier}')

    # 待核验：内容重要，但来源一般/未知，或偏政策/法律/资本混合
    if policy_flag or model_flag or infra_flag or automation_flag:
        if unknown_source:
            return ('待核验', bucket, '内容可能重要，但来源或链接不完整，需回源核验')
        if tier >= 3:
            return ('待核验', bucket, f'内容可用，但来源可靠度一般(T{tier})，建议核验')
        if market_flag or legal_flag:
            return ('待核验', bucket, '资本/法律因素较重，建议核验后决定是否入正文')
        return ('待核验', bucket, '硬核相关，但信号强度一般，建议核验')

    if market_flag or legal_flag:
        return ('仅候选池', '候选观察', '偏资本/诉讼噪音，放候选池观察')

    if hard_score >= 1:
        return ('仅候选池', bucket, '有一点相关性，但不足以进正文')

    return ('仅候选池', '候选观察', '硬核密度不足')


items = []
for num, title, body in pattern.findall(text):
    source_match = re.search(r'\[来源:(.+?)>>\]\((https?://[^)]+)\)', body)
    source = source_match.group(1).strip() if source_match else '未知来源'
    url = source_match.group(2).strip() if source_match else ''
    body_clean = re.sub(r'\[来源:.+?\]\(.+?\)', '', body, flags=re.S).strip()

    verdict, bucket, reason = classify(title.strip(), body_clean, source, url)

    items.append({
        'num': num,
        'title': title.strip(),
        'summary': body_clean.strip(),
        'source': source,
        'url': url,
        'verdict': verdict,
        'bucket': bucket,
        'reason': reason,
    })

body_items = [x for x in items if x['verdict'] == '入正文']
verify_items = [x for x in items if x['verdict'] == '待核验']
pool_items = [x for x in items if x['verdict'] == '仅候选池']

print('【腾讯新闻 AI 候选过滤 v3】')
print(f'更新时间：{update_time}')
if headline:
    print(f'速览：{headline}')
print(f'总条数：{len(items)} | 入正文：{len(body_items)} | 待核验：{len(verify_items)} | 仅候选池：{len(pool_items)}')
print()

print('==== 入正文 ====')
if not body_items:
    print('（暂无）')
else:
    for it in body_items:
        print(f"{it['num']}. {it['title']}")
        print(f"   建议板块：{it['bucket']}")
        print(f"   判断：{it['reason']} | 来源：{it['source']}")
        print(f"   摘要：{it['summary'][:140]}")
        if it['url']:
            print(f"   链接：{it['url']}")
        print()

print('==== 待核验 ====')
if not verify_items:
    print('（暂无）')
else:
    for it in verify_items:
        print(f"{it['num']}. {it['title']}")
        print(f"   建议板块：{it['bucket']}")
        print(f"   判断：{it['reason']} | 来源：{it['source']}")
        print(f"   摘要：{it['summary'][:130]}")
        if it['url']:
            print(f"   链接：{it['url']}")
        print()

print('==== 仅候选池 ====')
if not pool_items:
    print('（暂无）')
else:
    for it in pool_items:
        print(f"{it['num']}. {it['title']}")
        print(f"   建议板块：{it['bucket']}")
        print(f"   判断：{it['reason']} | 来源：{it['source']}")
        print(f"   摘要：{it['summary'][:110]}")
        if it['url']:
            print(f"   链接：{it['url']}")
        print()
PY
