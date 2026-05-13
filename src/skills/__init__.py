"""外部系统能力封装。"""

from src.skills.exam_system_skill import ExamSystemSkill
from src.skills.homework_platform_skill import HomeworkPlatformSkill
from src.skills.resource_platform_skill import ResourcePlatformSkill
from src.skills.school_user_skill import SchoolUserSkill

__all__ = [
    "ExamSystemSkill",
    "HomeworkPlatformSkill",
    "ResourcePlatformSkill",
    "SchoolUserSkill",
]
