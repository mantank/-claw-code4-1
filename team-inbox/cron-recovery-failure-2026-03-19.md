Cron恢复失败记录（心跳14:44）
- 现象：`openclaw cron list` 返回空，但 `/root/.openclaw/cron/jobs.json` 有19条（5条enabled，均无nextRunAtMs）
- 已尝试：拷贝jobs.json到005路径，重启gateway，仍无效
- 根因推测：001的cron storePath被覆盖为005路径，或cron模块下一步计算未触发
- 下一步：需旭确认openclaw.json中stateDir配置，或手动重建cron schedule
- 影响：AI日报、公众号流水线等7个cron任务未执行