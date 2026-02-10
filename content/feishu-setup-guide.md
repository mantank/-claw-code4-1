# 飞书开放平台 API 接入指南

> 目标：创建飞书应用，获取 API 访问能力，为后续接入 OpenClaw 或自动化工具做准备

---

## 第一步：注册飞书开放平台

1. 打开 https://open.feishu.cn
2. 用飞书账号登录（需要有企业/团队）
3. 进入「开发者后台」

## 第二步：创建应用

1. 点击「创建应用」→ 选择「企业自建应用」
2. 填写应用名称和描述（比如 "AI助手接入"）
3. 上传应用图标（随便找一个就行）
4. 创建完成后，进入应用详情页

## 第三步：获取凭证

应用详情页的「凭证与基础信息」中找到：

- **App ID** — 应用唯一标识
- **App Secret** — 应用密钥（点击显示后复制，妥善保管）

这两个是调用 API 的基础凭证。

## 第四步：获取 Access Token

飞书有两种 Token：

### 1. tenant_access_token（应用级别）
- 用于以应用身份调用 API
- 请求方式：

```bash
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "你的App_ID",
    "app_secret": "你的App_Secret"
  }'
```

- 返回的 `tenant_access_token` 有效期 2 小时，过期需重新获取

### 2. user_access_token（用户级别）
- 用于以用户身份调用 API（需要用户授权）
- 流程更复杂，涉及 OAuth2 授权码，初期用不到

**建议：先用 tenant_access_token 跑通基础功能。**

## 第五步：配置权限

1. 在应用详情页 →「权限管理」
2. 根据你要用的功能开通权限，常用的：
   - **消息** — `im:message:send_as_bot`（以机器人发消息）
   - **群组** — `im:chat`（管理群聊）
   - **文档** — `docx:document`（读写文档）
   - **通讯录** — `contact:user.base:readonly`（读取用户信息）
3. 开通权限后需要管理员审批

## 第六步：发布应用

1. 在应用详情页 →「版本管理与发布」
2. 创建新版本，填写更新说明
3. 提交审核（企业内部应用通常很快通过）
4. 审核通过后，应用上线

## 第七步：创建机器人（可选）

如果要做聊天机器人：
1. 应用详情页 →「应用功能」→「机器人」→ 开启
2. 配置事件订阅 URL（接收消息回调）
3. 在「事件订阅」中添加 `im.message.receive_v1`（接收消息事件）

---

## 常用 API 速查

| 功能 | API | 说明 |
|------|-----|------|
| 发消息 | POST /open-apis/im/v1/messages | 给用户/群发消息 |
| 读文档 | GET /open-apis/docx/v1/documents/{id} | 读取飞书文档 |
| 创建文档 | POST /open-apis/docx/v1/documents | 创建新文档 |
| 上传文件 | POST /open-apis/im/v1/files | 上传文件到消息 |
| 获取用户信息 | GET /open-apis/contact/v3/users/{id} | 查询用户 |

---

## 和 OpenClaw 对接的思路

目前 OpenClaw 已经原生支持飞书渠道（`openclaw doctor` 里有显示 Feishu: not configured）。

接入步骤推测：
1. 创建好飞书应用 + 机器人
2. 在 OpenClaw 配置里填入 App ID、App Secret
3. 配置事件回调 URL 指向 OpenClaw 的 webhook 地址
4. 具体操作需查看 OpenClaw 官方文档的飞书渠道配置部分

---

## 状态：📋 方案已整理，等旭决定是否接入
