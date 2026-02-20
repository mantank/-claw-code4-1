# HEARTBEAT.md

## 任务0：OpenClaw版本监控（每次心跳都检查）

运行 `bash ~/.openclaw/workspace/scripts/version-check.sh`，根据输出：
- `STATUS:NO_UPDATE` → 无需通知，继续下一个任务
- `STATUS:NEW_VERSION` 或 `STATUS:UPDATED` → 通知老大：更新了什么版本，检查changelog（web_search "OpenClaw changelog {新版本号}"），简要说明新功能
- `STATUS:VERSION_CHANGED` → 记录到memory，不通知
- 如果AUTH:FAILED → 立刻通知老大认证出问题，需要重新配置

## 任务1：时间表提醒

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
