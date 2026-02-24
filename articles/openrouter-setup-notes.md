# 002换模型：OpenRouter配置方案

## 配置方法

在 `~/.openclaw-002/openclaw.json` 中：

```json
{
  "env": { "OPENROUTER_API_KEY": "sk-or-xxx" },
  "agents": {
    "defaults": {
      "model": { "primary": "openrouter/google/gemini-3.1-pro-preview" }
    }
  }
}
```

或者用CLI：
```bash
OPENCLAW_STATE_DIR=/root/.openclaw-002 openclaw onboard --auth-choice apiKey --token-provider openrouter --token "sk-or-xxx"
```

## 旭需要做的

1. 去 https://openrouter.ai/keys 获取API key
2. 充值（Gemini 3.1 Pro: 输入$2/百万token，输出$12/百万token）
3. 把key发给我，我帮配

## 模型ID格式

OpenRouter格式：`openrouter/<provider>/<model>`

例如：
- `openrouter/google/gemini-3.1-pro-preview`
- `openrouter/minimax/minimax-m2.5`
- `openrouter/zhipu/glm-5`

## 备选方案

如果不想走OpenRouter，也可以直接用Google AI Studio的API：
- 但旭说Gemini额度用完了，所以走OpenRouter是唯一选择
- OpenRouter好处：一个key能切所有模型，不用每家都注册
