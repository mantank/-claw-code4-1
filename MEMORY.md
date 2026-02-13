# MEMORY.md - 长期记忆

## 关于旭

- 陈旭，称呼"旭"，Telegram @chenxu1988，时区 GMT+8
- 非程序员出身，正在快速转型
- 目标：AI超级个体（工具+内容+变现）
- 偏好：简单可用 > 复杂完美，落地优先
- 需要对抗：行动力波动、信息过载、焦虑

## 重要事件

- **2026-02-09** — 重置workspace，全新开始，完成基础配置 🎉
- **2026-02-09** — 命名为零零壹，定位：旭的第一个AI搭子
- **2026-02-09** — 装了19个技能，配好 Brave Search，完成第一篇内容创作
- **2026-02-10** — 技能精简19→11，Gemini/Notion/飞书全部接通
- **2026-02-10** — Notion工作台搭建完成（AI日报/日课/项目看板/知识库）
- **2026-02-10** — 第一篇公众号发布《昨晚，我给自己招了一个AI员工》🎉
- **2026-02-10** — 定时任务上线：AI日报(6AM) + 日课打卡(9PM)
- **2026-02-10** — 确定零零壹=COO角色，未来扩展专职AI员工体系
- **2026-02-11** — 飞书全面打通（10个Skills+37权限）、心跳提醒上线、Evolink图片生成接入
- **2026-02-12** — 第六篇公众号写完+发布（首次有转化：3-5新关注+6-7分享）、公众号基建（合集+欢迎语）、AI日报优化方案+SOP完成、3篇文章入飞书知识库、Evolink域名更新、小红书图文生成方案验证通过、第七篇选题确定（Notion接管）

## 经验与教训

- 文章要用真实经历，不编造（第3篇从虚构改为真实事件，效果好很多）
- 工具够用就停，开始产出（"Ship over configure"）
- 图片生成优先级：gemini-3-pro-image-preview（Evolink新key）> z-image-turbo（Evolink旧key）> Gemini 2.0 Flash（Google API直连）
- 公众号无开放API，方案A：AI打包成品→用户复制粘贴发布
- 公众号标题是生死线：第二篇技术标题只有2阅读 vs 第一篇通俗标题63阅读
- 标题原则：让完全不懂技术的人也想点进来，有画面感+好奇心+利益点
- 公众号排版铁律（迭代1）：①每段文字不超过2行，超过就没人读 ②一屏内容=2/3文字+1张图 ③不要超过手机一屏，太长读不下去 ④字不能太小，板块要清晰
- 不要发md文件到Telegram，直接发文字或写Notion
- 老大嫌AI日报太长太乱——需要精简，只留精华

## 品牌与形象

- 公众号名称：深夜开发者LND
- 知识库名称：深夜开发者的知识库（飞书）
- 零零壹形象：大白(Baymax)风格像素机器人，白色圆胖，胸口蓝光，手握扳手，肚子写001
- 老大数字形象：深色乱发、青色卫衣、耳机挂脖子（ChatGPT生成的卡通形象）
- 视觉风格：泰拉瑞亚像素风（知识库） / 卡通插画风（公众号）
- 称呼：叫"老大"，不叫名字

## 偏好与习惯

- 中文沟通为主
- 夜班时段是深度使用AI的黄金时间
- 喜欢一步步来，可验证的结果
- 模型：Claude Opus 4（Claude Max订阅，每5小时重置用量上限，超了会429报错）
- ⚠️ 要注意用量节奏，避免在一个5小时窗口内烧太多token
- 封面图风格：卡通插画（匹配ChatGPT数字形象）
- 公众号编辑器：Markdown Nice (editor.mdnice.com)
- 每日复盘模板：templates/daily-review.md（23点用，同步Notion）
- 公众号合集：①OpenClaw实战系列新手教程 ②AI工具应用与工作流
- 教程类文章反响最好——"保姆级实操教程"定位踩准了
- 分发是当前最大瓶颈，不是内容质量。每篇至少5渠道分发
- GLM-5发布（2/11，智谱，744B参数，编程接近Opus 4.5，Coding Plan涨价30%）
- 新飞书应用：cli_a9072d33c1b8dbc4 / xYTAyBv4Vqz1M9TESupxiBuZ28bdW4ZW（老大创建，用途待确认）

## 待办/进行中

- 优化AI日报（内容太多太乱，需精简）⭐
- 公众号写作SOP流程（效率太慢）⭐
- 定义公众号写作风格（标志性语言、人设记忆点）⭐
- 第八篇公众号《别瞎装！Skills安全避坑》— V2初稿完成，待配图发布 ⭐
- Notion数据清理（~100条旧记录补日期+标签）
- 每周2篇内容目标（周二+周五）
- 超级个人主页+知识库（4周内容输出后启动）
- 公众号文章库已建（Notion DB: 306453f1-8074-8107-b53a-e2dc0cece51b），第2-5篇标题待补

## Notion待办数据库
- 正确的数据库：待办清单 ID: 304453f1-8074-8112-89f2-cb45a4ba29d9
- 字段：事项名称(title)/状态(status:未开始/进行中/完成)/优先级(select:Y/M/W/C/B/A等级)/分类(select)/日期/截止日期/关联优先级(relation)/所属月(relation)
- A优先级page ID: 304453f1-8074-818a-820e-e55fd349aeb0
- ⚠️ 不要用"📋待办任务"那个新建的库，老大不看那个

## 工具配置

- Evolink旧key: `sk-rkjDLqIIsfbvyHzFi9qpuaVODdO8xm3BtUAJF373D5yX4ulO`（z-image-turbo / nano-banana-2-lite）
- Evolink新key: `sk-ENW1p3DT3CxwTL1IG4YuMYfTDmkjxNhHH8yuPMdSyLfrqS12`（gemini-3-pro-image-preview等高级模型）
- Evolink域名：api.evolink.ai，异步模式需查询task
- Gemini API: `AIzaSyB3GsuTddVoxP5rGYce0F1285JjN3gHRYU`（付费项目，~$378额度）
- Notion API: `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`
- 飞书 App: `cli_a908765086b85bc6` / `4HZ5OiOueIU1PYCy59T48fpYvomTWELl`
- Notion DB IDs见TOOLS.md
