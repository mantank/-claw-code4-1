# claw-code 源码学习 & OpenClaw 自我进化路线图

> 版本：v2.0（心跳驱动版）
> 开始日期：2026-04-02
> 模式：心跳自动推进，每步汇报

---

## 整体目标

通过学习 claw-code 源码，让 OpenClaw 具备：
1. **更聪明** — 更好的上下文管理、成本控制、任务规划
2. **更自主** — 减少人工干预，自动优化自身行为
3. **可进化** — 系统能够感知自身状态并改进

---

## 第二阶段完成 ✅ (2026-04-02 22:52)
```
✅ 2.1 cost_tracker ✅ → HEARTBEAT.md cost日志
✅ 2.2 query_engine ✅ → Compaction监控
✅ 2.3 permissions ✅ → tools-filter skill
✅ 2.4 context ✅ → workspace-scanner
✅ 2.5 session_store ✅ → JSON schema+迁移脚本
✅ 2.6 hooks ✅ → hooks-system skill
✅ 2.7 Tool+tool_pool ✅ → tool-registry skill
✅ 2.8 execution_registry ✅ → 多工具并发方案
✅ 2.9 setup ✅ → system-check skill
✅ 2.10 system_init ✅ → session-init skill

累计产出：10个新skill + 7个新脚本 + 2个schema + 1个路线图
```

## 第三阶段：架构级升级 ✅ (2026-04-02 22:52)

| # | 主题 | 状态 | 产出 |
|---|------|------|------|
| 3.1 | Quality Gate | ✅ 已完成 | 三级分级授权设计+quality-gate-check.sh |
| 3.2 | Streaming协议 | ✅ 已完成 | streaming-protocol skill + 事件模拟脚本 |
| 3.3 | 自监控仪表盘 | ✅ 已完成 | self-dashboard.sh 整合 system-check + compaction-advisor + workspace-scan + session-status |
| 3.4 | 记忆互斥系统 | ✅ 已完成 | memory-mutex/ lock+unlock+dedup 脚本 + DESIGN.md |
| 3.5 | 工具/命令路由 | ✅ 已完成 | intent-router.sh 关键词路由 + DESIGN.md |

## 执行状态
```
✅ 第二阶段 10/10 全部完成！
✅ 3.1 Quality Gate 完成
✅ 3.2 Streaming协议 完成
✅ 3.3 自监控仪表盘 完成
✅ 3.4 记忆互斥系统 完成
✅ 3.5 工具/命令路由 完成

🎉 第三阶段全部完成！
🎉 第四阶段全部完成！
🎉 全部4个阶段全部完成！🎊
```

```
当前阶段：📕 第四阶段 全部完成！
总进度：第四阶段 5/5 ✅
全部阶段：Phase1✅ Phase2✅ Phase3✅ Phase4✅
上次心跳：2026-04-02 23:08
上次心跳：2026-04-02 23:05
上次心跳：2026-04-02 22:52
exec审批：✅ 已解除
```

---

## 阶段一：理解核心架构 ✅

**已读完的模块：** port_manifest / models / task / tools / runtime / permissions / context / session_store / cost_tracker / query_engine / history / hooks

---

## 阶段二：单模块深度攻关（心跳推进中）

| # | 模块 | 状态 | 升级产出 |
|---|------|------|---------|
| 2.1 | cost_tracker | ✅ 已完成 | HEARTBEAT.md加cost日志 |
| 2.2 | query_engine | ✅ 已完成 | Compaction监控+compaction-log.md |
| 2.3 | permissions | ✅ 已完成 | tools-filter skill + 验证脚本 |
| 2.4 | context | ✅ 已完成 | workspace-scanner skill + workspace-scan.sh |
| 2.5 | session_store | ✅ 已完成 | JSON schema + 迁移脚本 |
| 2.6 | hooks | ✅ 已完成 | hooks-system skill + pre_tool_check示例 |
| 2.7 | Tool.py+tool_pool | ✅ 已完成 | tool-registry skill + 工具注册报告 |
| 2.8 | execution_registry | ✅ 已完成 | execution-registry skill + 多工具并发方案 |
| 2.9 | setup | ✅ 已完成 | system-check skill + 系统检测脚本 |
| 2.10 | system_init | ✅ 已完成 | session-init skill + 会话初始化报告 |

---

## 阶段三：架构级升级

| # | 主题 | 状态 |
|---|------|------|
| 3.1 | Quality Gate三级 | ⬜ |
| 3.2 | Streaming协议 | ⬜ |
| 3.3 | 自监控仪表盘 | ⬜ |
| 3.4 | 记忆互斥系统 | ⬜ |
| 3.5 | 工具/命令路由 | ⬜ |

---

## 阶段四：自我进化能力 ✅ (2026-04-02 23:11)

| # | 能力 | 状态 | 产出 |
|---|------|------|------|
| 4.1 | 自我调参 | ✅ 已完成 | self-tuning.sh — Context/Token双阈值监控 |
| 4.2 | 自我诊断 | ✅ 已完成 | self-diagnosis.sh — Gateway/Session/API/磁盘/内存全面诊断 |
| 4.3 | 自我扩展 | ✅ 已完成 | self-extend.sh — Skill缺失自动检测 |
| 4.4 | 自我升级 | ✅ 已完成 | self-upgrade.sh — 版本检测+升级建议 |
| 4.5 | 进化日志 | ✅ 已完成 | evolution-log.sh — 每次改进结构化记录 |

---

## 汇报模板

每次心跳完成一个模块，发送：

```
【001自我升级汇报 #N/10】模块: xxx

✅ 学到什么：xxx
✅ 改了哪里：xxx
✅ 验证结果：xxx
📊 进度：N/10 → N+1/10
🚀 下次心跳：xxx
```

---

## 心跳执行协议

每次心跳执行以下步骤：
1. 读本文件 → 找到当前状态
2. 读下一个待做模块的源码（已在 repos/claw-code-parity/src/）
3. 执行升级
4. 更新本文件状态
5. 发送汇报到 Telegram
