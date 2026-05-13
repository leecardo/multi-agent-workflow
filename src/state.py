"""
多智能体工作流状态定义。

本模块同时提供 LangGraph 使用的 `WorkflowState`，以及兼容示例代码的
Pydantic 状态模型。K12 工作流以 `WorkflowState` 作为唯一主状态契约。
"""

from __future__ import annotations

from typing import Any, Optional

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing_extensions import Annotated, TypedDict


UserRole = str
IntentName = str
SafetyStatus = str


def merge_dicts(
    left: Optional[dict[str, Any]], right: Optional[dict[str, Any]]
) -> dict[str, Any]:
    """合并 LangGraph 状态中的字典字段，避免后续节点覆盖前序结果。"""
    merged: dict[str, Any] = {}
    if left:
        merged.update(left)
    if right:
        merged.update(right)
    return merged


class WorkflowState(TypedDict, total=False):
    """K12 教育工作流主状态。"""

    messages: Annotated[list[BaseMessage], add_messages]
    current_agent: Optional[str]
    task: str
    raw_input: str
    user_role: UserRole
    user_id: Optional[str]
    grade: Optional[str]
    subject: Optional[str]
    topic: Optional[str]
    intent: Optional[IntentName]
    intent_confidence: Optional[float]
    missing_fields: list[str]
    requires_clarification: bool
    clarification_question: Optional[str]
    selected_agent: Optional[str]
    agent_output: Optional[str]
    safety_status: Optional[SafetyStatus]
    safety_notes: Optional[str]
    final_output: Optional[str]
    results: Annotated[dict[str, Any], merge_dicts]
    metadata: Annotated[dict[str, Any], merge_dicts]
    task_state: Optional[dict[str, Any]]
    resource_context: Annotated[dict[str, Any], merge_dicts]


class AgentState(BaseModel):
    """通用智能体状态模型，保留给业务层或外部调用使用。"""

    messages: list[BaseMessage] = Field(
        default_factory=list, description="对话消息历史"
    )
    current_agent: Optional[str] = Field(None, description="当前活跃的智能体名称")
    task: str = Field(default="", description="当前任务描述")
    raw_input: str = Field(default="", description="用户原始输入")
    user_role: UserRole = Field(default="unknown", description="用户角色")
    grade: Optional[str] = Field(default=None, description="年级")
    subject: Optional[str] = Field(default=None, description="学科")
    topic: Optional[str] = Field(default=None, description="主题")
    intent: Optional[IntentName] = Field(default=None, description="归一化意图")
    intent_confidence: Optional[float] = Field(default=None, description="意图置信度")
    missing_fields: list[str] = Field(default_factory=list, description="缺失字段")
    requires_clarification: bool = Field(default=False, description="是否需要澄清")
    selected_agent: Optional[str] = Field(default=None, description="命中的业务 Agent")
    agent_output: Optional[str] = Field(default=None, description="业务 Agent 输出")
    safety_status: Optional[SafetyStatus] = Field(default=None, description="安全状态")
    safety_notes: Optional[str] = Field(default=None, description="安全说明")
    final_output: Optional[str] = Field(default=None, description="最终输出")
    results: dict[str, Any] = Field(
        default_factory=dict, description="各智能体执行结果"
    )
    metadata: dict[str, Any] = Field(default_factory=dict, description="额外元数据")

    def add_message(self, message: BaseMessage) -> None:
        """添加消息到历史记录。"""
        self.messages.append(message)

    def add_human_message(self, content: str) -> None:
        """添加人类消息。"""
        self.add_message(HumanMessage(content=content))

    def add_ai_message(self, content: str, agent_name: str = "assistant") -> None:
        """添加 AI 消息。"""
        message = AIMessage(content=content, additional_kwargs={"agent": agent_name})
        self.add_message(message)

    def set_result(self, agent_name: str, result: Any) -> None:
        """设置智能体执行结果。"""
        self.results[agent_name] = result

    def get_result(self, agent_name: str) -> Optional[Any]:
        """获取智能体执行结果。"""
        return self.results.get(agent_name)

    class Config:
        """Pydantic 配置。"""

        arbitrary_types_allowed = True
        json_encoders = {BaseMessage: lambda v: {"type": v.type, "content": v.content}}


class TaskState(BaseModel):
    """任务状态模型，用于追踪任务执行状态。"""

    task_id: str = Field(..., description="任务唯一标识")
    status: str = Field(default="pending", description="任务状态")
    progress: int = Field(default=0, description="任务进度 (0-100)")
    assigned_agents: list[str] = Field(
        default_factory=list, description="分配的智能体列表"
    )

    def update_status(self, status: str) -> None:
        """更新任务状态。"""
        self.status = status

    def update_progress(self, progress: int) -> None:
        """更新任务进度。"""
        self.progress = min(max(progress, 0), 100)

    def assign_agent(self, agent_name: str) -> None:
        """分配智能体。"""
        if agent_name not in self.assigned_agents:
            self.assigned_agents.append(agent_name)


State = AgentState
Task = TaskState
