# 手把手教你部署AI员工——OpenClaw完整部署指南

> 适合人群：想拥有自己AI助手的普通人，不需要编程基础
> 预计耗时：30-60分钟
> 最后更新：2026年2月

---

## 目录

1. [准备工作](#1-准备工作)
2. [买服务器](#2-买服务器)
3. [安装OpenClaw](#3-安装openclaw)
4. [配置Telegram Bot](#4-配置telegram-bot)
5. [配置AI模型](#5-配置ai模型)
6. [启动和测试](#6-启动和测试)
7. [常见问题排查](#7-常见问题排查)

---

## 1. 准备工作

在开始之前，你需要准备这几样东西：

| 需要什么 | 说明 | 费用 |
|---------|------|------|
| 一台云服务器 | 用来24小时运行你的AI助手 | 约30-50元/月 |
| Telegram账号 | 用来跟AI助手聊天 | 免费 |
| AI模型的API Key | 让AI助手有"大脑" | 按使用量付费 |

**简单解释一下这三样东西的关系：**

- **服务器**就像一间办公室，AI助手在里面"上班"
- **Telegram**就像一部对讲机，你通过它跟AI助手说话
- **API Key**就像AI助手的"智商"，没有它AI助手就是个空壳

准备好了？我们开始！

---

## 2. 买服务器

### 选哪家？

推荐两个对新手最友好的：

- **腾讯云轻量应用服务器**：https://cloud.tencent.com/product/lighthouse
- **阿里云轻量应用服务器**：https://www.aliyun.com/product/swas

> 💡 两家都有新用户优惠，第一次买通常几十块钱就能用一年。哪家便宜买哪家。

### 买什么配置？

最低配置就够用了：

- **CPU**：2核
- **内存**：2GB（推荐4GB，运行更流畅）
- **硬盘**：40GB SSD
- **系统**：**Ubuntu 22.04**（重要！选这个，后面的命令才能直接复制用）
- **带宽**：3-5Mbps就够

### 怎么买？（以腾讯云为例）

1. 打开腾讯云官网，注册账号并实名认证
2. 搜索「轻量应用服务器」，点进去
3. 点「立即购买」
4. 地域选离你近的（比如上海、北京、广州）
5. 镜像选「系统镜像」→「Ubuntu 22.04 LTS」
6. 套餐选最便宜的那个
7. 购买时长选你想用多久
8. 付款

### 连接服务器

买好之后，你需要「远程连接」到服务器。就像用遥控器控制电视一样。

**方法一：网页直接连（最简单）**

1. 在腾讯云控制台找到你的服务器
2. 点「登录」按钮
3. 会打开一个黑色窗口（命令行终端），你直接在里面输入命令就行

**方法二：用SSH工具连**

如果你用的是Mac，打开「终端」（在启动台搜索"终端"）。如果你用的是Windows，下载一个叫 [Termius](https://termius.com/) 的软件（免费版就够）。

然后输入：

```bash
ssh root@你的服务器IP地址
```

第一次连接会问你 `yes/no`，输入 `yes` 回车。然后输入密码（就是你买服务器时设置的密码）。

> ⚠️ 输入密码时屏幕上不会显示任何字符（连星号都没有），这是正常的！盲打完密码直接按回车就行。

看到类似 `root@VM-xxxx:~#` 的提示，说明你已经成功登录服务器了！🎉

---

## 3. 安装OpenClaw

现在开始在服务器上安装OpenClaw。跟着下面的步骤，一步步来，每个命令直接复制粘贴到终端里按回车。

### 第一步：更新系统

```bash
apt update && apt upgrade -y
```

> 这条命令的意思是：把服务器上的软件都更新到最新版，就像给手机更新系统一样。会跑一会儿，等它自己跑完。

### 第二步：安装Node.js 22

OpenClaw需要Node.js 22或更新版本来运行。

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs
```

> 第一行：下载Node.js的安装脚本
> 第二行：执行安装

验证一下安装成功了没：

```bash
node --version
```

如果显示 `v22.x.x`（x是具体数字），就说明装好了。

### 第三步：安装OpenClaw

```bash
npm install -g openclaw@latest
```

> 这条命令的意思是：从网上下载并安装最新版的OpenClaw。`-g` 表示安装到全局，这样你在任何地方都能用。

等它跑完（可能需要一两分钟），验证一下：

```bash
openclaw --version
```

显示版本号就说明安装成功了！

### 第四步：运行引导设置向导

这是最关键的一步。OpenClaw有一个很贴心的「引导向导」，会一步步带你完成所有配置。

```bash
openclaw onboard --install-daemon
```

> 这个命令做了两件事：
> 1. 启动配置向导，问你一系列问题（比如用什么AI模型、连什么聊天工具）
> 2. `--install-daemon` 表示把OpenClaw设置成后台服务，这样它会自动开机启动，不会因为你关闭终端就停掉

向导会问你几个问题，别慌，我们一个个来：

**问你选AI模型（Model provider）：**
- 推荐选 **Anthropic**（就是Claude的公司）
- 向导会让你输入API Key，先跳过，我们下一节专门讲怎么获取

**问你连什么聊天渠道（Channel）：**
- 选 **Telegram**
- 向导会让你输入Bot Token，先跳过，我们第4节讲

> 💡 如果向导问的问题你不确定，大部分直接按回车用默认值就行。后面都可以改。

---

## 4. 配置Telegram Bot

### 什么是Telegram Bot？

简单说，就是在Telegram里创建一个"机器人账号"。你跟这个机器人聊天，消息会转发给OpenClaw，OpenClaw再用AI生成回复发回来。

### 第一步：安装Telegram

如果你还没有Telegram：
- 苹果手机：App Store搜索「Telegram」下载
- 安卓手机：Google Play或者到 https://telegram.org 下载
- 电脑：https://desktop.telegram.org

注册需要一个手机号。

### 第二步：找BotFather创建机器人

1. 打开Telegram，点上方的搜索框
2. 搜索 `BotFather`（注意B和F大写）
3. 找到那个有蓝色勾✓（官方认证）的 **@BotFather**，点进去

> ⚠️ 重要！一定要确认是带蓝色认证标志的 @BotFather，不要被冒牌的骗了！

4. 点「Start」或者发送 `/start`
5. 发送 `/newbot`
6. BotFather会问你：给机器人起个名字（display name），比如输入 `我的AI助手`
7. 然后问你设置一个用户名（username），必须以 `bot` 结尾，比如 `my_awesome_ai_bot`

> 💡 用户名是全Telegram唯一的，如果提示已被占用，换一个试试。

8. 创建成功！BotFather会给你一串像这样的 **Token**：

```
123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

**把这串Token复制保存好！这是你机器人的"钥匙"，不要分享给别人。**

### 第三步：可选设置（推荐做）

继续在BotFather里：

1. 发送 `/setprivacy`，选择你的机器人，然后选 `Disable`
   > 这样机器人在群聊里能看到所有消息（如果你想在群里用的话）

2. 发送 `/setjoingroups`，选择你的机器人，然后选 `Enable`
   > 这样别人可以把机器人拉进群

### 第四步：把Token配置到OpenClaw

回到你的服务器终端，有两种方式配置：

**方式一：用环境变量（简单）**

```bash
export TELEGRAM_BOT_TOKEN="你的Token粘贴在这里"
```

> 把 `你的Token粘贴在这里` 替换成BotFather给你的那串Token，注意保留引号。

为了让它开机也能用，把这行加到配置文件里：

```bash
echo 'export TELEGRAM_BOT_TOKEN="你的Token粘贴在这里"' >> ~/.bashrc
source ~/.bashrc
```

**方式二：用配置文件（推荐）**

编辑OpenClaw的配置文件：

```bash
nano ~/.openclaw/openclaw.json
```

> `nano` 是一个文本编辑器。如果提示没有这个文件，它会自动创建一个新的。

在文件里写入（或者找到对应位置修改）：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "你的Token粘贴在这里",
      "dmPolicy": "pairing"
    }
  }
}
```

> `dmPolicy: "pairing"` 的意思是：陌生人给你的机器人发消息时，需要你先批准才行。这是一个安全措施，防止别人随便用你的AI。

然后按 `Ctrl + O` 保存，按 `Enter` 确认，按 `Ctrl + X` 退出编辑器。

---

## 5. 配置AI模型

AI模型就是你助手的"大脑"。目前推荐 **Anthropic（Claude）** 或 **OpenAI（GPT）**。

### 选项一：Anthropic API Key（推荐）

Anthropic的Claude模型是OpenClaw官方推荐的，效果最好。

**获取API Key：**

1. 打开 https://console.anthropic.com
2. 点右上角「Sign Up」注册账号（用邮箱）
3. 注册完登录后，点左边菜单的「API Keys」
4. 点「Create Key」按钮
5. 给Key起个名字，比如 `openclaw`
6. 点「Create」
7. **立刻复制这个Key！它只会显示一次！** 格式类似：`sk-ant-api03-xxxxxxxxxxxx`

**充值：**

新账号通常有一些免费额度。用完了需要在「Billing」里绑定信用卡充值。建议先充$5试试水。

**配置到OpenClaw：**

编辑配置文件：

```bash
nano ~/.openclaw/openclaw.json
```

在配置中加上模型部分（跟前面的Telegram配置合并在一起）：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "你的Telegram-Bot-Token",
      "dmPolicy": "pairing"
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-5"
      }
    }
  }
}
```

然后设置API Key的环境变量：

```bash
echo 'export ANTHROPIC_API_KEY="你的API-Key粘贴在这里"' >> ~/.bashrc
source ~/.bashrc
```

> 把 `你的API-Key粘贴在这里` 替换成你刚复制的那个Key。

### 选项二：OpenAI API Key

如果你更喜欢GPT：

1. 打开 https://platform.openai.com
2. 注册/登录
3. 点左边菜单「API keys」→「Create new secret key」
4. 复制Key（格式类似 `sk-xxxxxxxxxxxx`）

配置方法类似：

```bash
echo 'export OPENAI_API_KEY="你的OpenAI-Key粘贴在这里"' >> ~/.bashrc
source ~/.bashrc
```

配置文件里的模型改成：

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "openai/gpt-4o"
    }
  }
}
```

> 💡 **新手建议：选Anthropic Claude。** 官方推荐，跟OpenClaw配合最好。

---

## 6. 启动和测试

### 启动OpenClaw

如果你在第3步用了 `--install-daemon`，OpenClaw可能已经在运行了。可以这样检查：

```bash
openclaw gateway status
```

如果没在运行，手动启动：

```bash
openclaw gateway start
```

或者前台运行（能看到实时日志，方便排查问题）：

```bash
openclaw gateway --port 18789 --verbose
```

> 前台运行的话，关闭终端窗口就会停止。调试完了记得用 `openclaw gateway start` 启动后台服务。

### 测试：给你的AI助手发消息！

1. 打开Telegram
2. 搜索你创建的那个机器人用户名（比如 `@my_awesome_ai_bot`）
3. 点进去，点「Start」
4. 发一条消息，比如"你好！"

**第一次会收到一个"配对码"（pairing code）**，因为我们设置了 `dmPolicy: "pairing"`。

回到服务器终端，批准配对：

```bash
openclaw pairing approve
```

> 这条命令会批准最近一个等待配对的请求。

批准之后，再给机器人发消息，它就会用AI回复你了！🎉

### 访问控制面板（可选）

OpenClaw还有一个网页控制面板，方便你查看状态和调整设置：

- 如果你在服务器本地：打开浏览器访问 `http://127.0.0.1:18789/`
- 如果你想从外部访问：需要配置Tailscale或SSH隧道（高级用法，以后再说）

---

## 7. 常见问题排查

### ❌ 安装Node.js失败

**现象**：`curl` 命令报错或 `node --version` 没反应

**解决**：
```bash
# 换一种方式安装
apt install -y curl
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs
```

如果还不行，试试直接用包管理器：
```bash
apt install -y nodejs npm
node --version
# 如果版本太低，用n来升级
npm install -g n
n 22
```

### ❌ `npm install -g openclaw` 卡住不动

**原因**：大概率是网络问题，国内访问npm比较慢

**解决**：换成国内镜像源
```bash
npm config set registry https://registry.npmmirror.com
npm install -g openclaw@latest
```

### ❌ Telegram机器人不回复

按这个顺序检查：

1. **Gateway在跑吗？**
   ```bash
   openclaw gateway status
   ```
   如果没在跑，启动它。

2. **Token配对了吗？**
   ```bash
   openclaw gateway --verbose
   ```
   看日志里有没有Telegram相关的报错。

3. **配对批准了吗？**
   第一次给机器人发消息会收到配对码，你需要在服务器上运行 `openclaw pairing approve` 来批准。

4. **API Key配了吗？**
   ```bash
   echo $ANTHROPIC_API_KEY
   ```
   如果什么都没显示，说明环境变量没设好，重新设一下。

### ❌ 报错 `Model is not allowed`

**原因**：配置里的模型名写错了，或者模型没在允许列表里

**解决**：检查配置文件里的模型名称是否正确（区分大小写）。可以用：
```bash
openclaw models list
```
查看所有可用的模型。

### ❌ 服务器重启后OpenClaw没有自动启动

**解决**：
```bash
openclaw onboard --install-daemon
```
这会重新设置自动启动。设置完重启验证一下：
```bash
reboot
# 等一两分钟重新连上服务器
openclaw gateway status
```

### ❌ 报错 `EACCES permission denied`

**解决**：权限问题，运行：
```bash
npm install -g openclaw@latest --unsafe-perm
```

或者如果你不是root用户：
```bash
sudo npm install -g openclaw@latest
```

---

## 进阶提示

🔹 **换模型**：在Telegram里直接发 `/model` 可以切换AI模型
🔹 **加群聊**：把机器人拉进群，在配置里设置群聊规则
🔹 **多渠道**：OpenClaw还支持WhatsApp、Discord、Slack等，配置方法类似
🔹 **看状态**：发 `/status` 给机器人可以查看运行状态
🔹 **健康检查**：`openclaw doctor` 可以自动诊断常见问题

---

## 写在最后

恭喜你！你现在拥有了一个24小时在线的AI私人助手。🦞

它能帮你：
- 回答各种问题
- 帮你写东西、翻译
- 搜索信息
- 甚至帮你写代码（如果你以后学编程的话）

有问题可以去这些地方找帮助：
- 📖 官方文档：https://docs.openclaw.ai
- 💬 Discord社区：https://discord.gg/clawd
- 🐙 GitHub：https://github.com/openclaw/openclaw

Enjoy your AI lobster! 🦞✨
