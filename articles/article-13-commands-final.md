# OpenClaw 斜杠命令完全手册：50+命令按场景分类，收藏备查

> 基于 OpenClaw 2026.2.x 版本 · 持续更新

打开 Telegram，输入 `/`。

弹出一个命令列表，大多数人扫一眼，关掉，继续聊天。

我之前也是这样。

直到有次 AI 在生成一篇很长的文章，写到一半我发现方向全错了——只能干等它写完，再从头解释。

后来我才知道，`/stop` 早就在那里了。

这篇文章，把 OpenClaw 所有斜杠命令整理出来，按使用场景分类，每个命令说清楚干什么用、什么时候用。

<font color="red">**不用记，收藏这篇，遇到问题翻一下就够了。**</font>

---

> **怎么用斜杠命令？**
> Telegram 对话框输入 `/`，自动弹出补全列表，点击即用，不需要手动输入完整命令。
> 命令后面跟参数直接空格隔开，例如 `/think high`。
> 部分命令（指令型）可以嵌在句子里使用，例如 `/model opus 帮我写一篇文章`，会先切换模型再执行任务。

---

## 一、🔥 高频必用——先把这8个练熟

<font color="red">**这8个命令覆盖了日常使用的90%场景，新手先从这里开始。**</font>

---

### `/status`
查看当前状态：正在用什么模型、消耗了多少 token、本次会话估算花了多少钱、推理模式是否开启。

<font color="red">**Claude Max 包月有用量上限，每5小时一个周期。随时发 `/status` 掌握余量，别等限速了才发现。**</font>

---

### `/model`
切换当前使用的模型，立刻生效。

发送后弹出可用模型列表，选一个即切换。也可以直接带参数：`/model sonnet` 或 `/model opus`。

别名：`/models`

> 用法建议：日常问答用轻量模型省用量，写文章、分析复杂问题切强力模型。

---

### `/think`
控制 AI 的思考深度。

参数：`off` / `minimal` / `low` / `medium` / `high` / `xhigh`

别名：`/thinking`、`/t`

<font color="red">**思考越深，回答越准，但 token 消耗也更多。日常聊天设 `off`，需要严谨分析时设 `high`。**</font>

---

### `/reset`
清空当前对话的上下文，AI 从空白状态重新开始。

AI 有上下文记忆，聊久了前面的内容会影响后续回答。切换话题前 `/reset` 一下，避免干扰。

<font color="red">**注意：只清上下文，不影响工作区文件、记忆文件和配置。**</font>

---

### `/new`
新建一个全新的会话，原有对话保留、可以切回去。

跟 `/reset` 的区别：reset 是清空当前对话，new 是另开一个窗口。同时处理多件不相关的事时用。

> 支持直接带模型名：`/new opus` 新建会话的同时切换到 Opus。

---

### `/stop`
立刻中止 AI 正在生成的内容。

<font color="red">**让 AI 写文章，写到一半发现方向不对，不用等它写完——`/stop` 打断，重新说需求。**</font>

---

### `/compact`
手动压缩上下文——保留关键信息，删除冗余历史。

比 `/reset` 更温和：不是清空，是精简。对话历史太长、AI 开始"忘事"时用。

可以加指令：`/compact 保留所有代码片段` 指定压缩时保留哪些内容。

---

### `/reasoning`
开关推理可见模式——让你看到 AI 回答前的思考过程。

参数：`on` / `off` / `stream`

- `on`：AI 的推理过程单独发一条消息（前缀 `Reasoning:`）
- `stream`：Telegram 上实时显示推理草稿（边想边给你看）

别名：`/reason`

> ⚠️ 群聊中谨慎开启，会把内部推理过程暴露给所有人。

---

## 二、🧠 模型与思考控制

---

### `/model <模型名>`
切换模型（详见高频命令）。支持别名、`provider/model` 格式、或提供商名称模糊匹配。

---

### `/think <级别>`
调整思考深度（详见高频命令）。

---

### `/reasoning`
推理过程可见模式（详见高频命令）。

---

### `/verbose`
开启详细输出，显示工具调用的完整日志。

参数：`on` / `full` / `off`

主要用于调试排错，正常使用保持 `off`。

别名：`/v`

---

### `/elevated`
控制 AI 执行操作时的权限级别。

参数：`on` / `off` / `ask` / `full`

- `ask`：AI 每次执行操作前询问确认（推荐默认）
- `full`：跳过所有审批直接执行（高风险操作谨慎用）

别名：`/elev`

---

### `/exec`
查看或设置代码/命令执行环境。

参数：`host=sandbox|gateway|node`、`security=deny|allowlist|full`、`ask=off|on-miss|always`

直接发 `/exec` 查看当前配置。

---

### `/queue`
控制消息队列模式，适合批量处理场景。

支持去抖动（`debounce:2s`）、消息上限（`cap:25`）、溢出处理（`drop:summarize`）。

直接发 `/queue` 查看当前设置。

---

## 三、📊 状态与信息查看

---

### `/status`
查看会话状态（详见高频命令）。支持嵌入句子使用（inline shortcut）。

---

### `/whoami`
查看你自己的发送者 ID（频道账号标识）。

别名：`/id`

---

### `/context`
解释当前上下文的构成：每个文件、工具、技能和系统提示各占了多少 token。

参数：`list` / `detail` / `json`

<font color="red">**AI 开始"忘事"或回答变奇怪时，用 `/context detail` 排查是哪里把上下文撑满了。**</font>

---

### `/usage`
控制每次 AI 回复后显示的用量信息。

参数：`off` / `tokens` / `full` / `cost`

`/usage cost`：打印当前会话从本地日志估算的总费用。

---

### `/help`
列出所有可用的斜杠命令。

---

### `/commands`
同 `/help`，列出命令列表。可以嵌在句子里使用。

---

## 四、💬 对话与上下文管理

---

### `/reset`
清空上下文（详见高频命令）。

---

### `/new`
新建会话（详见高频命令）。

---

### `/compact`
压缩上下文（详见高频命令）。

---

### `/session ttl <时长|off>`
设置当前会话的自动过期时间。

例如：`/session ttl 24h`（24小时后过期）、`/session ttl off`（不过期）。

---

### `/stop`
中止生成（详见高频命令）。

---

### `/export`
将当前会话导出为 HTML 文件，包含完整对话和系统提示。

别名：`/export-session`

默认保存到 workspace 目录，也可以指定路径。

---

## 五、🎙️ 语音与内容输出

---

### `/tts`
控制语音播报行为。

常用参数：
- `always` — 所有 AI 回复都转成语音
- `tagged` — 只有特定标记的回复才转语音
- `off` — 关闭语音
- `status` — 查看当前语音设置
- `provider` — 查看或切换语音提供商

> Discord 上这个命令叫 `/voice`（Discord 官方占用了 `/tts`），但文字命令 `/tts` 依然有效。

---

## 六、🤖 Agent 与子任务管理

---

### `/subagents`
管理当前会话的所有子 Agent。

参数：`list` / `kill` / `log` / `info` / `send` / `steer` / `spawn`

查看正在运行的子任务、发指令、终止任务都在这里。

---

### `/agents`
列出当前会话绑定的所有线程级 Agent。

---

### `/kill <id|#|all>`
立刻终止一个或所有正在运行的子 Agent，无需确认。

<font color="red">**`/kill all` 一键清场，紧急情况下用。**</font>

---

### `/steer <id|#> <消息>`
向正在运行的子 Agent 发送引导指令，中途纠正方向。

- 如果 Agent 正在执行中：立刻注入新指令
- 如果无法注入：中止当前任务，用新指令重启

别名：`/tell`

---

### `/focus <目标>`
（Discord 专属）将当前线程绑定到指定 session 或子 Agent。

---

### `/unfocus`
（Discord 专属）取消当前线程绑定。

---

## 七、⚙️ 系统与配置管理

---

### `/restart`
重启 OpenClaw Gateway。

服务异常或更新配置后用。默认启用，可通过 `commands.restart: false` 关闭权限。

---

### `/config`
读写 `openclaw.json` 配置文件。

参数：`show` / `get` / `set` / `unset`

需要在配置中开启 `commands.config: true` 才可用。仅 owner 执行。

---

### `/debug`
运行时临时覆盖配置（不写入磁盘，重启后失效）。

参数：`show` / `set` / `unset` / `reset`

需要 `commands.debug: true`。调试排错时用，日常不需要。

---

### `/bash <命令>`
在宿主机直接执行 Shell 命令。

别名：`! <命令>`

需要 `commands.bash: true` + `tools.elevated` 权限配置。

长任务配合 `!poll`（查进度）和 `!stop`（终止）使用。

---

### `!poll`
查看后台 bash 任务的输出和运行状态。

---

### `!stop`
终止正在运行的 bash 任务。

---

## 八、👥 群聊专属命令

---

### `/activation`
设置群聊中 AI 的响应触发方式。

参数：`mention` / `always`

<font color="red">**强烈建议群聊设为 `mention`（只有 @ 时才回复），否则 AI 会对所有消息都插话。**</font>

---

### `/allowlist`
管理命令使用白名单——控制谁有权限用斜杠命令。

参数：`list` / `add` / `remove`

需要 `commands.config: true`。

---

### `/approve <id> allow-once|allow-always|deny`
处理 AI 执行操作的审批请求。

当 AI 请求执行某个操作并等待确认时，用这个命令批准或拒绝。

---

### `/send`
控制当前频道的消息发送行为。

参数：`on` / `off` / `inherit`

仅 owner 可用。

---

### `/dock-telegram` / `/dock-discord` / `/dock-slack`
切换 AI 回复的目标频道。

例如在 Telegram 里发 `/dock-discord`，后续回复会路由到 Discord。多平台同时部署时用。

---

## 九、🧩 技能调用

---

### `/skill <技能名> [输入内容]`
直接按名称运行一个已安装的 Skill（技能插件）。

例如：`/skill weather 上海` 调用天气 Skill 查询上海天气。

<font color="red">**当命令槽位不够、技能没出现在列表里时，用 `/skill 名称` 直接调用。**</font>

Telegram 和 Discord 上已安装的 Skill 也会注册为原生命令，直接在 `/` 列表里选。

---

## ⚡ 速查索引表

| 命令 | 一句话描述 | 使用频率 |
|------|-----------|---------|
| `/stop` | 立刻打断 AI 回复 | ⭐⭐⭐⭐⭐ |
| `/reset` / `/new` | 清空对话 / 新建会话 | ⭐⭐⭐⭐⭐ |
| `/status` | 查用量+费用+模型 | ⭐⭐⭐⭐⭐ |
| `/model` | 切换 AI 模型 | ⭐⭐⭐⭐⭐ |
| `/compact` | 压缩上下文不丢记忆 | ⭐⭐⭐⭐⭐ |
| `/think` | 调整 AI 思考深度 | ⭐⭐⭐⭐ |
| `/reasoning` | 显示 AI 推理过程 | ⭐⭐⭐⭐ |
| `/usage` | 控制用量显示方式 | ⭐⭐⭐⭐ |
| `/help` / `/commands` | 显示所有命令 | ⭐⭐⭐⭐ |
| `/context` | 查看 AI 加载了哪些内容 | ⭐⭐⭐⭐ |
| `/subagents` | 管理子 Agent | ⭐⭐⭐ |
| `/steer` / `/tell` | 中途纠正子 Agent 方向 | ⭐⭐⭐ |
| `/kill` | 立刻终止子 Agent | ⭐⭐⭐ |
| `/tts` | 控制语音播报 | ⭐⭐⭐ |
| `/activation` | 群聊响应模式设置 | ⭐⭐⭐ |
| `/skill` | 直接调用技能插件 | ⭐⭐⭐ |
| `/session ttl` | 设置会话过期时间 | ⭐⭐ |
| `/elevated` | 调整执行权限级别 | ⭐⭐ |
| `/approve` | 审批 AI 执行请求 | ⭐⭐ |
| `/allowlist` | 管理白名单 | ⭐⭐ |
| `/config` | 读写配置文件 | ⭐⭐ |
| `/restart` | 重启 Gateway | ⭐⭐ |
| `/bash` / `!` | 服务器执行 Shell 命令 | ⭐⭐ |
| `/verbose` | 开启调试详细输出 | ⭐⭐ |
| `/export` | 导出完整对话记录 | ⭐ |
| `/focus` / `/unfocus` | Discord 线程绑定 | ⭐ |
| `/dock-telegram` 等 | 切换回复目标频道 | ⭐ |
| `/queue` | 消息队列模式 | ⭐ |
| `/whoami` / `/id` | 查自己的账号 ID | ⭐ |
| `/debug` | 临时调试配置覆盖 | ⭐ |

---

## 📌 今日速记三件事

<font color="red">**`/stop` 打断，`/reset` 重来，`/compact` 续命**</font>

调模型用 `/model`，查状态用 `/status`

群聊先设 `/activation mention`，不然它什么都接话

---

## 结尾

30多个命令，真正每天用到的不超过10个。

先把高频那8个练熟——遇到问题再往后翻。

<font color="red">**用 AI 最大的浪费，不是它没能力，是你没把它用到位。**</font>

这张表，消灭信息差。

如果你也在深夜折腾 AI，关注「深夜开发者LND」。

我先踩坑，你少走弯路。

---

*本文基于 OpenClaw 2026.2.x 版本整理，命令来源：官方文档 + 源码核对。版本更新后会同步修订。*
