# 第13篇草稿｜OpenClaw 斜杠命令完全手册

> 类型：B类 工具实战·收藏型
> 状态：草稿待润色
> 字数：约2400字

---

## 标题候选

A. 《收藏这一篇就够了——OpenClaw 全命令大全（持续更新）》⭐ 推荐
B. 《OpenClaw 斜杠命令完全手册：50+命令按场景分类，拿走即用》
C. 《用 OpenClaw？这些命令你迟早用得上——全场景命令大全》

---

## 正文

Telegram 输入框里打一个 `/`，会弹出一个命令列表。

大多数人看一眼，关掉，继续聊天。

但这些命令，是 OpenClaw 真正的控制台。

用好它们，你可以在一秒内切换模型、让 AI 停下来重想、开关推理模式、管理定时任务……不用写一大段提示词，一行命令搞定。

这篇文章，把所有斜杠命令按使用场景分类，每个命令说清楚是干什么的。不用记，收藏备查就行。

---

> **怎么用斜杠命令？**
> Telegram 对话框输入 `/`，自动弹出补全列表，点击即用。
> 命令后面跟参数直接空格隔开，例如 `/think high`。
> 大多数命令单独发送；少数命令（指令型）可以嵌在句子里，例如 `/model opus 帮我写一篇文章`。

---

## 一、🔥 高频必用（先记这几个）

这6个命令，每天都会用到，新手先掌握这里。

---

`/status`
查看当前状态：用的什么模型、消耗了多少 token、本次会话花了多少钱、推理模式是否开启。Claude Max 包月有用量限制，这个命令帮你随时掌握余量。

---

`/reset`
清空当前对话的上下文，重新开始。
AI 有上下文记忆，聊久了前面的内容会干扰后续回答。切换话题前 `/reset` 一下，让 AI 从空白开始思考。注意：只清上下文，不影响工作区文件和记忆。

---

`/new`
新建一个全新的会话，原有对话保留可切回。
跟 `/reset` 的区别：reset 是清空当前对话，new 是开一个新窗口。同时处理多件不相关的事时用，互不干扰。`/new opus` 还能在新建的同时直接指定模型。

---

`/stop`
立刻中止 AI 正在生成的内容。
让 AI 写文章，写到一半发现方向不对，不用等它写完——`/stop` 打断，重新说需求。

---

`/model`
切换模型，立刻生效。
发送 `/model` 弹出可用模型列表，选一个即切换。日常问答用轻量模型省用量，复杂任务切强力模型，随时切，不影响对话历史。

---

`/think`
控制 AI 的思考深度。
参数：`off` / `minimal` / `low` / `medium` / `high` / `xhigh`
别名：`/thinking`、`/t`
写简单内容设 `low`，分析复杂问题设 `high`，日常聊天设 `off`。思考越深，回答越准，但 token 消耗也更多。

---

## 二、🧠 模型与思考控制

---

`/model <模型名>`
切换当前会话使用的模型。支持模型别名、`provider/model` 格式、或模糊匹配提供商名称。
别名：`/models`

---

`/reasoning`
开关推理可见模式。
参数：`on` / `off` / `stream`
`on`：AI 推理过程单独发一条消息（前缀 `Reasoning:`）；`stream`：Telegram 上实时显示推理草稿。⚠️ 群聊中谨慎开启，会暴露内部推理过程。
别名：`/reason`

---

`/think <级别>`
动态设置思考深度（见高频命令）。

---

`/verbose`
开启详细输出模式，显示工具调用失败的完整信息。
参数：`on` / `full` / `off`
主要用于调试，正常使用保持 `off`。
别名：`/v`

---

`/elevated`
控制提权执行权限。
参数：`on` / `off` / `ask` / `full`
`full` 跳过所有 exec 审批直接执行。普通用户保持 `ask`（执行前询问确认）即可。
别名：`/elev`

---

`/exec`
查看或设置代码执行环境。
参数：`host=sandbox|gateway|node`、`security=deny|allowlist|full`、`ask=off|on-miss|always`
直接发 `/exec` 查看当前设置。

---

`/queue`
控制消息队列模式。
支持去抖动（`debounce:2s`）、消息上限（`cap:25`）、溢出处理（`drop:summarize`）等参数。
发 `/queue` 查看当前设置。

---

## 三、📊 状态与信息查看

---

`/status`
查看当前会话状态（见高频命令）。

---

`/whoami`
查看你自己的发送者 ID（频道账号标识）。
别名：`/id`

---

`/context`
解释当前上下文的构成：每个文件、工具、技能和系统提示占用了多少 token。
参数：`list` / `detail` / `json`
排查"上下文太满"或"AI 忘事"时用。

---

`/usage`
控制每次回复后显示的用量信息。
参数：`off` / `tokens` / `full` / `cost`
`cost` 会从本地日志打印当前会话总费用估算。

---

`/help`
列出所有可用的斜杠命令。

---

`/commands`
同 `/help`，列出命令列表。支持嵌入句子使用（inline shortcut）。

---

## 四、💬 对话与上下文管理

---

`/reset`
清空上下文（见高频命令）。

---

`/new`
新建会话（见高频命令）。

---

`/compact`
手动触发上下文压缩，保留关键信息、删除冗余历史。
可在后面加压缩指令，例如 `/compact 保留所有代码片段`。
上下文快满时用，比 `/reset` 更温和——不是清空，是精简。

---

`/session ttl <时长|off>`
设置当前会话的存活时间（TTL）。
例如 `/session ttl 24h` 设置24小时后自动过期。`off` 关闭 TTL。

---

`/stop`
中止生成（见高频命令）。

---

## 五、🎙️ 语音与内容输出

---

`/tts`
控制语音播报行为。
参数：`off` / `always` / `inbound` / `tagged` / `status` / `provider` / `limit` / `summary` / `audio`
`always`：所有回复都转语音；`tagged`：只有带标记的回复转语音。
Discord 上对应命令为 `/voice`（Discord 保留了 /tts 名称）。

---

`/export`
将当前会话导出为 HTML 文件，包含完整对话记录和系统提示。
别名：`/export-session`
参数：指定输出路径，默认保存到 workspace 目录。

---

## 六、🤖 Agent 与子任务管理

---

`/subagents`
管理当前会话的子 Agent。
参数：`list` / `kill` / `log` / `info` / `send` / `steer` / `spawn`
查看正在运行的子任务、发送指令、终止任务都在这里。

---

`/agents`
列出当前会话绑定的所有 thread 级 Agent。

---

`/kill <id|#|all>`
立刻终止一个或所有正在运行的子 Agent，无需确认。
`/kill all` 一键清场。

---

`/steer <id|#> <消息>`
向正在运行的子 Agent 发送引导指令。
如果 Agent 正在执行中，立刻注入新指令；如果无法注入，则中止当前任务并用新指令重启。
别名：`/tell`

---

`/focus <目标>`
（Discord 专属）将当前线程绑定到指定 session 或子 Agent。

---

`/unfocus`
（Discord 专属）取消当前线程绑定。

---

## 七、⚙️ 系统与配置管理

---

`/restart`
重启 OpenClaw Gateway。
默认启用，可通过 `commands.restart: false` 关闭此命令权限。

---

`/config`
读写 `openclaw.json` 配置文件。
参数：`show` / `get` / `set` / `unset`
需要在配置中开启 `commands.config: true` 才可用。仅 owner 可执行。

---

`/debug`
运行时临时覆盖配置（不写入磁盘）。
参数：`show` / `set` / `unset` / `reset`
需要 `commands.debug: true` 才可用。调试时用，正常使用不需要。

---

`/bash <命令>`
在宿主机执行 Shell 命令。
别名：`! <命令>`
需要 `commands.bash: true` + `tools.elevated` 权限配置。
执行长任务时配合 `!poll`（查看进度）和 `!stop`（终止）使用。

---

`!poll`
查看后台 bash 任务的输出/状态。接受可选 sessionId 参数。

---

`!stop`
终止正在运行的 bash 任务。

---

## 八、👥 群聊专属命令

---

`/activation`
设置群聊中 AI 的响应触发方式。
参数：`mention`（只有 @ 时回复）/ `always`（任何消息都回复）
群聊中默认建议设为 `mention`，避免 AI 乱插话。

---

`/send`
控制当前频道的消息发送行为。
参数：`on` / `off` / `inherit`
仅 owner 可用。

---

`/allowlist`
管理命令使用白名单。
参数：`list` / `add` / `remove`
控制哪些用户有权限使用斜杠命令。需要 `commands.config: true`。

---

`/approve <id> allow-once|allow-always|deny`
处理 exec 执行审批请求。
当 AI 需要执行某个操作并请求确认时，用这个命令批准或拒绝。

---

`/dock-telegram` / `/dock-discord` / `/dock-slack`
切换 AI 回复的目标频道。
例如在 Telegram 里发 `/dock-discord`，后续回复会发到 Discord。多频道协作时用。

---

## 九、🧩 技能调用

---

`/skill <技能名> [输入内容]`
直接调用一个已安装的 Skill。
例如 `/skill weather 上海` 调用天气 Skill 查上海天气。
Telegram 和 Discord 上 Skill 也会注册为原生命令，直接点击即可。

---

## 快速速查索引

| 场景 | 用这个命令 |
|------|-----------|
| 查用量/费用 | `/status` |
| 换模型 | `/model` |
| 让 AI 深入思考 | `/think high` |
| 清空对话重来 | `/reset` |
| 开新对话窗口 | `/new` |
| 打断 AI 生成 | `/stop` |
| 上下文快满了 | `/compact` |
| 开关推理可见 | `/reasoning on/off` |
| 查谁在执行任务 | `/subagents list` |
| 终止子任务 | `/kill all` |
| 文字转语音 | `/tts always` |
| 导出对话记录 | `/export` |
| 执行 Shell 命令 | `/bash <命令>` |
| 群聊只响应@提及 | `/activation mention` |

---

## 一句话结尾

工具会用和会使，差的不是功能，是信息差。

这张表，消灭信息差。

---

## 写作备注（内部）

- 待补：实际截图（Telegram 弹窗、/status 输出、/think 效果对比）
- 文章可注明"基于 OpenClaw 2026.2.x 版本，持续更新"
- 公众号不能带外链，工具链接引导到评论区
- HKR 自检：H✅ K✅（信息密度极高）R✅（信息差共鸣）

---

*草稿完成 2026-02-25 | 来源：OpenClaw 官方文档 + 源码扒取 | 001整理*
