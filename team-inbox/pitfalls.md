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
