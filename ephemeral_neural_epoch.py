"""Ephemeral neural-network configuration derived from a temporal snapshot.

This module defines a cryptographic configuration epoch rather than retraining a
brand-new neural model every second.

For every second:
    snapshot(t) -> canonical bytes -> epoch seed -> network topology/config

The same inputs reproduce the same ephemeral configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import hmac
import json
from typing import Any, Dict, Mapping, Optional


PROTOCOL = "WANGA-EPHEMERAL-NET/0.1"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def derive_seed(
    snapshot: Mapping[str, Any],
    secret: Optional[bytes] = None,
) -> bytes:
    payload = canonical_bytes(snapshot)
    if secret:
        return hmac.new(secret, payload, sha256).digest()
    return sha256(payload).digest()


def derive_uint(seed: bytes, label: str, index: int = 0) -> int:
    material = (
        seed
        + b"|"
        + label.encode("utf-8")
        + b"|"
        + str(index).encode("utf-8")
    )
    return int.from_bytes(sha256(material).digest(), "big")


@dataclass(frozen=True)
class EphemeralNeuralEpoch:
    epoch_id: str
    second: str
    seed_commitment: str
    topology: Mapping[str, Any]
    routing: Mapping[str, Any]


class EphemeralNetworkFactory:
    """Create a reproducible per-second neural execution configuration."""

    def __init__(self, secret: Optional[bytes] = None) -> None:
        self.secret = secret

    def create(
        self,
        temporal_snapshot: Mapping[str, Any],
        second: str,
        base_topology: Mapping[str, Any],
    ) -> EphemeralNeuralEpoch:
        source = {
            "protocol": PROTOCOL,
            "second": second,
            "snapshot": temporal_snapshot,
            "base_topology": base_topology,
        }

        seed = derive_seed(source, self.secret)
        epoch_digest = sha256(seed).hexdigest()

        node_count = int(base_topology.get("node_count", 0))
        edge_count = int(base_topology.get("edge_count", 0))

        node_order = [
            derive_uint(seed, "node-order", i) % max(node_count, 1)
            for i in range(node_count)
        ]

        edge_order = [
            derive_uint(seed, "edge-order", i) % max(edge_count, 1)
            for i in range(edge_count)
        ]

        topology = {
            **dict(base_topology),
            "epoch_second": second,
            "node_order_seeded": node_order,
            "edge_order_seeded": edge_order,
        }

        routing = {
            "seed_commitment": sha256(seed).hexdigest(),
            "routing_epoch": epoch_digest[:32],
            "derivation": "HMAC-SHA256" if self.secret else "SHA-256",
        }

        return EphemeralNeuralEpoch(
            epoch_id=(
                "ENE-"
                + second.replace(":", "").replace("-", "")
                + "-"
                + epoch_digest[:24]
            ),
            second=second,
            seed_commitment=sha256(seed).hexdigest(),
            topology=topology,
            routing=routing,
        )


def epoch_identity(epoch: EphemeralNeuralEpoch) -> Dict[str, Any]:
    return {
        "protocol": PROTOCOL,
        "epoch_id": epoch.epoch_id,
        "second": epoch.second,
        "seed_commitment": epoch.seed_commitment,
        "topology": dict(epoch.topology),
        "routing": dict(epoch.routing),
    }
