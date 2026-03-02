# 2026-03-01 工作日报

## 一、搞定的事情（按时间顺序）

### 1. 修复 X 大佬动态 Cron 推送
**做了什么：** 有两个定时任务负责推送X平台大佬动态，一个下午11点，一个晚间7点，都失效了。

**问题1（晚间7点）：** Cron配置里 `channel: last`，Cron是隔离session跑的，没有"last"记录，消息找不到目标，静默失败。改成 `channel: telegram` 写死。

**问题2（下午11点）：** 这个Cron指定了 `dev` profile运行，但dev profile里没有API Key，模型调不了，整个任务报 `No API Key` 失败。解法：把主profile的 `auth-profiles.json` 复制到dev profile目录。

**两个Cron的prompt也加了验证要求**，要求任务完成后验证消息是否真的发出去了。

---

### 2. 小红书MCP发布能力跑通
**做了什么：** 在001和002上都跑通了小红书发布能力，服务地址 `localhost:18060`。

**踩的坑：** 调发布接口时没有传图片，进程卡死，一直没有输出。原因是发布小红书必须带图片，没有图片MCP服务会挂起等待。

**写入铁律：**
- 发布必须带图片，否则不调接口
- 禁止用真实账号测试，测试内容往真账号发了一次，这条是血泪教训
- 一次只发一篇，等旭确认后才发布

---

### 3. 001把自己改挂了
**做了什么：** 在配置002的消息通道时，让001帮忙修改配置文件。001改错了位置，动了自己的运行配置，导致001无响应。

**解法：** 登录服务器，安装Claude Code，用外部工具直接编辑被改乱的配置文件，恢复原始内容，重启服务，001恢复正常。

**结论：** AI助手不能修改自己的运行配置文件，高风险操作必须人工介入。

---

### 4. 飞书文档读取能力打通
**做了什么：** 需要读取飞书分享的文章内容。

**踩的坑：** BrowserWing打开飞书链接，页面空白或需要登录。飞书文档是JS动态渲染，浏览器工具只能拿到空HTML壳。

**解法：** 飞书开放API，用App Token直接调 `docx/v1/documents/{token}/raw_content` 接口，不需要浏览器，不需要对方授权，公开文档直接可读。

成功读取了一篇飞书知识星球文章（4000+字），方法写入了工具文档。

---

### 5. 建立飞书知识收集流水线
**做了什么：** 建了一个飞书文档作为"知识收集箱"，旭随时把想读的链接扔进去。配置了每天北京时间18:00的Cron，自动读取收集箱→判断价值→存入飞书知识库→汇报。

---

### 6. 002配图SOP建立（第一版）
**做了什么：** 给002建了配图工作流文档，规定：写完内容→判断平台→生图→发旭确认→发布。初版用Gemini模型生图。

**后来发现问题：** Gemini图片API账户已消费$1.1，没有免费额度，每张图$0.067（约¥0.49）。002已经在悄悄烧钱。

---

### 7. 图片模型全线切换 qwen-image-max
**做了什么：** Gemini图片API停用，全部换成qwen-image-max（阿里云百炼）。

**对比：**
- Gemini：$0.067/张（¥0.49）
- qwen-image-max：¥0.04/张
- 差距：约10倍

**修改范围：**
- 001的TOOLS.md：更新图片生成策略
- 002的image-gen-sop SKILL.md：替换核心命令
- 后续：sketch-illustration和nanobanana-ppt-skills两个skill的生图脚本

---

### 8. 找到并改造PPT生成Skill
**做了什么：** 发现 `nanobanana-ppt-skills`（PPT自动生成）和 `sketch-illustration`（手绘插画配图）两个skill。

**安装问题：** nanobanana-ppt-skills被VirusTotal标记为可疑，clawhub拒绝安装。旭直接发了zip包，手动解压安装。

**改造内容：** 两个skill原来用Gemini或ZenMux API生图，全部改成qwen-image-max。

**sketch-illustration改造：** 替换 `generate_sketch.py`，ZenMux接口换成Dashscope接口，图片从URL下载到本地。

**nanobanana-ppt-skills改造：** 替换 `generate_slide()` 函数，Gemini SDK调用换成qwen-image-max HTTP请求，同时把 `load_dotenv` 依赖整个去掉（因为Key内置了）。

**踩的坑：** 只注释掉了 `import load_dotenv`，函数体里还有调用，运行报 `NameError: name 'load_dotenv' is not defined`。把整个函数替换成空函数解决。

**验证：** 跑了2页测试PPT，渐变毛玻璃风格，16:9，出图正常。

---

## 二、写入各类文档的内容

| 文档 | 新增内容 |
|------|---------|
| pitfalls.md | channel:last无效、dev profile无Key、小红书无图卡死、测试往真账号发帖 |
| TOOLS.md（001）| 图片生成双轨策略→改为qwen-image-max唯一方案 |
| TOOLS.md（002）| 飞书文档API读法、图片生成模型更新 |
| 002 image-gen-sop SKILL.md | 全面更新为qwen-image-max |
| 002 xiaohongshu-mcp SKILL.md | 铁律写入 |
| memory/tools-config.md | qwen-image-max调用方式、飞书API读文档方法 |

---

## 三、今天跑通的能力清单

| 能力 | 状态 |
|------|------|
| X平台大佬动态定时推送（两个时间段）| ✅ 修复 |
| 小红书带图发布（001和002均可）| ✅ 跑通 |
| 飞书公开文档读取（API方式）| ✅ 跑通 |
| 飞书知识收集→每日处理Cron | ✅ 建立 |
| qwen-image-max图片生成 | ✅ 跑通 |
| PPT自动生成（改造版）| ✅ 跑通 |
| 手绘插画配图（改造版）| ✅ 跑通 |
| 001把自己改挂后恢复 | ✅ 已恢复 |

---

## 四、还没跑通的

- 文章→自动配图→插图→发布的完整闭环（002自动走完全流程，无需人工干预）
- 002 qwen-image-max配图同步到002的image-gen-sop（今晚只改了002的skill，没有端到端测试）

---

## 五、今天花了什么钱

- Gemini图片API：历史累计已扣$1.1（今天发现，已停用）
- qwen-image-max：少量测试费用，估计¥0.5以内
- OpenRouter（002模型）：正常对话费用

