"""Gateway contract between the temporal router and the Thinking Machine.

The gateway receives a frozen route envelope and returns a normalized response.
It must not silently refresh the temporal snapshot mid-request.
"""

from __future__ import annotations

from typing import Any, Mapping, Protocol


class ThinkingMachineClient(Protocol):
    async def process(self, envelope: Mapping[str, Any]) -> Mapping[str, Any]:
        ...


class ThinkingMachineGateway:
    def __init__(self, client: ThinkingMachineClient) -> None:
        self.client = client

    async def execute(
        self,
        query: str,
        envelope: Mapping[str, Any],
    ) -> dict[str, Any]:
        result = dict(await self.client.process(envelope))
        return {
            "protocol": "WANGA-TEMPORAL-ROUTE/0.1",
            "route_id": envelope.get("route_id"),
            "request_id": envelope.get("request_id"),
            "observed_at_utc": envelope.get("observed_at_utc"),
            "query": query,
            "response": result.get("response"),
            "repositories_consulted": (
                envelope.get("routing", {}).get("repositories", {}).get(
                    "repositories", []
                )
            ),
            "chart_hash": envelope.get("routing", {}).get("chart_hash"),
            "repository_hash": envelope.get("routing", {}).get(
                "repository_hash"
            ),
            "map_image_hash": (
                envelope.get("routing", {})
                .get("chart", {})
                .get("map_artifact", {})
                .get("map_image_hash")
            ),
            "verification_state": result.get(
                "verification_state", "UNVERIFIED"
            ),
            "errors": result.get("errors", []),
        }
