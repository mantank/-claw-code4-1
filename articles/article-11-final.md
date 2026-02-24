# 第11篇终稿

## 标题（3选1，推荐A）

**A. 我让AI帮我雇了第二个AI员工，全程30分钟**
**B. 一个AI装另一个AI：我的一人公司正在自动扩编**
**C. AI员工连上班都需要你开机？那不叫员工，那叫宠物**

---

## 正文

凌晨两点，我发了条消息给002。

没动静。

盯着屏幕等了一分钟，还是没动静。

看了眼旁边的Windows本子，屏幕黑着——自动休眠了。

我叹了口气。这已经是这周第三次了。

---

002是我的第二个AI，每天负责搜X热词、出选题报告、写公众号初稿。

在这之前，它住在我的本地电脑上。

听起来没问题，但你仔细想想这有多荒谬——

我出门开会两小时，002断联。

周末睡到中午，选题报告没人推。

笔记本更新重启，它就在那干等着。

名义上是"全天候AI助手"，实际上是养了一个需要我开机才能上班的宠物。

那天凌晨，我决定把它搬上云服务器。

我自己踩了大半天的坑，整理出一套部署方法。

你照着做，30分钟够了。

---

### 你需要准备什么

一台云服务器，已经在跑001（你的第一个AI）。

没有的话，买一台最基础的2核4G就行，我两个AI加一个代理，内存还剩700MB。

---

### 第一步：创建002的独立工作目录

002不能和001共用同一个目录，不然配置会打架。

```bash
mkdir -p ~/.openclaw-002/workspace
```

然后把001 workspace里的几个核心文件复制给它，这是002的"入职材料"：

```bash
cp ~/.openclaw/workspace/SOUL.md ~/.openclaw-002/workspace/
cp ~/.openclaw/workspace/templates/writing-style-guide.md ~/.openclaw-002/workspace/templates/
cp ~/.openclaw/workspace/sop/wechat-content-sop.md ~/.openclaw-002/workspace/sop/
```

写作风格指南和SOP一定要同步过去，否则002上来就写出一堆AI腔。

---

### 第二步：写002的配置文件

在 `~/.openclaw-002/` 下新建 `openclaw.json`：

```json
{
  "gateway": {
    "port": 18790,
    "host": "0.0.0.0"
  },
  "model": "dashscope/qwen-plus",
  "plugins": {
    "entries": {
      "telegram": {
        "enabled": true,
        "token": "你的002 Bot Token"
      }
    }
  }
}
```

两个关键点：
- 端口用18790，001用的18789，错开
- `telegram.enabled` 必须写 `true`，不写的话Bot收不到消息

---

### 第三步：写systemd服务，让它开机自启

新建文件 `/etc/systemd/system/openclaw-002.service`：

```ini
[Unit]
Description=OpenClaw 002 Gateway
After=network.target

[Service]
Environment=OPENCLAW_STATE_DIR=/root/.openclaw-002
ExecStart=/usr/bin/openclaw gateway start
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

`OPENCLAW_STATE_DIR` 这个环境变量是关键——告诉002去哪里找自己的配置，不设的话它会跑去用001的目录。

然后启动：

```bash
systemctl daemon-reload
systemctl enable openclaw-002
systemctl start openclaw-002
```

---

### 第四步：验证是否跑通

```bash
systemctl status openclaw-002
```

看到 `active (running)` 就对了。

然后去Telegram，找到002的Bot，发一条消息，它应该会回。

两个AI都在跑了。

---

### 我踩的坑，你不用踩

**坑1：Grok API返回403**

如果002需要调用Grok的X搜索，直接发请求会被403拦截。

机房IP被Cloudflare标记成爬虫，不管你有没有API key，直接拒之门外。

解法：在服务器上装Mihomo代理，让Grok请求绕一道出去。

```bash
# 装好Mihomo之后，请求前加这个环境变量
HTTPS_PROXY=http://127.0.0.1:7890 curl https://api.x.ai/...
```

**坑2：Clash TUN模式会把SSH也劫了**

我一开始想用本地电脑的梯子给服务器中转，结果Clash开了TUN模式，把SSH连接本身都劫持了，怎么都连不上。

最干净的方案：代理装在服务器本地，完全独立，不依赖你自己的电脑。

**坑3：VSCode Remote SSH不能常驻**

装完想连上去看看文件，没问题。

但别一直挂着——VS Code Server会吃掉1.1GB内存，002的响应会从秒回变成等3秒。

验收完立刻断。

---

### 搬完之后，是什么感觉

今天早上，我洗完澡回来，手机弹了条Telegram消息：

「【002·选题日报】AI Agent调度器爆火，搜索量本周+120%...」

它自己搜的，自己整理的，发来时我还没开电脑。

这才叫员工。

之前那个需要我帮它开机的，那是宠物。

---

一人公司不是一个人干所有事。

是想清楚哪些事，可以不用你干。

002现在每天早上九点准时推选题，我的工作变成：扫一眼，决定写哪篇。

部署这件事本身不难，30分钟搞定。

难的是在凌晨两点又一次发消息没有回音时，意识到该换个活法了。

---

📌 三个关键点别忘：

- `OPENCLAW_STATE_DIR` 环境变量必须设，否则002会和001配置打架
- 需要调用Grok API的，服务器上装Mihomo代理，不然403
- VS Code Remote SSH验收完立刻断，不能常驻

如果你也在深夜折腾AI，关注「深夜开发者LND」。
我先踩坑，你少走弯路。

下篇预告：《从选题到排版，AI自动写完一篇公众号文章——我的完整流水线》
