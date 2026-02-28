# Skill: 公众号发布 SOP

## 触发场景
用户说「发公众号」「发文章」「推文章到公众号」「把这篇发了」时激活。

## 核心原则
旭不做排版/配图/发布执行动作，全交给001/002走这个SOP。

---

## 完整发布流程

### Step 1 — 内容准备
- 确认文章标题、正文（Markdown或纯文本）
- 封面图：若无提供，用万相2.6生成（见TOOLS.md）
- 摘要：取正文前50字或手动撰写

### Step 2 — 排版转换
使用 `baoyu-post-to-wechat` Skill 发布：
```
~/.openclaw/workspace/.agents/skills/baoyu-post-to-wechat/SKILL.md
```
该Skill支持：HTML / Markdown / 纯文本输入，自动调用公众号API。

### Step 3 — 发布参数确认
| 参数 | 说明 |
|------|------|
| title | 文章标题 |
| content | 正文（支持HTML） |
| thumb_media_id | 封面图media_id（需先上传） |
| author | 作者名，默认「深夜开发者」 |
| digest | 摘要，50字以内 |

### Step 4 — 发布 & 确认
- 调用API发布为草稿
- 将草稿链接返回给旭确认
- 旭确认后执行群发

---

## 封面图生成（万相2.6）
```bash
# 接口: POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# Key: sk-3e086717facd4d88a573260d127a15b0
# 模型: wan2.6-t2i
# 尺寸建议: 900x500（公众号封面比例）
```

## 常见问题
- access_token 过期 → 重新获取（有效期2小时）
- 图片未上传 → 先 uploadTempMedia，拿到media_id
- 内容含违禁词 → 用 checkMsg 接口预检

## 相关Skill
- `wechat-strategy` — 写作风格和选题策略
- `baoyu-post-to-wechat` — 实际API调用
