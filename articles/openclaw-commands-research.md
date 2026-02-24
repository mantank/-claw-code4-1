# OpenClaw命令大全 — 选题预研素材

> 来源：官方文档 https://docs.openclaw.ai/tools/slash-commands + CLI help
> 整理时间：2026-02-25

---

## 一、Telegram斜杠命令（日常最常用）

### 🔥 救命级（出问题第一时间用）
| 命令 | 作用 | 真实场景 |
|------|------|---------|
| `/new` | 开新会话 | thinking block报错连弹4次，发/new秒恢复 |
| `/stop` | 停止当前回复 | AI回复太长或跑偏了，立刻打断 |
| `/restart` | 重启Gateway | AI完全无响应时的终极手段 |

### ⚡ 效率级（日常提效）
| 命令 | 作用 | 真实场景 |
|------|------|---------|
| `/status` | 查看状态（模型/token/会话） | 想知道今天烧了多少token |
| `/model <名字>` | 切换模型 | 从Sonnet切到Opus处理复杂任务 |
| `/model list` | 列出所有可用模型 | 不记得模型名字时用 |
| `/new <模型名>` | 开新会话+指定模型 | `/new opus` 直接用Opus开新对话 |
| `/compact` | 压缩上下文 | 对话太长快超限时，手动压缩 |
| `/usage tokens` | 显示每次回复的token用量 | 监控成本 |
| `/usage cost` | 显示本地成本统计 | 看花了多少钱 |

### 🧠 高级调控
| 命令 | 作用 | 说明 |
|------|------|------|
| `/think <级别>` | 调整思考深度 | off/minimal/low/medium/high/xhigh |
| `/reasoning on` | 显示推理过程 | 看AI怎么想的（⚠️群聊慎用，会暴露内部思考） |
| `/reasoning off` | 关闭推理显示 | 默认关，省屏幕空间 |
| `/verbose on` | 详细模式 | 调试用，显示工具调用细节 |
| `/elevated on` | 提权模式 | 允许AI执行更多系统操作 |
| `/exec` | 查看/修改执行权限 | 控制AI能不能跑命令 |

### 📋 会话管理
| 命令 | 作用 |
|------|------|
| `/whoami` | 查看你的sender ID |
| `/context detail` | 查看上下文占用详情（每个文件/工具占多少） |
| `/export` | 导出当前会话为HTML |
| `/subagents list` | 查看正在跑的子Agent |
| `/kill all` | 杀掉所有子Agent |

### 🎙️ 语音
| 命令 | 作用 |
|------|------|
| `/tts always` | 所有回复都转语音 |
| `/tts off` | 关闭语音 |
| `/tts tagged` | 只有AI标记的才转语音 |

### 📱 多平台
| 命令 | 作用 |
|------|------|
| `/dock-telegram` | 切换回复到Telegram |
| `/dock-discord` | 切换回复到Discord |
| `/activation mention` | 群聊中只@才回复 |
| `/activation always` | 群聊中所有消息都回复 |

### 🔧 管理员级（需要开启config/debug）
| 命令 | 作用 | 前提 |
|------|------|------|
| `/config show` | 查看配置 | 需 commands.config: true |
| `/config set <key>=<value>` | 修改配置（写入磁盘） | 同上 |
| `/debug set <key>=<value>` | 运行时临时覆盖 | 需 commands.debug: true |
| `/debug reset` | 清除所有临时覆盖 | 同上 |
| `/bash <命令>` | 直接跑shell命令 | 需 commands.bash: true |

---

## 二、CLI命令（服务器端）

### Gateway管理
```
openclaw gateway start          # 启动
openclaw gateway stop           # 停止
openclaw gateway restart        # 重启
openclaw health                 # 健康检查
openclaw status                 # 查看频道状态+最近会话
openclaw doctor                 # 一键体检
openclaw logs                   # 查看日志
```

### 模型管理
```
openclaw models list            # 列出所有模型
openclaw models auth            # 管理模型认证
openclaw models aliases         # 管理模型别名
openclaw models fallbacks       # 管理fallback顺序
```

### 定时任务
```
openclaw cron list              # 列出所有cron
openclaw cron add               # 添加新cron
openclaw cron run <id>          # 手动跑一次
openclaw cron disable <id>      # 禁用
openclaw cron enable <id>       # 启用
openclaw cron rm <id>           # 删除
openclaw cron runs --id <id>    # 查看运行历史
```

### 频道管理
```
openclaw channels list          # 列出已配置频道
openclaw channels status        # 查看频道状态
openclaw channels add           # 添加频道
openclaw channels login         # 登录频道（如WhatsApp扫码）
```

### 会话管理
```
openclaw sessions               # 列出会话
openclaw sessions cleanup       # 清理过期会话
```

### 其他
```
openclaw configure              # 交互式配置向导
openclaw update                 # 更新OpenClaw
openclaw skills list            # 列出已安装技能
openclaw memory search <query>  # 搜索记忆文件
openclaw dashboard              # 打开控制面板
openclaw security               # 安全审计
```

---

## 三、文章写作角度

### 开头素材（今天真实踩坑）
- thinking block报错连弹4次，不知道怎么恢复
- 系统自动从Sonnet切到Opus，但旭不知道为什么
- 旭问"挂了？"——其实只要发/new就能恢复

### 核心卖点
- 大部分用户只会打字聊天，不知道还有30+个命令
- "你和高手的差距，就在这些命令里"
- 分层：救命级→效率级→高级→管理员级

### 配图方案
- Telegram命令菜单截图
- /status返回结果截图
- /model list模型列表截图
- 命令速查卡（Canva做）

---

## 四、旭今天踩坑的真实timeline

1. 23:32 — thinking block报错，连弹4次 "LLM request rejected: thinking blocks cannot be modified"
2. 23:33 — 旭发"嗯？"，还是报错
3. 23:34 — 旭发"嗯 挂了？"，还是报错  
4. 23:40 — 系统自动切换模型（Sonnet→Opus），恢复正常
5. 如果旭当时知道发/new，10秒就恢复了

这个timeline就是文章最好的开头。
