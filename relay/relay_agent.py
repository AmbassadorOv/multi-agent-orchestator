"""Minimal cross-group relay protocol.

The relay transports and tracks messages. It does not invent results or grant
professional authority to destination agents.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Callable
import uuid

from .receipt_logger import ReceiptLogger
from .routing_engine import RoutingEngine
from .context_manager import select_context

class RelayError(ValueError):
    pass

class RelayAgent:
    def __init__(self, registry: dict[str, dict[str, Any]], handlers: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] | None = None):
        self.routing = RoutingEngine(registry)
        self.handlers = handlers or {}
        self.receipts = ReceiptLogger()
        self.messages: dict[str, dict[str, Any]] = {}
        self.tasks: dict[str, str] = {}

    def create_request(self, *, task_id: str, source_agent: str, source_group: str,
                       capability: str, payload: dict[str, Any], context: dict[str, Any] | None = None,
                       context_refs: list[str] | None = None, evidence_refs: list[str] | None = None,
                       requires_response: bool = True, requires_human_approval: bool = False,
                       parent_task_id: str | None = None) -> dict[str, Any]:
        route = self.routing.resolve(capability)
        message = {
            "message_id": f"MSG-{uuid.uuid4().hex}",
            "task_id": task_id,
            "parent_task_id": parent_task_id,
            "source_agent": source_agent,
            "source_group": source_group,
            "destination_agent": route.group_id,
            "destination_group": route.group_id,
            "message_type": "REQUEST",
            "priority": "NORMAL",
            "payload": dict(payload),
            "context_refs": list(context_refs or []),
            "evidence_refs": list(evidence_refs or []),
            "verification_state": "UNVERIFIED",
            "requires_response": requires_response,
            "requires_human_approval": requires_human_approval,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if context is not None and context_refs:
            message["context"] = select_context(context_refs, context)
        self.messages[message["message_id"]] = message
        self.tasks[task_id] = "CREATED"
        return message

    def send(self, message_id: str) -> dict[str, Any]:
        message = self.messages[message_id]
        if message["requires_human_approval"]:
            self.tasks[message["task_id"]] = "WAITING"
            self.receipts.record(message, "APPROVAL_REQUIRED")
            raise RelayError("Human approval required before delivery")
        self.tasks[message["task_id"]] = "SENT"
        self.receipts.record(message, "SENT")
        handler = self.handlers.get(message["destination_group"])
        if handler is None:
            raise RelayError(f"No handler registered for group: {message['destination_group']}")
        response = handler(message)
        self.tasks[message["task_id"]] = "COMPLETED"
        self.receipts.record(message, "COMPLETED")
        return response

    def thread(self, task_id: str) -> list[dict[str, Any]]:
        return [m for m in self.messages.values() if m["task_id"] == task_id]
