# 多智能体工作流项目

基于 LangGraph 构建的多智能体协作工作流系统。

## 快速开始

### 1. 环境准备

确保已安装 mise 和 uv：

```bash
# 安装 mise（如未安装）
curl https://mise.run | sh

# 激活 mise
eval "$(mise activate bash)"

# 安装 Python 版本
mise install
```

### 2. 安装依赖

```bash
# 安装所有依赖（包括开发依赖）
uv sync
```

### 3. 运行项目

```bash
# 运行示例
uv run python main.py
```

## 项目结构

```
multi-agent-workflow/
├── src/                    # 源代码
│   ├── agents/            # 智能体定义
│   ├── nodes/             # 工作流节点
│   ├── tools/             # 工具函数
│   ├── config.py          # 配置管理
│   ├── graph.py           # 工作流图定义
│   └── state.py           # 状态模型
├── config/                 # 配置文件
├── data/                   # 数据存储
├── main.py                # 入口文件
├── pyproject.toml         # 项目配置
├── mise.toml              # 版本管理配置
├── uv.lock                # 依赖锁定文件
└── AGENTS.md              # 开发规范
```

## 开发规范

请参考 [AGENTS.md](AGENTS.md) 了解详细的开发规范，包括：

- **环境管理**: 使用 mise 管理 Python 版本
- **依赖管理**: 使用 uv 管理项目依赖
- **代码规范**: 使用 ruff 进行代码格式化和检查
- **工作流约束**: 所有命令必须通过 `uv run` 执行

## 核心功能

### 1. 状态管理 (`src/state.py`)
- 使用 Pydantic 模型定义状态
- 支持消息列表和智能体状态追踪
- 提供便捷的状态操作方法

### 2. 工作流图 (`src/graph.py`)
- 基于 LangGraph 的 StateGraph
- 多智能体协作：planner → executor → reviewer
- 条件路由和动态流程控制
- 支持状态持久化

### 3. 智能体节点
- **planner**: 任务规划和分析
- **executor**: 任务执行
- **reviewer**: 结果审核和验证

## 常用命令

```bash
# 环境管理
mise install                    # 安装配置的 Python 版本
mise current python             # 查看当前 Python 版本

# 依赖管理
uv sync                         # 安装所有依赖
uv add <package>                # 添加生产依赖
uv add --dev <package>          # 添加开发依赖
uv remove <package>             # 移除依赖

# 代码质量
uv run ruff check .             # 代码检查
uv run ruff format .            # 代码格式化
uv run ruff check --fix .       # 自动修复

# 运行项目
uv run python main.py           # 运行主程序
uv run python -m <module>       # 运行模块
```

## 故障排除

### 依赖问题
```bash
# 重新安装依赖
uv sync --reinstall

# 更新依赖
uv lock --upgrade
uv sync
```

### 环境问题
```bash
# 重置虚拟环境
rm -rf .venv
uv sync

# 重置 Python 版本
mise uninstall python
mise install
```

## 版本控制

### 必须提交的文件
- `pyproject.toml`: 项目配置
- `uv.lock`: 依赖锁定文件
- `mise.toml`: 版本管理配置
`AGENTS.md`: 开发规范

### 禁止提交的文件
- `.venv/`: 虚拟环境目录
- `__pycache__/`: Python 缓存
- `.pytest_cache/`: 测试缓存

## 许可证

[待添加]