# 读取微信公众号文章

## 触发条件
用户发来 `mp.weixin.qq.com` 链接时，自动使用此方法读取全文。

## 为什么不能用 web_fetch
微信公众号有防爬机制，web_fetch 只能拿到标题，拿不到正文。

## 正确方法：BrowserWing

### 第一步：导航到文章页
```bash
curl -s -X POST 'http://localhost:8080/api/v1/executor/navigate' \
  -H 'Content-Type: application/json' \
  -d '{"url":"<公众号链接>","wait_until":"networkidle"}'
```

### 第二步：提取正文
```bash
curl -s 'http://localhost:8080/api/v1/executor/page-text' | jq -r '.data.text'
```

## 注意事项
- 不要用 web_fetch，会失败
- 不要跟旭说"看不了公众号"
- 旭会经常转发公众号文章，这是高频操作
- 如果 BrowserWing 挂了，先尝试重启再说
