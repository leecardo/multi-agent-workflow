"""缓存仓储。

当前使用进程内字典模拟 Redis 行为，保留统一接口供服务层调用。
"""

from __future__ import annotations

from typing import Any


class RedisRepository:
    """简单缓存仓储。"""

    _cache: dict[str, Any] = {}

    def get(self, key: str) -> Any | None:
        """读取缓存。"""
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> Any:
        """写入缓存。"""
        self._cache[key] = value
        return value
