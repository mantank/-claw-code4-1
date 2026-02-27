# 工具与配置

## 服务器
- 规格：2 vCPU (AMD EPYC 7K62), 7.5GB RAM, 8GB Swap
- BrowserWing：http://localhost:8080，systemd browserwing.service
- Chromium：/root/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome（--no-sandbox）
- Claude Code：已安装（服务器+VSCode插件，Sonnet 4.6）
- VSCode Remote SSH吃1.1GB内存，用完必须断开

## 代理
- Mihomo v1.19.20，WgetCloud订阅，端口 127.0.0.1:7890
- ⚠️ WgetCloud到期：2026-03-07（需续费提醒）
- systemd: mihomo.service（开机自启）

## API Keys
- **万相2.6**：sk-3e086717facd4d88a573260d127a15b0（图片生成主力）
- **Notion**：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
- **飞书**：cli_a908765086b85bc6 / 4HZ5OiOueIU1PYCy59T48fpYvomTWELl
- **OpenRouter**：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
- **Grok**：xai-4YPImuiPnmESoKUHoKBbX7Mp1yX1IojfdBpSghrrA9ApexIkIaHgBZBFrhhnnsDFn5xQPPnEBQ9HObuG
- **Brave Search**：BSAU5ZtdDdeNlW3_EiKVFpuASTqiHiE（付费版，50次/秒）
- **Gemini**：AIzaSyB3GsuTddVoxP5rGYce0F1285JjN3gHRYU（额度用完，仅对话）
- **Evolink**：sk-5ZFrdndazZvcDEDFjEU8gbxScFHXLYLzzKjr8WlZn7WjJG0u（待测试）

## Notion 数据库 IDs
- 工作日志：bf0b46f590d943089e758c61c0a7b0e7
- AI日报：303453f1-8074-8130-9096-c99bd40be6c0
- 日课十二条：303453f1-8074-819b-b376-ceb1c3e4b402
- 项目看板：303453f1-8074-8162-98be-d2bf7b2dcc03
- 知识库：303453f1-8074-81ab-ba5c-d4101f22c310
- 待办清单：304453f1-8074-8112-89f2-cb45a4ba29d9（⚠️ 用这个，不用"📋待办任务"那个）
- 公众号文章库：306453f1-8074-8107-b53a-e2dc0cece51b
- A优先级page ID: 304453f1-8074-818a-820e-e55fd349aeb0

## 模型配置
- 001主力：Claude Opus 4（Max订阅，5小时重置）
- Fallback：Sonnet 4.6 → Opus → Gemini 3.1 Pro → Qwen Plus
- 002主力：Claude Sonnet 4.6 via OpenRouter，Fallback: qwen-plus
- Telegram streaming: partial（reasoning关闭）
- Grok：grok-4-1-fast-reasoning + x_search，$5够用数月

## 废弃工具
- Gemini图片生成：额度用完
- 即梦AI/Evolink：已废弃
- Evolink旧key两个失效（IP被封）

## Grok + X热点
- grok-x-trends.sh：调用grok-4-1-fast + x_search
- 每次搜7次X，返回5个带链接的真实热点
- 每次约$0.01-0.05
