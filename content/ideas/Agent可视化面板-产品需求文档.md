# Agent可视化管理面板 · 产品需求文档

> 状态：调研完成，技术方案已明确
> 作者：旭 + 001
> 更新：2026-03-11

---

## 一句话描述

一个网页控制台，实时显示所有数字员工在干什么，并且可以直接在页面上发任务、换模型、重启——不只是"看"，是真正的"操控大屏"。

---

## 核心体验（旭的目标）

打开网页，看到4张卡片：

- 零零壹 | 状态：正在回复消息 | 今日12万token | [发任务] [换模型] [查日志]
- 零零贰 | 状态：写稿中，预计3分钟 | 今日8万token | [发任务] [换模型] [重启]
- 零零叁 | 状态：空闲 | 上次任务21:00 | [发任务] [查日志]
- 零零肆 | 状态：整理场景案例 1/10 | [发任务] [重启]

**每张卡片的操作：**
- 发任务 → 输入框，直接发消息给这个Agent，不用打开Telegram
- 换模型 → 下拉选，即时生效
- 重启 → 重启Gateway，异常时一键恢复
- 查日志 → 弹出最近50条对话

---

## 竞品调研结论（2026-03-11）

### Star-Office-UI（已实测）

- GitHub：https://github.com/ringhyacinth/Star-Office-UI
- 星数：4241⭐，Twitter 10万+阅读
- **技术架构：**
  - 后端：Python Flask，端口19000，管理 `state.json` 状态文件
  - 前端：HTML/CSS/JS，像素风格地图，轮询后端API刷新Agent位置
  - Agent接入：`office-agent-push.py` 脚本，每15秒POST一次状态到后端
  - 状态字段：`state`（idle/writing/researching/executing/error）+ `detail`（文字描述）
  - 加入方式：join-key机制，支持多Agent同时在线
  - 昨日小记：读取 `memory/YYYY-MM-DD.md` 文件，脱敏后展示在界面
  - 生图功能：接入Gemini API，可以AI生成像素风背景
- **已部署：** http://127.0.0.1:19000（本地），临时公网：biography-soldier-horizon-chairman.trycloudflare.com
- **四个Agent已接入：** 001/002/003/004全部在线
- **不足：** 只能"看"，不能"操控"——没有发任务、换模型、重启等功能

### 旭想要的 vs Star-Office-UI 的差距

| 功能 | Star-Office-UI | 旭想要的 |
|------|---------------|---------|
| 状态可视化 | ✅ 像素地图 | ✅ 卡片或地图均可 |
| 实时刷新 | ✅ 轮询 | ✅ WebSocket更好 |
| 发任务给Agent | ❌ | ✅ 必须有 |
| 换模型 | ❌ | ✅ 必须有 |
| 重启Agent | ❌ | ✅ 必须有 |
| 查看日志 | ❌ | ✅ 必须有 |
| Token用量统计 | ❌ | ✅ 必须有 |

---

## 技术实现方案

### 状态显示层（已有，Star-Office-UI已实现）

```
Agent推送脚本 → POST /agent-push → 后端更新state → 前端轮询展示
```

每个Agent的推送脚本读取 `state.json`，每15秒推送一次状态到展示后端。

### 操控层（需要新增，核心差距）

OpenClaw Gateway已经暴露了完整API，可以直接调用：

**发任务给Agent：**
```
POST http://127.0.0.1:18789/api/sessions/main/send
Body: {"message": "帮我写一篇关于xxx的文章"}
```

**查看当前会话/日志：**
```
GET http://127.0.0.1:18789/api/sessions
GET http://127.0.0.1:18789/api/sessions/:id
```

**实时事件订阅（WebSocket）：**
```
WS ws://127.0.0.1:18789/api/events
→ 实时推送Agent输出，不用轮询
```

**换模型：**
```
修改 /root/.openclaw-XXX/openclaw.json → model.primary
然后 systemctl --user restart openclaw-XXX-gateway
```

**重启Agent：**
```
systemctl --user restart openclaw-001-gateway
systemctl --user restart openclaw-002-gateway
...
```

各Agent端口：001=18789, 002=18790, 003=18791, 004=18792

### 完整架构（目标版本）

```
[网页控制台]
    ↕ 查询状态、发任务、换模型
[中间层后端]（可以复用Star-Office-UI的Flask，加接口）
    ↕ 调用OpenClaw API         ↕ systemctl命令
[OpenClaw 001-004 Gateway]    [系统服务管理]
```

---

## 功能清单

### MVP必须有（先做这些）

| 功能 | 实现方式 | 难度 |
|------|---------|------|
| Agent状态卡片 | 读Star-Office-UI的 `/agents` | 低 |
| 实时状态刷新 | WebSocket订阅OpenClaw事件流 | 中 |
| 发任务输入框 | POST到对应Gateway `/api/sessions/main/send` | 低 |
| 重启Agent按钮 | 后端执行systemctl restart | 低 |
| 查看最近对话 | GET `/api/sessions` 拉历史 | 低 |

### 二期功能

| 功能 | 实现方式 |
|------|---------|
| Token用量统计 | 读session文件，统计usage字段 |
| 换模型下拉框 | 修改openclaw.json + 重启 |
| Cron管理 | 调用OpenClaw Cron API |
| 故障告警 | 心跳检测，挂了推Telegram通知 |

---

## 开发路径

### 最小MVP（1-2天，自己用）

基于Star-Office-UI加一个"操控侧边栏"：
1. 每张Agent卡片加"发任务"输入框
2. 加"重启"按钮（调后端接口执行systemctl）
3. 加"查日志"按钮（拉最近10条对话）

**这个版本就能解决旭"不用打开Telegram也能给Agent发任务"的核心需求。**

### 完整版（1-2周，可对外）

独立开发控制台，脱离Star-Office-UI的像素风格：
- 深色卡片式UI，更专业
- WebSocket实时推送，不用轮询
- 多用户支持（别人也能管自己的Agent团队）
- 开源，可以SaaS

---

## 放在哪

**先选项C（自己用）：** 在Star-Office-UI里加操控功能，不需要上线，验证体验
**再考虑选项B（独立产品）：** 如果自己用了觉得值，做成工具站对外开放

---

## 下一步

- [ ] 决定：在Star-Office-UI基础上改 or 从头写
- [ ] MVP：给每张卡片加"发任务"输入框（1天）
- [ ] 验证：旭自己用，看有没有比Telegram更顺手
- [ ] 决定是否对外开放

---

*Star-Office-UI已部署，四个Agent已接入，下一步加操控功能*
