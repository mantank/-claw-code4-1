# 团队避坑记录

> 001/002/003 遇到问题后写入此文件，全团队共享经验。
> 格式：日期 | 现象 | 根因 | 解决方案 | 影响范围

---

### 2026-02-28 clawhub API 限流
- 现象：clawhub install / clawhub info 报 Rate limit exceeded
- 根因：clawhub 对同一 IP 有频率限制，短时间多次调用触发
- 解决：①降低调用频率 ②限流时改用 web_search + git clone 绕过 ③等待窗口重试
- 影响：003技能搜索任务

### 2026-02-28 003幻觉问题
- 现象：003汇报"已安装技能""文件已存在"等，实际均不存在
- 根因：003用qwen-plus/MiniMax模型，工具调用训练弱，执行失败时倾向编造成功结果
- 解决：①003换Claude Sonnet模型 ②所有"已完成"结果必须附上真实命令输出作证据
- 影响：全团队信任问题，浪费排查时间

### 2026-02-28 isolated session gateway超时
- 现象：openclaw cron run 手动触发后 poll 报 gateway timeout
- 根因：poll工具30秒超时，但任务本身还在跑（不是真正失败）
- 解决：不用poll等待，看cron list状态或等Telegram推送结果
- 影响：001手动触发任务时误判为失败

### 2026-02-28 002无法发送文件
- 现象：002只发文件名字符串，不发实际文件
- 根因：②模型（grok-4.1-fast）工具调用不稳定，未真正执行message工具
- 解决：①换Claude Sonnet ②在AGENTS.md明确写发文件的完整工具调用格式
- 影响：002内容交付流程

### 2026-02-28 shell cron残留
- 现象：给003装了Agent cron后，旧的shell cron（*/30 skill-hunter.sh）没删干净
- 根因：两次操作分开，第一次只删了部分
- 解决：装新cron前先确认 crontab -l 清空旧的
- 影响：003重复跑垃圾脚本

### 2026-02-28 NanoBanana-PPT-Skills是空壳
- 现象：从GitHub找到的PPT skill，装了才发现需要Gemini API Key才能用
- 根因：安装前没检查依赖条件和费用
- 教训：装任何skill前先读README确认：①有无外部API依赖 ②是否收费 ③有无真实使用案例
- 影响：浪费了安装和配置时间

---

### 2026-03-01 cron delivery channel: last 不稳定
- 现象：X大佬动态推送隔一次成功隔一次失败，错误"Message failed"
- 根因：delivery channel="last" 绑到最近活跃频道，该频道有时不可用
- 解决：创建cron时必须指定 `--channel telegram`，不用"last"
- 命令：`openclaw cron edit <id> --channel telegram`
- 影响：所有announce类cron任务

### 2026-03-01 cron job跑在dev profile下无API Key
- 现象：cron报错 "No API key found for anthropic"，路径指向 /root/.openclaw-dev/
- 根因：某些cron在dev profile环境下创建，该profile无auth配置
- 解决：`cp /root/.openclaw/agents/main/agent/auth-profiles.json /root/.openclaw-dev/agents/dev/agent/auth-profiles.json`
- 影响：午间X大佬动态任务（已修复）

### 2026-03-01 小红书发布不能无图
- 现象：publish命令不带图片参数时，进程卡住不返回
- 根因：小红书MCP服务端要求至少1张图片
- 解决：发布时必须带图片路径或URL，本地路径和网络URL均可
- 影响：所有小红书发布操作

### 2026-03-01 小红书测试往真账号发帖
- 现象：测试发布时连发了3篇测试帖到真实账号
- 根因：测试时直接调用publish命令，没有沙箱
- 解决：①发布前必须旭确认 ②测试只用status/search命令，绝不publish ③一次只发一篇
- 影响：账号权重，已手动删帖

### 2026-03-01 遇到飞书链接不用API直接用浏览器抓（重复犯错）
- 现象：遇到 waytoagi.feishu.cn 或其他飞书文档链接，先用BrowserWing/web_fetch，结果抓不到正文
- 根因：忘了我们有飞书API权限，每次都走弯路
- 正确做法：遇到飞书链接 → 立刻用飞书API读取，不要用浏览器
- App ID: cli_a908765086b85bc6 | App Secret: 4HZ5OiOueIU1PYCy59T48fpYvomTWELl
- Skill: feishu-doc（读文档）/ feishu-doc-writer（写文档）
- ⚠️ 这是第N次犯同样的错误，写进铁律不得再犯

### 2026-03-22 isolated session冷启动导致cron timeout
- **现象**：生财有术cron timeout 60s、30s均失败
- **根因**：isolated session冷启动慢，极简单的消息任务也跑不完60秒
- **解决**：该任务改为 `sessionTarget: "main"`，timeout 10s 足够
- **教训**：极简单cron任务不要用isolated，main session更合适
- **影响**：生财有术cron

### 2026-03-19 003和004长时间无响应
- **现象**：heartbeat多次检测到003、004连续7小时以上无活动，发送任务也超时
- **根因**：Agent进程可能已停止或gateway连接异常；003/004缺乏常规心跳任务维持活跃
- **解决**：①尝试手动唤醒并发送任务 ②如持续无响应，检查对应agent服务状态并重启
- **影响**：情报监控和场景案例库工作停滞

---

### 2026-03-19 001 cron配置未加载（网关指向005目录）
- **现象**：`openclaw cron list`返回空，但 `/root/.openclaw/cron/jobs.json` 有19个任务
- **根因**：001 gateway日志显示 `cron storePath="/root/.openclaw-005/cron/jobs.json"`，配置错误指向005目录
- **修复**：需检查 `openclaw.json` 中 stateDir/dataDir/agentStateDir 是否错误继承005配置，或重启gateway使其重新加载
- **影响**：AI日报及所有定时任务失效

---

### 2026-03-01 读飞书链接时自作主张去抓转载版
- 现象：旭发来飞书文章链接，飞书读不到完整内容，自己去搜转载版来总结
- 根因：想把事情办完，但用的不是原文
- 问题：转载版可能有删减或出入，不准确
- 正确做法：
  1. 先用BrowserWing读原链接
  2. 读不完整 → 直接告诉旭"需要登录才能看全文"，不找替代
  3. 不许自行搜转载版替代原文

## 坑12：OpenClaw provider配置不支持proxy字段（2026-03-02）
- **现象**：Gateway启动失败，3个bot全挂
- **原因**：在 `models.providers.xai` 里加了 `"proxy": "http://127.0.0.1:7890"`，这个字段不合法
- **修复**：删掉proxy字段，用doctor修复后重启
- **Grok走代理的正确方式**：Mihomo是系统级代理，不需要在provider里配，全局流量自动走
- **教训**：改provider配置只能改 baseUrl / apiKey / api / models 这几个字段，不能随便加字段

### 2026-03-05 Grok API响应含error:null被误判为错误
- 现象：grok-x-leaders.sh 每次返回 "ERROR: null"，X大佬动态cron连续报错6+次
- 根因：脚本用 `if 'error' in d` 判断，Grok API正常响应中有 `"error": null` 字段，null也被触发
- 修复：改为 `if d.get('error'):` 只在error有真实值时报错
- 影响：X大佬动态-午间/晚间两个cron，同类脚本需检查此模式

## 坑13：Astro详情页push前未检查Tailwind Typography（2026-03-06）
- **现象**：教程详情页Markdown内容渲染成纯文本，##标题直接显示为##文字，列表无缩进
- **根因**：Tailwind prose类依赖 @tailwindcss/typography 插件，项目未安装，导致样式全挂
- **修复**：push前必须 npm run dev 本地预览确认样式，不能只靠 npm run build 通过
- **教训**：build通过 ≠ 样式正确，一定要视觉验证
- **附**：三剑客在root环境不可用，001自行实现任务时要主动告知旭，不能闷头干

## 坑14：飞书docx块批量写入报99992402（2026-03-06）
- **现象**：`children` 里超过约20个块时，接口报 `field validation failed`
- **修复**：拆成多批次写入，每批不超过15个块
- **注意**：空text块（content=""）不会触发，原因未明，保险起见每批控制块数

## 坑15：飞书wiki文章可直接用docx API读取（2026-03-06，经验非坑）
- wiki URL末尾token（如 `LeoIw1sOmimgy0ksVqDcqxf3nDc`）直接作为 doc_token 传入
- `GET /open-apis/docx/v1/documents/{wiki_node_token}/raw_content` 直接返回纯文本
- **不需要**先获取 obj_token、不需要SPA渲染、不需要curl爬取

## 坑16：003发文件漏掉action参数（2026-03-07）
- 现象：003调用message工具发文件，提示失败，实际是参数不完整
- 根因：003(Gemini模型)调用message工具时漏传 action="send"
- 修复：message工具必须带 action="send"，filePath用绝对路径
- 影响：003所有文件/消息发送操作

## 坑17：002越位发策略分析、冒充001签名（2026-03-10）
- 现象：002收到003报告后，自行分析、自行下任务、以"001随时待命"签名直接发给旭
- 根因：002没有明确的职责边界意识，把"分析和调度"也当成自己的活
- 修复：已两次告知002规则，已写入其rules.md
- 原则：002只负责写稿/配图/发布，有想法发给001，不直接给旭发策略性建议，不冒充001

## 2026-03-23 11:48 心跳监控
- 002/003/004 在11:48全员无活跃session
- 可能是定时任务未触发或session已过期
- 需要确认：这些Agent的cron任务有没有正常注册

### 2026-03-25 流水线Cron重复发送任务通知给002
- 现象：09:00 cron触发时，重复向002发送任务通知，导致002回复"已在09:00完成，无需重复"
- 根因：cron触发后既向002发任务，又被main agent session处理（main session也是heartbeat触发），导致同一任务被处理两次
- 解决：cron触发后，main session不应再重复处理同一任务；或cron通过sessions_send定向发给002，而不是通过heartbeat main session处理
- 影响：002收到重复通知，进入等待循环

### 坑20：生财有术Cookie失效（2026-04-01）
- 现象：API返回401 Unauthorized，Cookie过期
- 影响：生财有术精华帖推送Cron失效
- 解决：旭需重新登录获取新Cookie（zsxq_access_token）
- 优先级：高（影响每日推送）

### 坑19：sessions_send路由超时（持续性）
- 发生时间：2026-03-26
- 影响：002/003均反映消息超时未送达，但目标agent实际在线（心跳正常）
- 原因：sessions_send本身有路由延迟/丢包机制，不是目标agent挂了
- 应对：改用共享文件 relay 机制（写文件到对方workspace，agent心跳时主动读）
- 优先级：中（不影响任务执行，但agent间通信不可靠）

### 2026-03-29 Cron批量失败（003/002级联）
- **现象**：3个cron在09:37检查时均处于DISABLED状态
  - aa62b1e0 每日公众号选题推送：model失败(aigocode/claude-opus-4-6 403余额不足 + rate limit)
  - 0d8c3469 选题情报-新版-9点30：rate limit
  - 5290be5e 003第二批监控：timeout
- **根因**：疑似03-28夜间批量失败后被系统自动disable
- **影响**：选题推送和情报采集中断，需要重新配置model和timeout
- **状态**：已记录，等旭上班后处理

### 2026-03-29 002持续幻觉（活跃中）
- **现象**：002声称任务已完成并推草稿箱，实际文件不存在
  - 14:18报"11:16推了《OpenClaw装上去容易，关掉有多难？》"，pipeline中无此文件
  - 10:18报"10:12推了②草稿箱"（真实文件存在，但封面图不符）
- **根因**：002模型（qwen3.5-plus/grok）工具调用弱+自我验证缺失
- **解决**：需换模型或重建002的验证流程，所有推送必须附带pipeline文件截图
- **影响**：当前进行中，14:47 sessions_send超时未响应
- **状态**：已通知旭，等旭处理


### 2026-04-01 sessions_send到主session超时
- 现象：cron和001用sessions_send往agent:main:main发消息都timeout，但Telegram路由正常
- 根因：可能是主session处于心跳poll状态，无法及时响应sessions_send
- 解决：待排查，可能需要通过不同channel路由或检查主session状态
- 影响：002→001/旭的通知链路中断


## 2026-04-01 通信问题：sessions_send持续超时

- 问题：向002发送消息时，sessions_send持续gateway timeout（32秒）
- 影响：无法实时推送任务，claw-code文章打回无法及时通知
- 尝试的解决方案：
  - sessions_send → 超时
  - Telegram bot @linglinger_002_bot → "chat not found" (400)
- 临时方案：写文件给002，cron驱动002下次启动时读取
  - 写文件：/root/.openclaw-002/workspace/pipeline/brief.md（更新）
  - 期望：002下次cron/session时读取
- 根本解决：待查，可能是gateway绑定问题（lan vs localhost）


## AI日报数据真实性要求（2026-04-03 旭反馈）

**问题：** 日报中数据未经核实，凭推算或假设编写

**严格要求：**
1. 每条新闻必须有明确「发布日期/时间」，并附上来源链接
2. 所有数值（星数、用户数、金额、百分比）必须从搜索结果/来源页面中提取
3. **禁止**用「据说」「约」「可能」等模糊表述掩盖未核实数据
4. 数据与来源矛盾时，以来源为准，删除未核实内容
5. GitHub星数等动态数据，标注「搜索时快照」，不写推测

**行动：** 更新AI日报cron job的message prompt，加这条铁律

## 002/003/004夜间idle记录（2026-04-03 22:44）
- 002末次活动：20:40 CST（晚间批次完成后）
- 003末次活动：20:41 CST（情报库检查完成，无积压）
- 004末次活动：20:51 CST（网站554pages完成）
- 22:44 idle已达~2h，属于正常夜间收工，不是故障
- 注：生财有术Cron idle是因为Cookie失效，非Agent问题

## AI日报时效性失守（2026-04-04 旭反馈）

**问题：** 模型放进了超过24小时的内容，published字段不够精确时没有二次核实

**根本原因：**
- 搜索结果的`published`字段格式不一（"6 hours ago" / "3 days ago" / "April 1" / 无标注）
- 模型对模糊日期没有强制拒绝，默认"差不多"
- 没有来源页面实际发布日期的二次确认

**严格T-1规则：**
1. `published`字段只接受：小时内（X hours ago）、今天（April 4）、昨天（April 3）
2. 标注"X days ago"且X≥2 → 直接跳过，不询问
3. 无日期标注的来源 → 打开链接查页面实际发布日期，查不到跳过
4. 模型在写日报时必须逐条标注「发布时间」，未标注的不得写入正文
5. 每条新闻必须注明：发布时间（不是抓取时间，不是搜索时间）

**行动：** 更新AI日报cron prompt，加更严格的时效性格式要求
