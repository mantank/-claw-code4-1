---
name: sketch-illustration
description: 插画图片生成技能，支持多种手绘风格。使用 qwen-image-max（¥0.04/张）生成插图，适合流程图、功能说明、PPT配图、教程配图等场景。支持三种风格：A) Sketch 极简手绘风（Notion/Linear 风格）；B) Watercolor 奶油彩铅水彩风；C) Flat Vector Retro 扁平矢量复古风。当用户要求生成插画、配图、手绘风格图、流程示意图、产品插图、PPT配图时触发此技能。
---

# 插画生成 Skill

用 qwen-image-max 生成手绘风配图，¥0.04/张。

## 风格选择

查看 `references/styles.md` 了解三种风格详细说明：
- **风格 A：Sketch 极简手绘风**（默认）— Notion/Linear 风，极简冷淡，适合技术流程图
- **风格 B：Watercolor 奶油彩铅水彩风** — 暖色调纸纹，适合 PPT 配图、课程讲义
- **风格 C：Flat Vector Retro 扁平矢量复古风** — 黑色轮廓线+几何简化，适合课程封面、复古感内容

用户未指定时默认用风格 A。

## 执行流程

### 1. 确认内容与风格
- 明确要画什么内容、用什么风格
- 从 `references/styles.md` 取对应风格块

### 2. 构建 Prompt

基础结构：
```
[风格块（从 styles.md 复制）]
顶部居中标题：'[中文标题]'
[内容描述：人物、场景、元素、布局]
[负面约束]
```

详细提示词模板见 `references/prompt-guide.md`。

### 3. 生成图片

```bash
python3 /root/.openclaw/workspace/skills/sketch-illustration/scripts/generate_sketch.py \
  --prompt "<完整prompt>" \
  --output /root/.openclaw/workspace/assets/YYYY-MM-DD-描述.png \
  --size "1664*936"
```

**尺寸参考：**
- PPT配图（16:9）：`1664*936`
- 小红书封面（3:4）：`1104*1472`
- 公众号配图（1:1）：`1328*1328`
- 公众号封面（16:9）：`1664*928`

### 4. 发给旭确认后使用

图片生成后发给旭看，确认OK再插入文章或发布。

## 注意事项

- 模型：qwen-image-max（阿里云百炼，¥0.04/张）
- API Key 已内置在脚本中，无需额外配置
- 生成时间约 30-60 秒
- 失败重试1次，再失败告知旭
- Gemini / ZenMux 已废弃，禁止使用
