# DEV-FLOW.md — openclaw-cn 开发协作流程

> 适用范围：所有功能开发、页面改动、内容更新
> 执行者：旭（决策）+ 001（统筹）+ 三剑客（实现）
> 更新时间：2026-03-06

---

## 标准开发流程

```
旭下达指令
    ↓
【第1步】001 写任务描述 → 发给旭确认
    ↓
旭确认 ✅（不确认不开工）
    ↓
【第2步】打备份标签（自动）
    ↓
【第3步】Claude Code 实现核心代码
    ↓
【第4步】Gemini 检查（方向/逻辑/设计层）
    ↓
【第5步】Codex 审核（bug/类型错误/遗漏）
    ↓
【第6步】001 本地 build 验证（必须无报错）
    ↓
【第7步】001 向旭汇报结果（截图/描述变化）
    ↓
旭预览确认 ✅
    ↓
【第8步】push GitHub → Vercel 自动部署
```

---

## 各步骤详细规则

### 第1步：任务描述（001 → 旭）

001 写任务描述，必须包含：

| 字段 | 说明 |
|------|------|
| **做什么** | 用一句话说清功能目标 |
| **改哪些文件** | 列出具体文件路径 |
| **不碰哪些** | 明确不改的文件/功能，防止误改 |
| **验收标准** | 怎么算做完了 |
| **预计风险** | 可能出问题的地方 |

**示例格式：**
```
任务：在右上角添加语言切换按钮（中/英客户端切换）

改动范围：
✅ 改：src/components/Header.astro（加按钮）
✅ 改：src/layouts/BaseLayout.astro（注入切换脚本）
✅ 新增：src/i18n/en.ts（英文翻译字典）
❌ 不碰：src/pages/（不新增路由页面）
❌ 不碰：src/data/site-content.ts（内容数据不动）

验收标准：点击 EN 按钮，导航文字切换为英文；再点切回中文；刷新后语言保持。
预计风险：BaseLayout 注入 JS 可能与现有脚本冲突。
```

旭回复「确认」或提出修改意见后才进入下一步。

---

### 第2步：打备份标签

开工前自动执行：
```bash
git tag backup-$(date +%Y%m%d-%H%M%S)
```

出问题时一键恢复：
```bash
# 查看所有备份标签
git tag | grep backup

# 恢复到某个备份
git checkout backup-20260306-105900

# 或者直接回滚最近一次 commit（安全方式）
git revert HEAD
git push origin main
```

---

### 第3步：Claude Code 实现

- 负责核心代码编写
- 工作目录：`/root/.openclaw/workspace/projects/openclaw-cn`
- 完成后不直接 push，等待审核

---

### 第4步：Gemini 检查（方向层）

检查维度：
- 实现方向是否符合任务描述？
- 有没有超出改动范围（改了不该改的文件）？
- 用户体验是否合理？

---

### 第5步：Codex 审核（代码层）

检查维度：
- TypeScript 类型错误
- 潜在的 runtime 报错
- 遗漏的 edge case
- 代码风格是否和项目一致

---

### 第6步：本地 build 验证

```bash
cd /root/.openclaw/workspace/projects/openclaw-cn
npm run build
```

**规则：build 有任何报错，禁止 push，打回修改。**

---

### 第7步：汇报给旭

001 发消息，包含：
- 改了什么（文件列表）
- 视觉变化描述（或截图）
- build 结果：✅ 无报错 / ❌ 有问题
- 是否准备好 push

旭回复「push」或提出修改意见。

---

### 第8步：push + 部署

```bash
git add -A
git commit -m "类型(范围): 简短描述"
git push origin main
```

Vercel 自动触发部署，约 1-2 分钟后线上更新。

---

## Commit 规范

| 类型 | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | bug 修复 |
| `style` | 样式调整（不影响功能） |
| `content` | 内容/数据更新 |
| `refactor` | 代码重构 |
| `chore` | 构建/配置变更 |

示例：`feat(header): add zh/en language switcher`

---

## 紧急回滚流程

出现线上问题，立刻执行：

```bash
# 方式1：撤销最近一次 commit（推荐，保留历史）
git revert HEAD
git push origin main

# 方式2：回滚到指定备份标签
git checkout backup-20260306-105900 -- .
git commit -m "revert: rollback to backup-20260306-105900"
git push origin main

# 方式3：Vercel 控制台一键回滚到上一个部署版本（最快）
# 打开 vercel.com → 项目 → Deployments → 找上一个版本 → Redeploy
```

**原则：线上出问题先回滚，再查原因，不在生产环境热修复。**

---

## 三剑客分工

| 角色 | 工具 | 负责 |
|------|------|------|
| Claude Code | `claude` | 核心功能实现、组件开发 |
| Gemini | `gemini` | 方案规划、内容生成、设计评审 |
| Codex | `codex` | 代码审查、bug 发现、测试 |
| 001 | OpenClaw | 统筹调度、任务拆解、质量把关 |

---

*本文档随项目迭代更新。有流程问题直接告诉旭，讨论后修改。*

---

## 三剑客 tmux 持久化规则

> 更新：2026-03-06

### 核心原则
**三剑客必须跑在 tmux 里。** 小龙虾（OpenClaw）超时或重启不会影响三剑客的进程。

### tmux session 结构
```
session: sanjian
  window 0: claude-code   ← Claude Code 专用
  window 1: codex         ← Codex 专用
  window 2: gemini        ← Gemini CLI 专用
  window 3: workspace     ← 001 调度/监控用
```

### 每次使用前检查
```bash
tmux ls  # 确认 sanjian session 存在
# 如果不存在，重建：
bash ~/.openclaw/workspace/scripts/start-sanjian.sh
```

### 001 发指令给三剑客的方式
```bash
# 让 Claude Code 执行任务
tmux send-keys -t sanjian:claude-code "claude --dangerously-skip-permissions '你的任务'" Enter

# 让 Gemini 分析
tmux send-keys -t sanjian:gemini "gemini '你的任务'" Enter

# 读取三剑客的输出
tmux capture-pane -t sanjian:claude-code -p
```

### 异常处理
- 小龙虾超时/重启 → tmux session 仍在，三剑客不受影响
- 某个 window 挂了 → `tmux respawn-window -t sanjian:claude-code`
- 整个 session 没了 → 跑 `start-sanjian.sh` 重建
