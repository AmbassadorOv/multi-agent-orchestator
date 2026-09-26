"""Temporal network routing for WANGA-style reasoning orchestration.

The chart snapshot is a time-indexed coordinate/configuration layer.
It is not treated as causal proof about software behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import hmac
import json
from typing import Any, Dict, Mapping, Optional, Protocol, Sequence


class ChartSnapshotProvider(Protocol):
    def snapshot(self, at: datetime) -> Mapping[str, Any]:
        """Return the exact chart/astronomy state for the requested instant."""


class RepositoryStateProvider(Protocol):
    def snapshot(self, repositories: Sequence[str], at: datetime) -> Mapping[str, Any]:
        """Return observable GitHub state bound to the request."""


@dataclass(frozen=True)
class RouteSnapshot:
    request_id: str
    observed_at_utc: str
    chart_snapshot: Mapping[str, Any]
    repository_snapshot: Mapping[str, Any]
    chart_hash: str
    repository_hash: str
    route_id: str
    verification: Mapping[str, str]


def canonical_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return sha256(payload).hexdigest()


def normalize_utc(at: Optional[datetime]) -> datetime:
    if at is None:
        at = datetime.now(timezone.utc)
    elif at.tzinfo is None:
        raise ValueError("Timestamp must include timezone information.")
    return at.astimezone(timezone.utc).replace(microsecond=0)


def derive_route_id(
    request_id: str,
    observed_at_utc: str,
    chart_hash: str,
    repository_hash: str,
    secret: Optional[bytes] = None,
) -> str:
    material = "|".join(
        [request_id, observed_at_utc, chart_hash, repository_hash]
    ).encode("utf-8")

    if secret:
        digest = hmac.new(secret, material, sha256).hexdigest()
    else:
        digest = sha256(material).hexdigest()

    compact_time = observed_at_utc.replace(":", "").replace("-", "")
    return f"TR-{compact_time}-{digest[:24]}"


class TemporalNetworkRouter:
    def __init__(
        self,
        chart_provider: ChartSnapshotProvider,
        repository_provider: RepositoryStateProvider,
        route_secret: Optional[bytes] = None,
    ) -> None:
        self.chart_provider = chart_provider
        self.repository_provider = repository_provider
        self.route_secret = route_secret

    def resolve(
        self,
        request_id: str,
        repositories: Sequence[str],
        at: Optional[datetime] = None,
    ) -> RouteSnapshot:
        observed = normalize_utc(at)

        chart = dict(self.chart_provider.snapshot(observed))
        repos = dict(self.repository_provider.snapshot(repositories, observed))

        chart_hash = canonical_hash(chart)
        repository_hash = canonical_hash(repos)

        observed_iso = observed.isoformat().replace("+00:00", "Z")
        route_id = derive_route_id(
            request_id=request_id,
            observed_at_utc=observed_iso,
            chart_hash=chart_hash,
            repository_hash=repository_hash,
            secret=self.route_secret,
        )

        return RouteSnapshot(
            request_id=request_id,
            observed_at_utc=observed_iso,
            chart_snapshot=chart,
            repository_snapshot=repos,
            chart_hash=chart_hash,
            repository_hash=repository_hash,
            route_id=route_id,
            verification={
                "chart": str(chart.get("verification_status", "UNVERIFIED")),
                "repositories": str(
                    repos.get("verification_status", "UNVERIFIED")
                ),
                "semantic_mapping": "ARCHITECTURAL_COORDINATE_ONLY",
            },
        )


def build_instruction_envelope(
    query: str,
    snapshot: RouteSnapshot,
) -> Dict[str, Any]:
    return {
        "protocol": "WANGA-TEMPORAL-ROUTE/0.1",
        "request_id": snapshot.request_id,
        "route_id": snapshot.route_id,
        "observed_at_utc": snapshot.observed_at_utc,
        "query": query,
        "routing": {
            "chart_hash": snapshot.chart_hash,
            "repository_hash": snapshot.repository_hash,
            "chart": snapshot.chart_snapshot,
            "repositories": snapshot.repository_snapshot,
        },
        "verification": snapshot.verification,
        "instruction": (
            "Process the query against this immutable temporal snapshot. "
            "Do not substitute a later repository state or later chart state."
        ),
    }
