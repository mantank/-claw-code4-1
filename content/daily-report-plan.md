# 每日日报自动化方案

## 目标
每天 23:50（北京时间）自动生成当日工作日报，发送到 Telegram。

## 实现方式

使用 OpenClaw cron 功能，创建定时任务。

### 命令（等旭确认后执行）

```bash
openclaw cron add \
  --name "daily-report" \
  --cron "50 15 * * *" \
  --tz "Asia/Shanghai" \
  --message "现在是北京时间23:50，请生成今天的工作日报。步骤：1) 读取 memory/ 目录下今天的文件；2) 整理今天完成的任务、进展、遇到的问题；3) 写成简洁的日报格式；4) 保存到 memory/YYYY-MM-DD.md（如果还没有的话）。日报格式：已完成/进行中/明日计划，三段式，简洁不啰嗦。" \
  --announce \
  --channel telegram \
  --session isolated \
  --thinking low \
  --timeout-seconds 120
```

### 参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| --cron | `50 15 * * *` | 每天 15:50 UTC = 23:50 北京时间 |
| --tz | Asia/Shanghai | 时区（注：cron表达式本身是UTC，加tz后可能会自动转换，需确认） |
| --announce | - | 将结果发到聊天里 |
| --session | isolated | 用独立session，不干扰主对话 |
| --thinking | low | 不需要深度思考 |
| --timeout-seconds | 120 | 2分钟超时 |

### 注意事项

1. **时区确认：** `--tz` 参数 + `--cron` 的组合行为需要测试。如果 --tz 生效，cron 应该写 `50 23 * * *`；如果 --tz 不生效，用 UTC 写法 `50 15 * * *`
2. **先测试一次：** 创建后用 `openclaw cron run daily-report` 手动触发一次，确认效果
3. **日报内容依赖：** 需要日常坚持在 memory/ 下记录，日报才有内容可整理
4. **成本：** 每天一次调用，token 消耗很少

### 管理命令

```bash
openclaw cron list              # 查看所有定时任务
openclaw cron run daily-report  # 手动触发测试
openclaw cron disable daily-report  # 暂停
openclaw cron enable daily-report   # 恢复
openclaw cron rm daily-report       # 删除
```

## 状态：⏸️ 等旭确认后执行
