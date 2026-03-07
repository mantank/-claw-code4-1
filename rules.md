# rules.md - 001铁律（执行任务前必读）

> 每条规则都是真金白银踩出来的坑。违反 = 浪费时间 + 挨骂。

## 🔧 工具使用
- web_search: search_lang中文必须用 `zh-hans`，不是 `zh`
- browser 工具当前不可用，不要尝试
- 系统是 opencloudos，用 `dnf`，不是 `apt-get`
- 飞书链接 → 立刻用飞书API读取，**不要用浏览器/web_fetch**
- 飞书读不到完整内容 → 告诉旭"需要登录"，**不许自行搜转载版替代原文**
- OpenClaw provider配置只支持 baseUrl/apiKey/api/models，**不能加proxy等自定义字段**

## 📱 小红书发布
- 标题 ≤ 20字（超了会500报错）
- 必须带图片（无图会卡住）
- 多图发布先测1张确认流程通
- 发布前必须旭确认，测试只用 status/search，**绝不 publish**
- 一次只发一篇

## ✍️ 图片生成
- 中文文字渲染不稳定，数据尽量用英文数字（1T、320B、1M tokens）
- 生成后必须检查中文错字（常见："文"写成"交"、"发"写成"学"）

## 🌙 每日总结
- 必须用 `templates/daily-summary-template.md` 模板，不得自由发挥
- 必须推送到Notion（用notion-push.sh）
- 包含：今日计划、复盘/反省/思考、明日计划

## 📤 内容发布
- AI日报原文转发，不二次加工（会丢链接）
- cron任务必须指定 `--channel telegram`，不用 `last`
- 发布前必须旭确认，不能自己判断就直接发

## 🧠 记忆管理
- 重要决定（字体、配色、架构选择）必须写进文件，不能只记在上下文里
- 每次任务完成后更新 SESSION-STATE.md
- 003汇报"已完成"必须附命令输出证据，不信口头汇报

## ⚙️ 系统配置
- 改provider配置后，同步检查所有agent的fallback别名
- 装skill前先读README确认：有无外部API依赖、是否收费、有无真实案例
- 装新cron前先 `crontab -l` 确认清空旧的

## 🖼️ 公众号配图
- 公众号文章配图永远用 `nanobanana-ppt-skills`，4种风格：白板马克笔/渐变毛玻璃/矢量插画/手绘涂鸦
- 每次生成前必须先推荐风格供旭选择，不得直接生成
- 禁止用 nano-banana-ppt、nano-banana-pro、sketch-illustration、Gemini 图片 API
- 封面尺寸：1664*928（16:9），API: qwen-image-max

## 📋 任务下发规范（2026-03-04 旭要求）
- 每次让002执行任务，必须在 sessions_send 里写清楚：①做什么 ②用哪个文件 ③输出到哪里 ④完成后汇报给谁
- 不能只发一句"去做XXX"——002不会自己猜上下文
- 001知道的背景信息，也要主动告诉002，不能假设002知道

## 🔌 API响应错误判断（2026-03-05 新增）
- Grok API 正常响应中含 `"error": null` 字段，不代表出错
- 脚本中**禁止**用 `if 'error' in d` 判断，会把 null 误判为错误
- **正确写法**：`if d.get('error'):` 只在 error 有真实值时才报错
- 同样适用于其他可能返回 `"error": null` 的 API（参考: grok-x-leaders.sh 修复）

## 铁律13：Grok API error字段判断用 d.get('error') 不用 'error' in d（2026-03-05）
- **错误写法**：`if 'error' in d:` → Grok正常响应有 `"error": null`，null也会触发
- **正确写法**：`if d.get('error'):` → null/空值不触发，只有真实错误才报错
- **覆盖范围**：所有调用Grok API的脚本（grok-x-leaders.sh已修，grok-x-trends.sh已修）
- **同类问题**：其他API也可能有相同模式，凡用 `if 'xxx' in response_dict` 判断错误的都要检查

## 铁律13：Astro/前端项目push前必须视觉验证（2026-03-06）
- build通过 ≠ 样式正确
- push前必须 npm run dev 本地预览，或截图确认关键页面渲染效果
- Tailwind prose类必须确认 @tailwindcss/typography 已安装

## 铁律14：三剑客不可用时必须告知旭（2026-03-06）
- root环境下 claude --dangerously-skip-permissions 被禁，三剑客不可用
- 遇到此情况：立刻告知旭，说明替代方案，不能闷头自己做
- 格式："三剑客在root环境不可用，我直接用工具实现，你确认吗？"

## 规则N+1：push前必须本地视觉验证（来自坑13，2026-03-06）
- `npm run build` 通过 ≠ 样式正确
- 有任何UI改动，必须 `npm run dev` 本地预览，手机模拟器确认排版
- 凡涉及 Tailwind prose / Typography，先确认 `@tailwindcss/typography` 已安装
- 顺序：本地预览 → 旭确认 → push，不能跳过中间步骤

## 规则N+2：三剑客root限制（来自坑13，2026-03-06）
- `claude --dangerously-skip-permissions` 在root环境被禁止
- 三剑客在服务器上实际不可用，001自行实现时要明确告知旭，不能闷头干
- 替代方案：旭在Mac本地跑Claude Code / 001用write+edit工具直接实现

## 飞书API规则（2026-03-06）

**R-FEISHU-01：docx块批量写入每批不超过15个**
- 超过约20块时接口报 `99992402 field validation failed`
- 解决：拆成多批次，每批 ≤ 15 个块

**R-FEISHU-02：飞书wiki文章直接用docx API读取**
- wiki URL末尾token直接当 doc_token 用
- `GET /open-apis/docx/v1/documents/{token}/raw_content` 返回纯文本
- 不需要SPA渲染、不需要curl爬、不需要转换token


## 🚨 系统配置变更必须先确认（2026-03-07 旭要求）
- 修改 openclaw.json、channel配置、provider配置 → **先说方案，等旭说可以再动**
- 聊聊能不能做 ≠ 去做，不要把探讨当成授权
- 违反此规则 = 擅自动了旭的系统
