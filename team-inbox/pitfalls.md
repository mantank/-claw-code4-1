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
