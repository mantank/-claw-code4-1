# 🤖 手把手教你部署私人AI助手！普通人也能搞定

> 小红书图文版 · 共6张图

---

## 📱 图1：封面/引子

**标题：我花3小时，给自己搞了个24小时在线的AI助手 🔥**

姐妹们！！！
我不是程序员❌ 但昨晚真的自己动手
把AI助手部署到了手机Telegram上 📱

现在随时随地跟AI聊天
不用开网页、不用等回复
就像有个超聪明的朋友 24小时秒回你 💬

往下看👇 我把踩的坑全告诉你！

---

## 🛠️ 图2：你需要准备什么

**部署前先备好这4样东西 📋**

✅ 一台Linux服务器（腾讯云/阿里云都行，最便宜的够用）
✅ Anthropic API Key（去 console.anthropic.com 注册）
✅ Telegram Bot Token（找 @BotFather 创建，很简单）
✅ 你自己的 Telegram ID（@userinfobot 一查就有）

💡 小tips：
先别选最贵的模型！
Sonnet 4.5 日常完全够用
等跑通了再升级 🚀

---

## 💻 图3：安装三步走

**核心操作就3条命令 🎯**

第一步：装 Node.js
```
dnf install -y nodejs npm
```

第二步：装 Git
```
dnf install -y git
```

第三步：装 OpenClaw
```
npm install -g openclaw@latest
```

⚠️ 中间有黄色警告别慌！
看到 `added XXX packages` 就是成功了 ✅

---

## ⚙️ 图4：配置连接

**一行命令搞定配置 🔧**

运行：
```
openclaw onboard
```

会弹出菜单让你填4个东西：
1️⃣ 选模型 + 填API Key
2️⃣ 填 Telegram Bot Token
3️⃣ 填你的 Telegram ID
4️⃣ 工作目录（默认就行）

然后给Bot发条消息
它会回一个配对码
在服务器上运行：
```
openclaw pairing approve telegram 配对码
```

搞定！可以开聊了 🎉

---

## 🚨 图5：我踩过的4个坑

**避坑指南（帮你省2小时）⏰**

❌ 坑1：Node.js装不上
→ OpenCloudOS用 `dnf install` 手动装

❌ 坑2：npm报错找不到git
→ 别忘了先 `dnf install -y git`

❌ 坑3：API Key 404报错
→ 用curl测一下key是否有效
→ 不行就重新生成一个

❌ 坑4：发消息没反应
→ 检查有没有跑 approve 配对命令
→ `openclaw doctor` 诊断一下

---

## 🎯 图6：部署完能干嘛 + 常用命令

**恭喜你！现在你有了一个24h在线的AI员工 🤖**

它能帮你：
📝 写文案、改文章
📊 分析数据、做调研
💡 头脑风暴、出方案
🔍 搜索信息、整理资料
⏰ 设定时提醒你

**记住这几个命令：**
- `openclaw status` → 看状态
- `openclaw gateway restart` → 重启
- `openclaw logs --follow` → 看日志
- `openclaw doctor` → 出问题先跑这个

---

🏷️ #AI助手 #OpenClaw #AI部署教程 #普通人学AI #效率工具 #Telegram机器人 #AI实战
