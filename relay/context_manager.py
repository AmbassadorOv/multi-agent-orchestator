"""Controlled context projection for cross-group relay messages."""
from __future__ import annotations
from typing import Any, Iterable

def select_context(required: Iterable[str], context: dict[str, Any]) -> dict[str, Any]:
    """Return only explicitly requested context keys; never forward global memory implicitly."""
    return {key: context[key] for key in required if key in context}
