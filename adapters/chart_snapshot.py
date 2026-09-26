"""Chart/astronomy snapshot adapter contracts.

The adapter consumes exact values from a chart/ephemeris provider. It does not
derive or guess planetary positions, houses, or aspects.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Protocol


class AstronomyChartClient(Protocol):
    def snapshot(self, at: datetime) -> Mapping[str, Any]:
        ...

    def map_image(self, at: datetime) -> Mapping[str, Any]:
        ...


class ChartTemporalSnapshotAdapter:
    def __init__(self, client: AstronomyChartClient) -> None:
        self.client = client

    def snapshot(self, at: datetime) -> dict[str, Any]:
        chart = dict(self.client.snapshot(at))
        image = dict(self.client.map_image(at))

        chart["map_artifact"] = {
            "map_image_id": image.get("id"),
            "map_image_hash": image.get("sha256"),
            "map_generated_at_utc": image.get("generated_at_utc"),
            "map_source": image.get("source"),
        }
        chart["verification_status"] = chart.get(
            "verification_status", "OBSERVED"
        )
        return chart
