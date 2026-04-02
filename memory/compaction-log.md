# Compaction 监控日志

> 基于 claw-code query_engine 设计
> 记录 context 使用趋势，提前预警

---

## 阈值参考（claw-code 模式）
- ⚠️ context > 80% → 建议 compaction
- ⚠️ 估算轮次 ≥ 20 → 建议 compaction
- ⚠️ Token 总量 ≥ 80k → 接近预算

---

## 2026-04-02

| 时间 | Context% | Compactions | Token总量 | 状态 |
|------|---------|------------|---------|------|
| 22:43 | 30% | 0 | ~40k | OK |

| 22:52 | 53% | 0 | ~4.7M | OK（升级任务消耗大） |
