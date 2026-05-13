# 多智能体工作流项目开发规范

## 项目概述
本项目基于 LangGraph 构建多智能体协作工作流，使用 Python 3.12 开发。

## 开发环境配置

### 1. Python 版本管理
- **工具**: mise (多语言版本管理)
- **配置文件**: `mise.toml`
- **当前版本**: Python 3.12
- **初始化命令**:
  ```bash
  # 安装 mise（如未安装）
  curl https://mise.run | sh
  
  # 激活 mise
  eval "$(mise activate bash)"
  
  # 安装配置的 Python 版本
  mise install
  ```

### 2. 依赖管理
- **工具**: uv (Python 包管理器)
- **配置文件**: `pyproject.toml`
- **依赖组**:
  - `dependencies`: 生产依赖
  - `dev.dependencies`: 开发依赖
- **常用命令**:
  ```bash
  # 安装所有依赖
  uv sync
  
  # 添加生产依赖
  uv add <package>
  
  # 添加开发依赖
  uv add --dev <package>
  
  # 移除依赖
  uv remove <package>
  
  # 运行 Python 脚本
  uv run python <script.py>
  
  # 运行项目命令
  uv run <command>
  ```

## 开发规范

### 1. 代码风格
- 使用 `ruff` 进行代码格式化和检查
- 配置位于 `pyproject.toml` 的 `[tool.ruff]` 部分
- 格式化命令:
  ```bash
  # 检查代码
  uv run ruff check .
  
  # 自动修复
  uv run ruff check --fix .
  
  # 格式化代码
  uv run ruff format .
  ```

### 2. 类型注解
- 所有函数必须有完整的类型注解
- 使用 Pydantic 模型进行数据验证
- 状态定义使用 TypedDict（LangGraph 要求）

### 3. 文件结构
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
└── AGENTS.md              # 本文件
```

## 工作流约束

### 1. 开发流程
1. **环境准备**: 确保 `mise install` 和 `uv sync` 已执行
2. **代码开发**: 遵循类型注解和代码风格规范
3. **测试验证**: 运行 `uv run python main.py` 验证功能
4. **代码检查**: 运行 `uv run ruff check .` 确保代码质量

### 2. 依赖管理约束
- **禁止**: 直接使用 `pip install` 安装依赖
- **必须**: 使用 `uv add` 管理依赖
- **版本锁定**: `uv.lock` 文件必须提交到版本控制
- **Python 版本**: 通过 `mise.toml` 统一管理，禁止手动指定

### 3. 运行约束
- **所有 Python 命令**: 必须通过 `uv run` 执行
- **脚本执行**: `uv run python <script.py>`
- **模块执行**: `uv run python -m <module>`
- **项目命令**: `uv run <command>`

### 4. 环境隔离
- **虚拟环境**: 由 `uv` 自动管理，位于 `.venv/`
- **环境激活**: 无需手动激活，`uv run` 自动处理
- **IDE 配置**: 指向 `.venv/` 目录

## 工具使用约定

### 1. 版本管理
```bash
# 检查当前 Python 版本
mise current python

# 安装指定版本
mise install python@3.12

# 切换版本
mise use python@3.12
```

### 2. 依赖操作
```bash
# 查看已安装依赖
uv pip list

# 查看依赖树
uv pip tree

# 更新所有依赖
uv lock --upgrade

# 生成 requirements.txt（如需要）
uv pip compile pyproject.toml -o requirements.txt
```

### 3. 代码质量
```bash
# 完整检查
uv run ruff check .

# 格式化
uv run ruff format .

# 类型检查（如配置 mypy）
uv run mypy src/
```

## 故障排除

### 1. 常见问题
- **依赖安装失败**: 检查网络连接，尝试 `uv sync --reinstall`
- **版本不匹配**: 运行 `mise install` 确保 Python 版本正确
- **导入错误**: 确认已执行 `uv sync` 安装所有依赖

### 2. 环境重置
```bash
# 重置虚拟环境
rm -rf .venv
uv sync

# 重置 Python 版本
mise uninstall python
mise install
```

## 版本控制

### 1. 必须提交的文件
- `pyproject.toml`: 项目配置
- `uv.lock`: 依赖锁定文件
- `mise.toml`: 版本管理配置
`AGENTS.md`: 本规范文件

### 2. 禁止提交的文件
- `.venv/`: 虚拟环境目录
- `__pycache__/`: Python 缓存
- `.pytest_cache/`: 测试缓存

## 更新记录
- 2024-01-XX: 初始版本，建立基础开发规范