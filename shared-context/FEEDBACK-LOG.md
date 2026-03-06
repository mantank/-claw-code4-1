# FEEDBACK-LOG.md — 跨Agent通用修正（所有Agent共读）

> 旭给任何一个Agent的反馈，如果对其他Agent也适用，就记在这里。
> 一次修正，全员生效。不用挨个改rules.md。

---

## 写作类

### 1. 公众号配图永远用 nanobanana-ppt-skills 风格（白板马克笔风）
### 1b. 小红书封面/内容图用 Qwen-Image-Max 手绘涂鸦风
- 日期：2026-03-06
- 触发：旭否定了Auto-Redbook渲染的HTML卡片（"太垃圾了"），确认Qwen-Image-Max的doodle-infographic风格OK
- 规则：小红书图片用 qwen-image-max 模型 + sketchnote doodle infographic 风格生成，不用HTML渲染技能
- 日期：2026-03-04
- 触发：旭多次否定水彩/日系/卡通风格
- 规则：生成前先推荐风格让旭选，不得直接生成

### 2. 文章结尾必须用模板
- 日期：2026-03-04
- 模板位置：templates/article-endings.md（A传播型/B留存型）
- 规则：不得自创结尾格式

### 3. 不要提"复刻别人做过的东西"
- 日期：2026-02-28
- 旭反感这个思路，我们做原创路径

## 沟通类

### 4. 全中文回复，不要大段英文
- 旭看不懂英文，模型专有名词可保留但加中文说明
- 链接、命令行可以是英文

### 5. 不要主动推送夜检报告/任务提醒
- 日期：2026-03-04
- 心跳只做后台任务，不主动打扰旭

### 6. 不要切换到低配模型降级
- 旭明确要求001保持Opus，不要自作主张降到Sonnet

## 技术类

### 7. 公众号链接用BrowserWing读，不用web_fetch
- mp.weixin.qq.com 的反爬会导致web_fetch拿不到内容

### 8. 飞书文档用飞书API读，不用web_fetch
- feishu.cn/wiki/ 或 feishu.cn/docx/ 链接走飞书Skills

### 9. Grok API error判断用 d.get('error') 而非 d.get('error','')
- 日期：2026-03-05
- Grok返回 error:null 时，d.get('error','') 不为空字符串会误判

## 流程类

### 10. Notion每日记录：一天一个文档，计划+总结合并
- 文件名格式：「每日记录 YYYY-MM-DD」（名称在前，日期在后）
- 必须用固定模板，不得自创格式

### 11. 发布前必须验证publish文件末尾内容正确
- 日期：2026-03-04
- 踩坑：修改文章后publish文件没同步，发出去的是旧版

---

*新增修正直接追加到对应分类下，注明日期和触发原因。*
