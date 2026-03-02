# HEARTBEAT.md

## 任务0：OpenClaw版本监控（每次心跳都检查）

运行 `bash ~/.openclaw/workspace/scripts/version-check.sh`，根据输出：
- `STATUS:NO_UPDATE` 或 `STATUS:ALREADY_NOTIFIED` → 无需通知，继续下一个任务
- `STATUS:NEW_VERSION` → **只通知，不要自动更新！** 做以下三件事：
  1. web_search "OpenClaw {新版本号} changelog" 查更新内容
  2. 整理：新功能是什么、有没有破坏性变更、是否值得现在更新
  3. 发消息给旭，等他确认后再说"帮你升级"
- `STATUS:VERSION_CHANGED` → 记录到memory，不通知

## 任务1：主动任务推进

读 `GOALS.md`、`PROJECT_STATUS.md`、`001-KPI.md`，判断：
- 001-KPI.md里的"自主任务队列"有没有未完成的事 → 立刻干
- 有没有我可以**现在就默默干**的事（不打扰旭）
- 有没有快到截止日期的任务需要提醒

**KPI自查（每次心跳）：**
- AI日报Cron是否正常（非error）？
- 今天有踩坑未记录？→ 补写到memory/今日日记
- PROJECT_STATUS.md是否超过3天未更新？→ 主动更新
- 连续2次心跳没有实质产出？→ 主动找一件事干

如果有可以主动做的事，去做，做完后简报通知旭。
如果没有，跳过这个任务。

## 任务2：时间表提醒

读取 `schedule.md` 和当前时间（GMT+8），找到老大现在应该在做什么，发一条简短提醒。

### 规则
1. 用 session_status 获取当前UTC时间，转换为GMT+8
2. 对照 schedule.md 找到当前时间段对应的任务
3. 发一条Telegram消息提醒老大，格式简短有力，例如：
   - "🚀 20:30 副业深度时间开始了！内容创作/学AI/做产品，专注干活"
   - "📖 12:00 读书时间，雷打不动"
   - "🏃 20:00 该运动了，动起来"
4. 如果是睡眠/通勤/吃饭等生活时间段，不提醒，回复 HEARTBEAT_OK
5. 如果是副业深度块（14:30-17:00 或 20:30-23:00），语气要强一点，拉回注意力
6. 提醒风格：直接、简短、有能量，不啰嗦。偶尔可以毒舌一句（"别刷手机了老大"）
7. 不要每次都用同样的话，变着花样说

### 不提醒的时段
- 0:00-6:00（睡觉）
- 7:00-8:30（通勤/早饭）
- 11:30-14:30（午饭/午休/散步）
- 17:00-19:30（通勤/洗澡/吃饭/交接）
- 23:30-24:00（准备睡觉）

## 任务3：记忆卫生（每次心跳轻量检查）

### 每次心跳
1. 检查今天的日记 `memory/YYYY-MM-DD.md` 是否存在，不存在就创建
2. 如果有重要事件发生但没记录，补写进当日日记

### 每周一（GMT+8）
执行一次大扫除：
1. 检查 `memory/` 下超过7天的日记文件 → 有价值的内容归入主题文件，然后移到 `memory/archive/`
2. 检查各主题文件大小，超过3KB的清理过期内容
3. 检查 `MEMORY.md` 索引是否需要更新（新主题文件/当前重点变化）
4. 完成后在当日日记记录：「记忆卫生完成，归档X个文件」

## 任务4：技能分配（每次心跳检查）
读取 `/root/.openclaw/workspace/team-inbox/new-skills.json`
找出 status="pending" 的技能，根据以下规则分配：
- category="content" → 复制到 /root/.openclaw-002/workspace/skills/，用message通知002
- category="system" → 留在001 workspace
- category="general" → 001+002都复制一份

分配完把该条目 status 改为 "done"，并记录分配时间和去向。
无pending条目跳过。

## 任务5：003健康监控（每次心跳检查）

检查003（@linglingsan_003_bot）是否在正常工作：
1. 用 `sessions_list(kinds=["agent"], activeMinutes=60)` 查003的session
2. 如果003有活跃session → 跳过
3. 如果003无活跃session且有未完成任务 → 发消息唤醒003（通过Telegram直接@它）并通知旭
4. 如果003报错 → 记录错误到 `team-inbox/pitfalls.md`，通知旭

003当前长期任务：见 `/root/.openclaw-003/workspace/STANDING-ORDERS.md`

## 任务6：读避坑记录（每次新任务前）
涉及以下操作前，先查 `/root/.openclaw/workspace/team-inbox/pitfalls.md`：
- 安装新技能
- 触发003/002任务
- 调用外部API

避免重复踩已知的坑。
