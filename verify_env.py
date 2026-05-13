#!/usr/bin/env python3
"""
环境验证脚本
验证项目开发环境是否正确配置
"""

import sys
import subprocess
from pathlib import Path


def check_command(cmd: str) -> bool:
    """检查命令是否可用"""
    try:
        subprocess.run([cmd, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main():
    """主函数"""
    print("=== 环境验证 ===")
    print()

    # 检查 Python 版本
    print(f"Python 版本: {sys.version}")
    print(f"Python 路径: {sys.executable}")
    print()

    # 检查 mise
    print("检查 mise:")
    if check_command("mise"):
        result = subprocess.run(
            ["mise", "current", "python"], capture_output=True, text=True
        )
        print("  ✓ mise 已安装")
        print(f"  当前 Python 版本: {result.stdout.strip()}")
    else:
        print("  ✗ mise 未安装")
    print()

    # 检查 uv
    print("检查 uv:")
    if check_command("uv"):
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        print("  ✓ uv 已安装")
        print(f"  版本: {result.stdout.strip()}")
    else:
        print("  ✗ uv 未安装")
    print()

    # 检查虚拟环境
    print("检查虚拟环境:")
    venv_path = Path(".venv")
    if venv_path.exists():
        print(f"  ✓ 虚拟环境存在: {venv_path}")

        # 检查虚拟环境中的 Python
        venv_python = venv_path / "bin" / "python"
        if venv_python.exists():
            print(f"  ✓ 虚拟环境 Python: {venv_python}")
        else:
            print("  ✗ 虚拟环境 Python 不存在")
    else:
        print("  ✗ 虚拟环境不存在")
    print()

    # 检查配置文件
    print("检查配置文件:")
    config_files = ["pyproject.toml", "mise.toml", "uv.lock", "AGENTS.md"]
    for file in config_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file}")
    print()

    # 检查依赖
    print("检查依赖:")
    try:
        result = subprocess.run(
            [
                "uv",
                "run",
                "python",
                "-c",
                "import langgraph; print('langgraph: 已安装')",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"  ✓ {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ langgraph 导入失败: {e.stderr}")

    try:
        result = subprocess.run(
            [
                "uv",
                "run",
                "python",
                "-c",
                "import pydantic; print('pydantic:', pydantic.__version__)",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"  ✓ {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ pydantic 导入失败: {e.stderr}")

    print()
    print("=== 验证完成 ===")


if __name__ == "__main__":
    main()
