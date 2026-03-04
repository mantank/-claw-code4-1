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
