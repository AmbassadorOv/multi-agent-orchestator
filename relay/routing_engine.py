"""Capability-based routing for the relay layer."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Route:
    group_id: str
    capabilities: tuple[str, ...]

class RoutingError(ValueError):
    pass

class RoutingEngine:
    def __init__(self, registry: dict[str, dict[str, Any]]):
        self.registry = registry

    def resolve(self, capability: str, preferred_group: str | None = None) -> Route:
        if preferred_group:
            group = self.registry.get(preferred_group)
            if group and capability in group.get("capabilities", []):
                return Route(preferred_group, tuple(group.get("capabilities", [])))
        matches = [
            (gid, data) for gid, data in self.registry.items()
            if capability in data.get("capabilities", [])
        ]
        if not matches:
            raise RoutingError(f"No group provides capability: {capability}")
        gid, data = matches[0]
        return Route(gid, tuple(data.get("capabilities", [])))
