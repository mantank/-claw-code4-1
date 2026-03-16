# 工具与配置

## 服务器
- 2 vCPU (AMD EPYC 7K62), 7.5GB RAM, 8GB Swap
- BrowserWing: localhost:8080, systemd browserwing.service
- Claude Code已安装（Sonnet 4.6）
- VSCode Remote SSH吃1.1GB，用完必须断开

## 代理
- Mihomo v1.19.20, WgetCloud, 127.0.0.1:7890, mihomo.service
- WgetCloud续费状态待确认（上次续费3/7）

## API Keys → 详见 TOOLS.md（避免重复维护）

## Notion 数据库 IDs → 详见 TOOLS.md

## 模型配置
- 001: Claude Opus 4（Max $100/月，5h重置）
- 002/003: Gemini 3.1 Flash Lite（google provider, $370额度至2026-05-10）
- Grok: grok-4-1-fast-reasoning + x_search, $5够用数月

## 飞书公开文档读取
直接调docx raw_content API，传URL中token即可读公开wiki/docx。详见TOOLS.md飞书部分。

## 废弃工具
- Gemini旧key额度用完 / 即梦AI / Evolink旧key / 万相2.1
