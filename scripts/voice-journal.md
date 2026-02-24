# 语音日记功能说明

## 工作原理

OpenClaw已经能接收Telegram语音消息并自动转文字（通过Telegram自带的语音识别或ffmpeg+whisper）。

## 使用方式

旭在Telegram给001发语音消息，001自动：
1. 接收并转文字
2. 记录到 memory/YYYY-MM-DD.md 的"语音笔记"板块
3. 如果是深夜（23:00后），自动整理当天所有语音笔记为结构化日记

## 触发方式

- 随时发语音 → 自动记录
- 说"整理今天的语音笔记" → 手动触发汇总
- 每晚睡前做总结时自动包含语音笔记内容

## 技术依赖

- ffmpeg: ✅ 已安装 (v7.0.2)
- Telegram语音消息: OpenClaw原生支持
- 不需要额外的whisper模型，Telegram App端已经做了语音转文字

## 注意

如果Telegram没有自动转文字，需要在服务器端用whisper处理。
可以后续安装 openai-whisper 或 faster-whisper 来本地处理。
