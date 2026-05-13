"""项目配置。"""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    """应用配置。"""

    app_env: str = "development"
    resource_cache_ttl_seconds: int = 600
    use_mock_external_skills: bool = True
    default_student_id: str = "student-demo"
    default_class_id: str = "class-demo"

    @property
    def enable_cache(self) -> bool:
        """是否启用缓存。"""
        return self.resource_cache_ttl_seconds > 0


def get_config() -> AppConfig:
    """从环境变量加载配置。"""
    ttl = int(os.getenv("RESOURCE_CACHE_TTL_SECONDS", "600"))
    return AppConfig(
        app_env=os.getenv("APP_ENV", "development"),
        resource_cache_ttl_seconds=ttl,
        use_mock_external_skills=os.getenv("USE_MOCK_EXTERNAL_SKILLS", "true").lower()
        != "false",
        default_student_id=os.getenv("DEFAULT_STUDENT_ID", "student-demo"),
        default_class_id=os.getenv("DEFAULT_CLASS_ID", "class-demo"),
    )
