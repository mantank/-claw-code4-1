# Skill: 飞书 API 调用指南

## 触发场景
需要调用飞书API但不确定用哪个Skill时，先查这里。

---

## 凭证（从TOOLS.md同步）
```
App ID:     cli_a908765086b85bc6
App Secret: 4HZ5OiOueIU1PYCy59T48fpYvomTWELl
```

## 获取 Access Token
```bash
curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_a908765086b85bc6","app_secret":"4HZ5OiOueIU1PYCy59T48fpYvomTWELl"}'
# 返回 tenant_access_token，有效期2小时
```

---

## Skill 路由表（按场景选）

| 需求 | 用哪个Skill |
|------|------------|
| 发消息/建群/群管理 | `feishu-im` |
| 多维表格增删改查 | `feishu-bitable` |
| 文档读写 | `feishu-doc` / `feishu-doc-writer` |
| 知识库操作 | `feishu-wiki` |
| 日历/日程 | `feishu-calendar` |
| 审批流 | `feishu-approval` |
| 任务管理 | `feishu-task` |
| 用户/部门查询 | `feishu-contact` |
| 文件/云盘 | `feishu-drive` |
| 权限管理 | `feishu-perm` |
| 互动卡片 | `feishu-card` |

---

## 常用接口速查

### 发送文本消息
```
POST /open-apis/im/v1/messages?receive_id_type=open_id
Body: {"receive_id":"...","msg_type":"text","content":"{\"text\":\"hello\"}"}
```

### 查询多维表格记录
```
GET /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records
```

### 上传文件
```
POST /open-apis/drive/v1/files/upload_all
```

---

## 重要ID备忘
| 资源 | ID |
|------|----|
| OPENA知识库 | space_id: 7603748469693484257 |

## 注意
- token有效期2小时，超时重新获取
- 所有请求Header加：`Authorization: Bearer {token}`
- 详细参数看对应Skill的SKILL.md
