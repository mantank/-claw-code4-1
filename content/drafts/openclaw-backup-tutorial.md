# OpenClaw数据备份指南——把你的AI员工记忆存到GitHub

> 适合人群：已经部署好OpenClaw的用户，不需要编程基础
> 预计耗时：15分钟
> 最后更新：2026年2月

---

## 目录

1. [为什么要备份](#1-为什么要备份)
2. [准备工作](#2-准备工作)
3. [在服务器上生成SSH Key](#3-在服务器上生成ssh-key)
4. [把SSH Key添加到GitHub](#4-把ssh-key添加到github)
5. [在GitHub创建私有仓库](#5-在github创建私有仓库)
6. [添加.gitignore](#6-添加gitignore)
7. [推送workspace到仓库](#7-推送workspace到仓库)
8. [换服务器时如何恢复](#8-换服务器时如何恢复)
9. [日常同步命令](#9-日常同步命令)

---

## 1. 为什么要备份

你的OpenClaw workspace里存着很多重要的东西：

- **AI的记忆**（MEMORY.md、memory/文件夹）——你和AI聊了那么久，它记住的你的偏好、习惯、之前的对话上下文，这些都在里面
- **配置文件**——你辛辛苦苦调好的各种设置
- **自定义内容**——你写的提示词、技能文件、工具配置

如果服务器突然坏了、到期忘续费、或者你想换一台更好的服务器——**没有备份的话，AI就"失忆"了**。它不再认识你，一切从头开始。

把数据备份到GitHub，好处是：

- ☁️ 数据存在云端，服务器炸了也不怕
- 🔄 换服务器时一条命令就能恢复
- 📝 还能看到每次修改的历史记录

---

## 2. 准备工作

你只需要一个 **GitHub账号**。

如果还没有：

1. 打开 https://github.com
2. 点右上角「Sign up」
3. 输入邮箱、设置密码、起个用户名
4. 按提示完成验证
5. 去邮箱点确认链接

搞定。

---

## 3. 在服务器上生成SSH Key

SSH Key是一把"钥匙"，让你的服务器能安全地和GitHub通信，不用每次都输密码。

登录你的服务器，运行：

```bash
ssh-keygen -t ed25519 -C "你的邮箱@example.com"
```

> 把 `你的邮箱@example.com` 换成你注册GitHub用的邮箱。

然后它会问你几个问题：

```
Enter file in which to save the key (/root/.ssh/id_ed25519):
```
**直接按回车**，用默认位置就好。

```
Enter passphrase (empty for no passphrase):
```
**直接按回车**（不设密码，省事）。再问一次确认，**再按回车**。

现在查看你的公钥（等下要用）：

```bash
cat ~/.ssh/id_ed25519.pub
```

屏幕会显示一长串以 `ssh-ed25519` 开头的文字，**把它整行复制下来**。

> 💡 用鼠标选中整行，右键复制。或者在终端里按 `Ctrl+Shift+C` 复制。

---

## 4. 把SSH Key添加到GitHub

1. 打开浏览器，登录 https://github.com
2. 点右上角你的头像 → 点「**Settings**」
3. 左边菜单找到「**SSH and GPG keys**」，点进去
4. 点绿色按钮「**New SSH key**」
5. **Title** 随便填，比如 `我的OpenClaw服务器`
6. **Key type** 保持默认的 `Authentication Key`
7. **Key** 那个大框框里，粘贴你刚才复制的那一长串公钥
8. 点「**Add SSH key**」

GitHub可能会让你输一次密码确认，输完就添加成功了。

**验证一下连接是否成功**，回到服务器终端：

```bash
ssh -T git@github.com
```

第一次连会问你 `Are you sure you want to continue connecting?`，输入 `yes` 回车。

如果看到：

```
Hi 你的用户名! You've successfully authenticated...
```

就说明连上了！✅

---

## 5. 在GitHub创建私有仓库

1. 打开 https://github.com/new
2. **Repository name** 填 `openclaw-workspace`（或者你喜欢的名字）
3. **Description** 可以写 `我的OpenClaw AI助手备份`（选填）
4. ⚠️ **一定选「Private」！！！**

> 🔴 **重要警告**：你的workspace里可能包含API Key、个人记忆、聊天记录等敏感信息。**仓库必须设为Private**，否则全世界都能看到！

5. 下面的那些选项（README、.gitignore、license）都**不要勾**，保持空白
6. 点「**Create repository**」

创建好之后页面会显示一些命令提示，先别管它，跟着我下面的步骤来。

---

## 6. 添加.gitignore

在推送之前，我们先告诉Git哪些文件**不需要**备份（比如临时文件、缓存等）。

```bash
cd ~/.openclaw/workspace
```

```bash
cat > .gitignore << 'EOF'
# 依赖目录
node_modules/

# 临时文件
*.tmp
*.log
.DS_Store

# 敏感凭证文件（如果有单独的密钥文件）
*.pem
*.key

# 系统文件
Thumbs.db
.Trash-*
EOF
```

> 这个命令创建了一个 `.gitignore` 文件，告诉Git忽略这些不需要备份的东西。

> 💡 **关于API Key**：如果你的API Key是写在 `TOOLS.md` 或其他workspace文件里的，它们**会**被备份上去。这就是为什么仓库**必须是Private**。如果你觉得不放心，可以在 `.gitignore` 里加上包含Key的文件名。

---

## 7. 推送workspace到仓库

现在把你的workspace推送到GitHub。确保你还在workspace目录下：

```bash
cd ~/.openclaw/workspace
```

先配置一下Git的用户信息（第一次用Git需要做）：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的邮箱@example.com"
```

> 把用户名和邮箱换成你自己的。

然后初始化仓库并推送：

```bash
git init
git add .
git commit -m "首次备份：OpenClaw workspace"
git branch -M main
git remote add origin git@github.com:你的GitHub用户名/openclaw-workspace.git
git push -u origin main
```

> ⚠️ 把 `你的GitHub用户名` 换成你真正的GitHub用户名！

**逐行解释：**

| 命令 | 干了什么 |
|------|---------|
| `git init` | 把这个文件夹变成一个Git仓库 |
| `git add .` | 把所有文件加入"待备份"清单 |
| `git commit -m "..."` | 确认这次备份，附上一句备注 |
| `git branch -M main` | 把默认分支命名为main |
| `git remote add origin ...` | 告诉Git远程仓库的地址 |
| `git push -u origin main` | 把本地文件推送到GitHub |

推送完成后，刷新你的GitHub仓库页面，应该能看到所有文件了！🎉

---

## 8. 换服务器时如何恢复

将来如果你要换服务器，恢复流程非常简单：

### 1）在新服务器上安装好OpenClaw

按之前的部署教程装好OpenClaw。

### 2）生成SSH Key并添加到GitHub

跟第3、4步一样，在新服务器上重新生成SSH Key，添加到GitHub。

### 3）拉取备份

```bash
# 先删掉空的workspace（如果有的话）
rm -rf ~/.openclaw/workspace

# 从GitHub克隆你的备份
git clone git@github.com:你的GitHub用户名/openclaw-workspace.git ~/.openclaw/workspace
```

### 4）恢复配置文件

workspace拉回来了，但 `openclaw.json` 配置文件和API Key环境变量需要重新设置（这些不在workspace里）。

```bash
# 重新配置API Key
echo 'export ANTHROPIC_API_KEY="你的Key"' >> ~/.bashrc
echo 'export TELEGRAM_BOT_TOKEN="你的Token"' >> ~/.bashrc
source ~/.bashrc

# 启动OpenClaw
openclaw gateway start
```

然后给你的Telegram机器人发条消息试试——**AI还认识你！它的记忆都在！** 🧠

---

## 9. 日常同步命令

以后每次想备份最新数据，只需要三条命令：

```bash
cd ~/.openclaw/workspace
git add .
git commit -m "日常备份 $(date +%Y-%m-%d)"
git push
```

> `$(date +%Y-%m-%d)` 会自动填上今天的日期，比如"日常备份 2026-02-10"。

### 懒人一键版

把上面的命令合成一条：

```bash
cd ~/.openclaw/workspace && git add . && git commit -m "备份 $(date +%Y-%m-%d %H:%M)" && git push
```

复制这条命令，每次想备份就粘贴运行一遍就行。

### 更懒的做法：自动定时备份

让服务器每天自动帮你备份：

```bash
crontab -e
```

> 如果问你选哪个编辑器，输入 `1` 选nano（最简单的）。

在打开的文件**最后一行**加上：

```
0 3 * * * cd /root/.openclaw/workspace && git add . && git commit -m "自动备份 $(date +\%Y-\%m-\%d)" && git push 2>/dev/null
```

> 这行的意思是：每天凌晨3点自动备份一次。

按 `Ctrl + O` 保存，`Enter` 确认，`Ctrl + X` 退出。

从此以后，备份全自动，你什么都不用管。😎

---

## 小贴士

🔹 **第一次push如果报错**：检查SSH Key有没有正确添加到GitHub，用 `ssh -T git@github.com` 验证

🔹 **commit提示nothing to commit**：说明没有新的改动，不用担心

🔹 **仓库不小心设成了Public**：立刻去GitHub仓库页面 → Settings → 拉到最下面 Danger Zone → Change visibility → 改成Private

🔹 **想看备份历史**：运行 `git log --oneline` 可以看到每次备份的记录

🔹 **想回滚到之前的版本**：`git log --oneline` 找到想回到的那次的编号（比如 `a1b2c3d`），然后 `git checkout a1b2c3d -- 文件名`

---

祝你的AI员工永不失忆！🦞💾
