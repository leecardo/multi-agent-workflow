"""用户中心能力封装。"""

from __future__ import annotations

from typing import Any


class SchoolUserSkill:
    """读取校内用户基础信息。"""

    def fetch_user_summary(self, *, user_id: str) -> dict[str, Any]:
        """返回用户摘要。"""
        return {
            "user_id": user_id,
            "display_name": "示例用户",
            "role": "student",
            "guardians": ["家长A"],
        }
