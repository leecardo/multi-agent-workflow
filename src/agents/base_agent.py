"""教育 Agent 基类。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.state import WorkflowState


@dataclass(frozen=True)
class AgentResult:
    """业务 Agent 的标准输出。"""

    output: str
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseEducationAgent:
    """K12 教育业务 Agent 基类。"""

    name: str = "base_agent"
    description: str = "K12 教育业务 Agent"

    def run(self, state: WorkflowState) -> AgentResult:
        """执行 Agent 逻辑。"""
        raise NotImplementedError
