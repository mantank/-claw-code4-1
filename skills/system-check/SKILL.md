# system-check skill

> 基于 claw-code setup.py 的系统环境检测
> 功能：启动时检测运行环境、依赖、配置有效性

---

## claw-code 设计

```python
@dataclass(frozen=True)
class WorkspaceSetup:
    python_version: str           # "3.11.4"
    implementation: str           # "CPython" / "PyPy"
    platform_name: str            # "Linux-6.6.117-x86_64"
    test_command: str             # "python3 -m unittest discover..."

    def startup_steps(self) -> tuple[str, ...]:
        return (
            'start top-level prefetch side effects',
            'build workspace context',
            'load mirrored command snapshot',
            ...
        )
```

**核心思想：session 开始前，先把运行环境的所有信息收集齐全，形成可信的基础**

---

## OpenClaw 系统检测清单

### 1. 运行时环境

```bash
# 基础信息
openclaw --version           # OpenClaw 版本
node --version               # Node 版本
python3 --version            # Python 版本
```

### 2. 依赖完整性检查

| 依赖 | 检查命令 | 最低版本 |
|------|---------|---------|
| OpenClaw | `openclaw --version` | 2026.4.1 |
| Node | `node --version` | v18+ |
| npm | `npm --version` | 8+ |
| Git | `git --version` | 2+ |

### 3. 配置文件有效性

```bash
openclaw config validate
```

### 4. 插件状态

```bash
ls ~/.openclaw/extensions/
```

### 5. 磁盘和内存

```bash
df -h ~/.openclaw              # 磁盘空间
free -h                       # 内存
```

---

## 运行系统检测

```bash
bash ~/.openclaw/workspace/scripts/system-check.sh
```

---

## startup_steps 等效于 OpenClaw 的启动链

claw-code 的 startup_steps 在 OpenClaw 等价为：

```
Gateway 启动
  → workspace 加载
  → plugins 加载
  → agents 初始化
  → heartbeat 启动
  → 等待第一个用户消息
```

OpenClaw 的启动日志在 `openclaw gateway logs` 中可见。
