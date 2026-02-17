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
- **2026-02-13** — 第八篇公众号发布《别瞎装！Skills安全避坑》🎉、生财有术API打通+每日19:00精华帖自动推送、Chrome插件需本地Node Host（暂搁置）、公众号引流钩子模块待定
- **2026-02-15** — 日报cron大升级、002号装机指南、一人公司方向确定、小红书图文5张、公众号第9篇写完（外链被审核卡住）、即梦AI+万相2.6 API打通🎉、第10篇大纲完成、加入OpenClaw付费课程社群
- **2026-02-17** — 春节假期Day1，AI前沿研究报告完成（Seedance 2.0/Pomelli/Vibe Coding/一人公司趋势）、4篇选题规划（第9-12篇）、ClawHub Skills汇总23个
- **2026-02-18** — 零零壹夜班：第9篇终稿+第10篇初稿+日报模板v3+风格指南v1.1+Notion验证通过+Memory维护

## 经验与教训

- 文章要用真实经历，不编造（第3篇从虚构改为真实事件，效果好很多）
- 工具够用就停，开始产出（"Ship over configure"）
- 图片生成优先级：即梦AI（火山引擎API）> Gemini 2.0 Flash（Google API直连）> Evolink（IP被封待修复）
- AI生图通病：中文字体渲染都不行，最佳方案是AI出底图+Canva叠清晰文字
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
- Seedance 2.0（字节，2/10发布）— AI视频生成标杆，多模态输入，配合Kling 3.0
- Google Pomelli — 品牌内容自动生成（美加澳新公测，国内暂不可用）
- Vibe Coding — MIT 2026十大突破技术，Lovable/Replit/Cursor让零基础造App
- 一人公司+AI Agent成2026主旋律（BI/Metaintro/Fast Company多家报道）
- 春节假期5天（2/17-2/21），每晚2-3小时电脑时间

## 生财有术（知识星球）
- Group ID: 1824528822，Cookie有效期到2026年底
- 精华帖: scope=digests，最新帖: scope=all
- 每日19:00自动推送精华帖（cron job已设置）
- scys.com板块menuId：中标539 / 超级标2634453 / 亦仁1985685 / 超级术3783551 / 亦仁收藏夹1702
- scys.com独立站需X-TOKEN（前端localStorage），知识星球API够用

## Moltbook（AI社交平台）
- 注册名：Agent-001-LND，状态：pending_claim
- API Key存在 ~/.config/moltbook/credentials.json
- 认领链接：https://moltbook.com/claim/moltbook_claim_5LbeaBnam-zBebsfyCxW6psau1KNeeJG
- 验证码：scuttle-PJJR
- OPCC（一人公司教会）：刘小排发起，拟加入申请创始先知
- Profile: https://moltbook.com/u/Agent-001-LND

## Chrome插件 & Node Host
- OpenClaw Chrome插件需要本地Node Host才能连远程Gateway（origin限制）
- 暂时搁置，等有本地机器再弄

## 知识付费/变现
- OpenClaw付费课程社群已加入（199元 30%分销）
- 分销当副线 内容当主线 — 先攒人 不急着卖
- 3周验证计划：先教 用数据定方向（详见Notion）
- 公司暂定定位：帮普通人用AI提效的内容+工具公司
- 引流现状：公众号文章→微信加好友（已有3人转化）
- 阶段一（200粉前）：不建群 1对1聊 挖需求
- 阶段二（200粉后）：建免费交流群
- 阶段三（500粉后）：做付费产品
- 公众号不能带外链！会被审核卡住（第9篇踩坑）→ 链接引导到评论区

## 待办/进行中

- **第9篇AI工具箱终稿已就绪** — articles/article-09-ai-toolbox.md ✅
- **第10篇AI员工初稿完成** — articles/article-10-ai-employees.md ✅
- **引流钩子已初步落地** — 加微信送链接清单/配置文件
- ~~优化AI日报~~ → 精简日报模板v3完成（templates/daily-report-template.md）✅
- ~~定义公众号写作风格~~ → 风格指南v1.1完成（templates/writing-style-guide.md）✅
- Notion推送脚本key已更新，验证通过 ✅
- 第11篇选题：Seedance 2.0视频教程（2/24）
- 第12篇选题：Vibe Coding入门（2/27）
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

- Evolink旧key两个都失效（IP被封 43.159.48.54）
- Evolink最新key: `sk-5ZFrdndazZvcDEDFjEU8gbxScFHXLYLzzKjr8WlZn7WjJG0u`（待本地机器测试）
- Evolink图片正确接口: /v1/images/generations（异步任务+轮询）
- 火山引擎即梦AI: AK/SK签名，req_key=high_aes_general_v20，200次免费额度
- 阿里云百炼Coding Plan: 首月10元/18000次，支持OpenClaw（备选给002号）
- Gemini API: `AIzaSyB3GsuTddVoxP5rGYce0F1285JjN3gHRYU`（付费项目，~$378额度）
- Notion API: `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`
- 飞书 App: `cli_a908765086b85bc6` / `4HZ5OiOueIU1PYCy59T48fpYvomTWELl`
- Notion DB IDs见TOOLS.md
