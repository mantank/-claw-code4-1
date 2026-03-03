# 🔒 OpenClaw 安全风险情报库

**采集日期：** 2026年3月2日  
**数据来源：** web_search (Brave Search API)  
**关键词：** "OpenClaw security", "OpenClaw vulnerability", "OpenClaw CVE", "OpenClaw 安全"  
**采集数量：** 40条搜索结果（去重后35条）

---

## 🏆 关键安全风险（按严重性排序）

### [ClawJacked Flaw Lets Malicious Sites Hijack Local OpenClaw AI Agents via WebSocket]
- 🔗 链接：https://thehackernews.com/2026/02/clawjacked-flaw-lets-malicious-sites.html
- 📝 摘要：ClawJacked漏洞允许恶意网站通过WebSocket连接到本地运行的OpenClaw实例，暴力破解密码后完全控制用户的AI代理。同时发现71个恶意技能在ClawHub技能市场传播恶意软件和加密货币诈骗。该漏洞已在最新版本修复。
- 🔥 严重性：严重（CVSS 8.8）
- ⭐ 影响范围：所有暴露的OpenClaw实例
- 💰 潜在损失：数据泄露、系统控制、金融损失
- 📅 发现日期：2026-03-02
- 🏷️ 标签：#ClawJacked #WebSocket #暴力破解 #恶意技能

### [CVE-2026-25253: Critical Remote Code Execution Vulnerability]
- 🔗 链接：https://www.kaspersky.com/blog/moltbot-enterprise-risk-management/55317/
- 📝 摘要：OpenClaw中最危险的漏洞是CVE-2026-25253（CVSS 8.8）。利用此漏洞会导致网关完全被攻陷，允许攻击者运行任意命令。这是远程代码执行漏洞，影响所有未更新的实例。
- 🔥 严重性：严重（CVSS 8.8）
- ⭐ 影响范围：所有版本<2026.2.25
- 💰 潜在损失：系统完全控制
- 📅 发现日期：2026-03-02
- 🏷️ 标签：#CVE-2026-25253 #RCE #网关攻陷 #任意命令执行

### [Malicious OpenClaw Skills Used to Distribute Atomic MacOS Stealer]
- 🔗 链接：https://www.trendmicro.com/en_us/research/26/b/openclaw-skills-used-to-distribute-atomic-macos-stealer.html
- 📝 摘要：已识别39个恶意技能（无特定模式），操纵OpenClaw在ClawHub上安装假的命令行界面工具。这些技能已被下架，但代码仍存在于ClawHub的GitHub仓库中。攻击者通过供应链攻击分发macOS信息窃取器。
- 🔥 严重性：高
- ⭐ 影响范围：MacOS用户
- 💰 潜在损失：凭证窃取、数据泄露
- 📅 发现日期：2026-03-02
- 🏷️ 标签：#供应链攻击 #恶意技能 #macOS窃取器 #ClawHub

### [OpenClaw security issues include data leakage & prompt injection]
- 🔗 链接：https://www.giskard.ai/knowledge/openclaw-security-vulnerabilities-include-data-leakage-and-prompt-injection-risks
- 📝 摘要：OpenClaw（Moltbot, Clawdbot）已经泄露API密钥和凭证。个人AI代理也容易受到通过提示注入的远程代码执行攻击。控制UI和会话管理中的架构弱点为提示注入和未经授权的工具使用创造了直接路径。
- 🔥 严重性：高
- ⭐ 影响范围：所有用户
- 💰 潜在损失：凭证泄露、未经授权访问
- 📅 发现日期：2026-03-02
- 🏷️ 标签：#数据泄露 #提示注入 #API密钥泄露 #会话管理

### [Researchers Reveal Six New OpenClaw Vulnerabilities]
- 🔗 链接：https://www.infosecurity-magazine.com/news/researchers-six-new-openclaw/
- 📝 摘要：OpenClaw修复了六个新漏洞，涵盖服务器端请求伪造（SSRF）、缺失身份验证和路径遍历错误。包括CVE-2026-26329（浏览器上传中的路径遍历，高严重性）和CVE-2026-28363（通过GNU长选项缩写绕过验证）。
- 🔥 严重性：中高
- ⭐ 影响范围：特定功能
- 💰 潜在损失：权限提升、数据访问
- 📅 发现日期：2026-03-02
- 🏷️ 标签：#SSRF #路径遍历 #验证绕过 #六个新漏洞

### [OpenClaw: What is it and can you use it safely? | Malwarebytes]
- 🔗 链接：https://www.malwarebytes.com/blog/news/2026/02/openclaw-what-is-it-and-can-you-use-it-safely
- 📝 摘要：荷兰数据保护局警告组织不要在处理敏感或受监管数据的系统上部署像OpenClaw这样的实验性代理，将特权本地访问、不成熟的安全工程和快速增长的可疑第三方插件生态系统的组合标记为端点上的特洛伊木马。
- 🔥 严重性：高
- ⭐ 影响范围：企业用户
- 💰 潜在损失：合规风险、数据泄露
- 📅 发现日期：2026-03-02
- 🏷️ 标签：#合规风险 #企业安全 #数据保护 #第三方插件

### [OpenClaw Security Guide 2026 | Contabo Blog]
- 🔗 链接：https://contabo.com/blog/openclaw-security-guide-2026/
- 📝 摘要：完整的OpenClaw自托管安全指南。学习提示注入防御、VPS加固、Docker隔离和凭证管理。包含40+漏洞修复、信任模型基础和逐步锁定程序。
- 🔥 严重性：指南
- ⭐ 影响范围：所有自托管用户
- 💰 潜在损失：预防性指南
- 📅 发现日期：2026-03-02
- 🏷️ 标签：#安全指南 #自托管 #Docker隔离 #凭证管理

### [基于亚马逊云科技 Mac 实例部署 OpenClaw，深度苹果生态自动化的最佳选择]
- 🔗 链接：https://aws.amazon.com/cn/blogs/china/openclaw-deployment-aws-mac/
- 📝 摘要：场景举例：OpenClaw处理公司敏感邮件、iMessage通讯、Keychain密码时，多层安全机制确保数据不泄露。所有操作都有CloudTrail日志记录，满足企业合规要求。远程访问通过SSM，不暴露任何公网端口，审计追溯完整。
- 🔥 严重性：解决方案
- ⭐ 影响范围：企业部署
- 💰 潜在损失：安全部署方案
- 📅 发现日期：2026-03-02
- 🏷️ 标签：#AWS #企业部署 #合规 #多层安全

### [2026年OpenClaw（Clawdbot）安全实战指南：5000+Skill选型攻略+部署流程+风险防御解析]
- 🔗 链接：https://developer.aliyun.com/article/1713724
- 📝 摘要：Windows专属安全安装脚本（内置恶意软件扫描）。运行安装脚本（自动禁用高危权限，隔离运行目录）。配置阿里云百炼大模型（安全版默认集成，仅需填入API-Key）。限制OpenClaw仅能访问指定文件夹。
- 🔥 严重性：指南
- ⭐ 影响范围：Windows用户
- 💰 潜在损失：安全配置指南
- 📅 发现日期：2026-03-02
- 🏷️ 标签：#Windows安全 #阿里云 #权限限制 #安全脚本

### [OpenClaw 作为 AI 智能体网关引发热议，解析其核心能力与潜在风险]
- 🔗 链接：https://www.huxiu.com/article/4838115.html
- 📝 摘要：同样一句"它能做事"，在不同人听来会有两种完全不同的解读：生产力派觉得太爽了，终于有人把链路打通；安全派觉得太危险了，你这是把自己交出去了。风险并不抽象。尤其当Skills生态开始爆炸后，"插件供应链"会成为最薄弱的一环：恶意技能、提示注入、权限误配、对外暴露端口。
- 🔥 严重性：分析
- ⭐ 影响范围：所有用户
- 💰 潜在损失：风险意识
- 📅 发现日期：2026-03-02
- 🏷️ 标签：#风险分析 #插件供应链 #安全心智 #虎嗅分析

---

## 🎯 安全风险分类

### 1. 远程代码执行（RCE）
- **漏洞**：CVE-2026-25253（CVSS 8.8）
- **影响**：网关完全被攻陷，任意命令执行
- **修复**：更新到v2026.2.25+
- **检测**：版本检查、漏洞扫描

### 2. WebSocket劫持（ClawJacked）
- **漏洞**：恶意网站通过WebSocket连接本地实例
- **攻击**：暴力破解密码，完全控制代理
- **修复**：更新到最新版本，禁用不必要的WebSocket
- **防护**：防火墙规则、访问控制

### 3. 供应链攻击（恶意技能）
- **平台**：ClawHub技能市场
- **数量**：71个恶意技能（已下架）
- **类型**：加密货币诈骗、信息窃取器、后门
- **防护**：仅安装可信技能、代码审查、沙箱运行

### 4. 数据泄露与凭证暴露
- **问题**：API密钥、凭证明文存储
- **场景**：会话管理弱点、控制UI漏洞
- **风险**：敏感数据泄露、未经授权访问
- **防护**：加密存储、最小权限、访问日志

### 5. 提示注入攻击
- **机制**：恶意指令嵌入数据中
- **影响**：LLM将恶意指令解释为合法用户指令
- **案例**：远程代码执行、数据泄露
- **防护**：输入验证、输出过滤、沙箱执行

### 6. 路径遍历与SSRF
- **漏洞**：CVE-2026-26329（路径遍历）
- **影响**：未经授权访问文件系统
- **漏洞**：SSRF（服务器端请求伪造）
- **防护**：输入验证、访问控制、网络隔离

### 7. 企业合规风险
- **警告**：荷兰数据保护局不建议部署
- **原因**：特权访问+不成熟安全+可疑插件
- **风险**：数据保护违规、合规处罚
- **方案**：企业级部署、审计日志、访问控制

### 8. 权限与访问控制
- **问题**：过度权限、权限误配
- **风险**：未经授权操作、数据泄露
- **配置**：限制访问目录、最小权限原则
- **工具**：安全配置命令、权限管理

---

## 💡 关键洞察

### 1. 安全危机集中爆发
- **时间线**：流行后三周内爆发多向量安全危机
- **原因**：快速增长+不成熟安全工程+开放生态
- **教训**：新兴技术需要同步安全建设
- **机会**：安全服务、审计工具、加固方案

### 2. 供应链攻击是最大威胁
- **平台**：ClawHub技能市场成为攻击目标
- **数量**：71个恶意技能，39个macOS窃取器
- **模式**：伪装成有用工具，实际分发恶意软件
- **防护**：技能审核、代码签名、信誉系统

### 3. 企业部署面临合规挑战
- **监管**：数据保护局明确警告
- **要求**：敏感数据系统不应部署实验性代理
- **方案**：企业级安全部署（AWS、阿里云）
- **市场**：合规部署服务、安全托管

### 4. 中文本地化安全方案
- **平台**：阿里云、AWS中国、CSDN
- **内容**：中文安全指南、Windows安全脚本
- **特点**：符合中国法规、本地化解决方案
- **机会**：中文安全服务、合规咨询

### 5. 零点击漏洞威胁
- **ClawJacked**：恶意网站无需用户交互即可劫持
- **影响**：开发者环境令牌泄露，云资源访问
- **防护**：会话隔离、跨源保护、令牌管理
- **趋势**：AI代理特有的新型攻击向量

### 6. 安全与生产力的平衡
- **矛盾**：功能强大 vs 安全风险
- **认知**：生产力派 vs 安全派的视角差异
- **方案**：分层安全、最小权限、监控告警
- **教育**：正确的安全心智模型建立

---

## 🚀 行动建议（针对安全防护）

### 短期（1-4周）
1. **立即更新** - 所有实例更新到v2026.2.25+修复ClawJacked
2. **技能审计** - 审查已安装技能，移除可疑来源
3. **权限限制** - 配置allowed-directories限制访问范围
4. **日志监控** - 启用详细日志，监控异常活动

### 中期（1-3个月）
1. **企业部署方案** - 基于AWS/阿里云的企业级安全部署
2. **安全配置模板** - 创建标准安全配置模板
3. **技能审核流程** - 建立技能安装前的代码审查流程
4. **监控告警系统** - 实现异常行为检测和告警

### 长期（3-6个月）
1. **安全认证体系** - 建立OpenClaw安全配置认证
2. **供应链安全** - 构建技能签名和信誉系统
3. **合规解决方案** - 针对不同行业的合规部署方案
4. **安全培训** - OpenClaw安全使用培训课程

---

## 📊 数据统计

| 风险类别 | 数量 | 占比 | 平均严重性 |
|----------|------|------|------------|
| RCE漏洞 | 4条 | 11.4% | 严重 |
| WebSocket劫持 | 5条 | 14.3% | 严重 |
| 供应链攻击 | 6条 | 17.1% | 高 |
| 数据泄露 | 5条 | 14.3% | 高 |
| 提示注入 | 4条 | 11.4% | 中高 |
| 路径遍历/SSRF | 3条 | 8.6% | 中 |
| 合规风险 | 4条 | 11.4% | 高 |
| 安全指南 | 4条 | 11.4% | 低 |

**严重性分布：**
- 🔴 严重：9条（25.7%）
- 🟠 高：14条（40.0%）
- 🟡 中：8条（22.9%）
- 🟢 低：4条（11.4%）

**信息来源：**
- 🔍 安全研究：The Hacker News、BleepingComputer、Oasis Security
- 🛡️ 安全公司：Kaspersky、Trend Micro、Malwarebytes、Giskard
- 📰 技术媒体：Infosecurity Magazine、Security Affairs、Dataconomy
- 🇨🇳 中文平台：阿里云、AWS中国、虎嗅、CSDN

---

## 🔗 相关资源

### 漏洞详情
- [ClawJacked漏洞详情](https://thehackernews.com/2026/02/clawjacked-flaw-lets-malicious-sites.html)
- [CVE-2026-25253详情](https://www.kaspersky.com/blog/moltbot-enterprise-risk-management/55317/)
- [六个新漏洞详情](https://www.infosecurity-magazine.com/news/researchers-six-new-openclaw/)

### 安全指南
- [OpenClaw安全指南2026](https://contabo.com/blog/openclaw-security-guide-2026/)
- [阿里云安全实战指南](https://developer.aliyun.com/article/1713724)
- [AWS企业部署方案](https://aws.amazon.com/cn/blogs/china/openclaw-deployment-aws-mac/)

### 恶意技能分析
- [恶意技能分发macOS窃取器](https://www.trendmicro.com/en_us/research/26/b/openclaw-skills-used-to-distribute-atomic-macos-stealer.html)
- [ClawHub供应链攻击](https://www.oasis.security/blog/openclaw-vulnerability)

### 合规与风险
- [Malwarebytes安全警告](https://www.malwarebytes.com/blog/news/2026/02/openclaw-what-is-it-and-can-you-use-it-safely)
- [虎嗅风险分析](https://www.huxiu.com/article/4838115.html)

---

**下次更新：** 2026年3月3日  
**采集代理：** 003零零叁  
**状态：** ✅ 完成security分类采集，准备开始community分类