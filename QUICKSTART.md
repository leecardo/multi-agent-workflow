# 快速开始指南

## 环境要求

- **mise**: Python 版本管理工具
- **uv**: Python 包管理器
- **Python 3.12**: 项目要求版本

## 1. 环境准备

### 安装 mise（如未安装）
```bash
curl https://mise.run | sh
eval "$(mise activate bash)"
```

### 安装 Python 版本
```bash
mise install
```

## 2. 项目初始化

### 克隆项目（如从远程仓库）
```bash
git clone <repository-url>
cd multi-agent-workflow
```

### 安装依赖
```bash
uv sync
```

## 3. 验证环境

运行环境验证脚本：
```bash
uv run python verify_env.py
```

预期输出：
```
=== 环境验证 ===

Python 版本: 3.12.13
Python 路径: /root/projects/multi-agent-workflow/.venv/bin/python3

检查 mise:
  ✓ mise 已安装
  当前 Python 版本: 3.12.13

检查 uv:
  ✓ uv 已安装
  版本: uv 0.11.10 (x86_64-unknown-linux-musl)

检查虚拟环境:
  ✓ 虚拟环境存在: .venv
  ✓ 虚拟环境 Python: .venv/bin/python

检查配置文件:
  ✓ pyproject.toml
  ✓ mise.toml
  ✓ uv.lock
  ✓ AGENTS.md

检查依赖:
  ✓ langgraph: 已安装
  ✓ pydantic: 2.13.4

=== 验证完成 ===
```

## 4. 运行示例

```bash
uv run python main.py
```

预期输出：
```
=== 多智能体工作流示例 ===

示例1：执行默认工作流
任务: 分析用户需求并生成技术方案
--------------------------------------------------
执行结果:
  当前智能体: reviewer
  执行结果: {'reviewer': {'approved': True, 'quality_score': 85, 'feedback': '结果符合预期，质量良好'}}
  元数据: {'review_completed': True}

示例2：创建自定义工作流图
工作流图类型: <class 'langgraph.graph.state.CompiledStateGraph'>
可用节点: ['__start__', 'planner', 'executor', 'reviewer']

示例3：使用状态模型
任务ID: task-001
状态: running
进度: 30%
分配的智能体: ['planner', 'executor']

示例完成！
```

## 5. 开发工作流

### 添加依赖
```bash
# 添加生产依赖
uv add <package>

# 添加开发依赖
uv add --dev <package>
```

### 代码检查
```bash
# 检查代码
uv run ruff check .

# 格式化代码
uv run ruff format .

# 自动修复
uv run ruff check --fix .
```

### 运行代码
```bash
# 运行脚本
uv run python <script.py>

# 运行模块
uv run python -m <module>
```

## 6. 项目结构

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
├── verify_env.py          # 环境验证脚本
├── pyproject.toml         # 项目配置
├── mise.toml              # 版本管理配置
├── uv.lock                # 依赖锁定文件
├── AGENTS.md              # 开发规范
└── QUICKSTART.md          # 本文件
```

## 7. 常见问题

### 依赖安装失败
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

### 导入错误
确保已执行 `uv sync` 安装所有依赖。

## 8. 更多信息

- 详细开发规范：[AGENTS.md](AGENTS.md)
- 项目说明：[README.md](README.md)