"""Verification boundary: relay records state but does not self-authorize verification."""
from __future__ import annotations
from typing import Any

class VerificationBridge:
    ALLOWED_STATES = {"UNVERIFIED", "NOT_YET_VERIFIED", "VERIFIED"}

    def attach(self, result: dict[str, Any], state: str, evidence_refs: list[str] | None = None) -> dict[str, Any]:
        if state not in self.ALLOWED_STATES:
            raise ValueError(f"Invalid verification state: {state}")
        output = dict(result)
        output["verification_state"] = state
        if evidence_refs is not None:
            output["evidence_refs"] = list(evidence_refs)
        return output
