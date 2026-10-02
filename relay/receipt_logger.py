"""Append-only in-memory receipt log for the relay prototype."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class Receipt:
    message_id: str
    task_id: str
    source_group: str
    destination_group: str
    status: str
    timestamp: str

class ReceiptLogger:
    def __init__(self):
        self._receipts: list[Receipt] = []

    def record(self, message: dict[str, Any], status: str) -> Receipt:
        receipt = Receipt(
            message_id=message["message_id"],
            task_id=message["task_id"],
            source_group=message["source_group"],
            destination_group=message["destination_group"],
            status=status,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self._receipts.append(receipt)
        return receipt

    def thread(self, task_id: str) -> list[Receipt]:
        return [r for r in self._receipts if r.task_id == task_id]
