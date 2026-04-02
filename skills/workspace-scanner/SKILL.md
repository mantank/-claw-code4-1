# workspace-scanner skill

> 基于 claw-code context.py 的工作区自动扫描
> 功能：启动时自动感知工作区结构，生成结构化上下文报告

---

## claw-code 原始设计

```python
@dataclass(frozen=True)
class PortContext:
    source_root: Path
    tests_root: Path
    assets_root: Path
    archive_root: Path
    python_file_count: int
    test_file_count: int
    asset_file_count: int
    archive_available: bool

def build_port_context(base: Path | None = None) -> PortContext:
    # 扫描工作区，统计各类文件数量
    return PortContext(
        python_file_count=sum(1 for path in source_root.rglob('*.py')),
        archive_available=archive_root.exists(),
        ...
    )
```

---

## OpenClaw 版本功能

### 扫描维度

| 维度 | 说明 |
|------|------|
| 代码文件 | .py / .js / .ts / .sh 数量 |
| 配置文件 | .json / .yaml / .md 文件列表 |
| Git状态 | 是否为git仓库，最后commit时间 |
| 依赖文件 | requirements.txt / package.json / Pipfile |
| 磁盘占用 | 工作区总大小 |
| 最近修改 | 过去7天修改过的文件 |

### 输出格式

```
## Workspace Context

- 代码文件：12 个 (.py/js/ts/sh)
- 配置文件：8 个 (.json/.yaml/.md)
- Git仓库：是，最后commit 3天前
- 依赖管理：requirements.txt ✅ / package.json ❌
- 磁盘占用：45MB
- 最近活跃：SOUL.md, HEARTBEAT.md, AGENTS.md
```

---

## 使用场景

1. **启动时上下文准备**：在处理任务前先了解工作区状态
2. **异常检测**：文件突然大量变化时预警
3. **交接参考**：新session可以快速了解工作区

---

## 实现

运行扫描：

```bash
bash ~/.openclaw/workspace/scripts/workspace-scan.sh
```

集成到心跳：每次心跳检查工作区变化，有异常时记录。
