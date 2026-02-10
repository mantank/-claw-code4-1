# 折腾了一晚上，终于在 Linux 服务器上把 OpenClaw 跑起来了

> 我不是程序员。但昨晚花了大概三个小时，把自己的 AI 助手部署到了 Telegram 上。踩了不少坑，全记下来了。

---

## 先说 OpenClaw 是什么

简单讲：装好 OpenClaw，你就有了一个 24 小时在线的私人 AI 助手 Bot。

它是个开源框架，能把 Claude、GPT 这些大模型接到 Telegram、WhatsApp 上。不用开网页，手机上随时跟 AI 聊。

---

## 我的环境

腾讯云 OpenCloudOS 服务器，配置不高，跑这个够用。

部署前准备好这几样东西：
- Linux 服务器一台
- Anthropic API Key（去 console.anthropic.com 申请）
- Telegram Bot Token（找 @BotFather 创建）
- 你自己的 Telegram 用户 ID

---

## 开始折腾

### 装 Node.js —— 第一个坑

OpenClaw 跑在 Node.js 上，所以得先装。

**踩坑：** 官方安装脚本跑到一半报错了，说不支持当前系统。我用的 OpenCloudOS 虽然是 RPM 系的，但 NodeSource 的脚本没认出来。

最后手动装的：

```bash
dnf install -y nodejs npm
```

或者用 nvm，兼容性更好：

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install --lts
```

### 装 Git —— 第二个坑

npm 装 OpenClaw 的时候直接报错了：`npm error path git errno -2`

原因很简单，系统没装 git：

```bash
dnf install -y git
```

### 装 OpenClaw

```bash
npm install -g openclaw@latest
```

中间会有一堆黄色的 deprecated 警告，别管它，看到 `added XXX packages` 就行。

---

## 配置

```bash
openclaw onboard
```

会弹出交互式菜单，主要填四个东西：

1. **模型和 API Key** — 选模型，填 Anthropic 的 Key
2. **Telegram Bot Token** — BotFather 给你的那串
3. **你的 Telegram ID** — 用 @userinfobot 查
4. **工作目录** — 默认就行

### 模型怎么选？

| 模型 | 输入/输出价格 | 我的体验 |
|------|-------------|---------|
| Opus 4.6 | $5/$25 | 最强，但需要高等级 API 账户 |
| Opus 4.5 | $5/$25 | 旗舰，性价比高 |
| Sonnet 4.5 | $3/$15 | 日常够用，推荐先用这个试 |

建议：先拿 Sonnet 4.5 跑通流程，确认没问题再换 Opus。

### 第三个坑：API Key 404

配好之后给 Bot 发消息，回了个 `HTTP 404: not_found_error`。

折腾了半天，发现是 Key 的问题。用 curl 直接测最快：

```bash
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: 你的KEY" \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"model":"claude-sonnet-4-5-20250929","max_tokens":100,"messages":[{"role":"user","content":"hello"}]}'
```

返回 `authentication_error` 就是 Key 有问题，去重新生成一个。

---

## 配对 Telegram

第一次给 Bot 发消息，它会回一串配对码，类似：

```
Pairing code: KW39NZUZ
```

回到服务器上跑：

```bash
openclaw pairing approve telegram KW39NZUZ
```

搞定。之后就能正常对话了。

---

## 常用命令

用得最多的几个：

```
openclaw status          # 看运行状态
openclaw gateway restart # 重启
openclaw logs --follow   # 看实时日志
openclaw doctor          # 出问题先跑这个
npm update -g openclaw   # 更新版本
```

---

## 几个已知的限制

**微信公众号文章读不了。** OpenClaw 用浏览器访问公众号文章会被微信拦截，要验证码。目前没好办法，只能手动复制内容给它。

**Telegram 默认英文。** 点这个链接一键换中文：[简体中文](https://t.me/setlanguage/zh-hans-raw)

---

## 最后

整个过程顺利的话 30 分钟，算上踩坑大概两三个小时。

主要卡点就四个：
1. **系统兼容** — OpenCloudOS 得手动装 Node.js 和 Git
2. **API Key** — 一定要先用 curl 测一下，别瞎猜
3. **模型权限** — 不是所有 Key 都能用 Opus，先拿 Sonnet 试
4. **配对** — 别忘了在服务器上跑 approve 命令

部署好之后，你就有了一个 24 小时在线、随叫随到的 AI 助手。

值得折腾。
