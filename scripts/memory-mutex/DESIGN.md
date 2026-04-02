# 记忆互斥系统 — 设计规范

## 背景
多 Agent（001/002/003/004）共享同一个 memory/ 目录。
如果不协调，可能出现：
- 两个 Agent 同时写同一天日记 → 互相覆盖
- 同一事件被多次记录 → facts.md 重复
- 主题竞争导致写入丢失

## 核心机制：主题锁

### 文件结构
```
memory/.mutex/
  <topic>.lock    # 内容：agent_id
```

### 可用 Topic（预定义）
- `daily-YYYY-MM-DD` — 某天的日记（每天一把锁）
- `facts` — 事实库（facts.md 写入前需锁 facts）
- `team-status` — 团队状态快照
- `project-<name>` — 某项目进展

### API

**获取锁：**
```bash
bash scripts/memory-mutex/lock.sh <topic> <agent_id>
# 成功 → ACQUIRED
# 失败 → HELD_BY: <owner>
```

**释放锁：**
```bash
bash scripts/memory-mutex/unlock.sh <topic> <agent_id>
```

**去重检查：**
```bash
bash scripts/memory-mutex/dedup.sh <topic> <content_snippet>
# 重复 → DUPLICATE
# 新内容 → NEW
```

## 使用流程

Agent 写日记前：
```bash
# 1. 尝试获取今日日记锁
if lock.sh "daily-$(date +%Y-%m-%d)" "001"; then
    # 2. 去重检查
    if dedup.sh "daily" "$SOME_FACT"; then
        echo "已记录，跳过"
    else
        echo "$FACT" >> memory/$(date +%Y-%m-%d).md
    fi
    # 3. 释放锁
    unlock.sh "daily-$(date +%Y-%m-%d)" "001"
else
    echo "另一个Agent正在写，等待后重试"
fi
```

## 限制
- 锁基于文件，不支持分布式（多台机器）
- 不支持锁超时自动释放（需外部 cron 清理 stale 锁）
- 目前为单 workspace 设计（/root/.openclaw/workspace）

## 待扩展
- [ ] 锁超时自动释放（防止 Agent 崩溃后锁残留）
- [ ] facts.md 结构化存储（每条事实带 timestamp + source agent）
- [ ] 与 memory-extractor skill 集成
