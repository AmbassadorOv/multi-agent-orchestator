from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import urllib.request
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path


WORKSPACE = Path(os.getenv("MASORAH_WORKSPACE", "./masorah_system_workspace"))
DRY_RUN = os.getenv("MASORAH_DRY_RUN", "true").lower() == "true"
SPREADSHEET_ID = os.getenv(
    "MASORAH_SPREADSHEET_ID",
    "1mkQyj6by1AtBUabpbaxaZq9Z2X3pX8ZpwG91ZCSOEYs",
)
SPREADSHEET_URL = os.getenv("MASORAH_SPREADSHEET_URL", "")


@dataclass
class Provenance:
    source_reference: str
    author: str
    date: str
    exact_location: str
    retrieval_timestamp: str
    content_hash: str
    verification_status: str = "NOT_YET_VERIFIED"


@dataclass
class Trace:
    trace_id: str
    agent_id: str
    action: str
    input_reference: str
    output_reference: str
    timestamp: str
    status: str


class Agent:
    def __init__(self, agent_id: str, role: str):
        self.agent_id = agent_id
        self.role = role

    def trace(self, action: str, input_reference: str, output_reference: str, status: str):
        return Trace(
            trace_id=str(uuid.uuid4()),
            agent_id=self.agent_id,
            action=action,
            input_reference=input_reference,
            output_reference=output_reference,
            timestamp=datetime.now(timezone.utc).isoformat(),
            status=status,
        )


AGENTS = {
    "core": Agent("sy-neurokernel-core", "Ingestion & Invariant Parser"),
    "topology": Agent("wanga-topology-bridge", "Graph Router & Repository Structurer"),
    "reasoning": Agent("tnrl-reasoning-engine", "Masorah Linguistic & Semantic Engine"),
    "enforcement": Agent("s39-refuge-enforcement", "Validation, Conflict Detection & Git Sync"),
}


def normalize_location(value: str) -> tuple[str, str]:
    cleaned = value.replace('"', "").replace("'", "").strip()
    if not cleaned:
        return "UNKNOWN", "GENERAL"

    parts = cleaned.split()
    book = parts[0]
    chapter = "GENERAL"

    if len(parts) > 1:
        chapter = re.split(r"[,;:]", parts[1])[0] or "GENERAL"

    return book, chapter


def content_hash(payload: dict) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def source_reference(row: dict) -> str:
    explicit = row.get("SourceReference") or row.get("source_reference")
    if explicit:
        return explicit
    location = row.get("where", "")
    date = row.get("dd/mm/y", "")
    return f"sheet:{SPREADSHEET_ID}:{date}:{location}"


def build_payload(row: dict, sequence: int) -> tuple[dict, Provenance]:
    location = row.get("where", "")
    book, chapter = normalize_location(location)

    payload = {
        "schema_version": "1.0",
        "sequence": sequence,
        "date": row.get("dd/mm/y", ""),
        "author": row.get("who", ""),
        "exact_location": location,
        "book": book,
        "chapter": chapter,
        "change_description": row.get("what", ""),
        "c1_attribution": "PENDING",
        "c2_temporal_revision": "PENDING",
    }

    digest = content_hash(payload)
    prov = Provenance(
        source_reference=source_reference(row),
        author=row.get("who", ""),
        date=row.get("dd/mm/y", ""),
        exact_location=location,
        retrieval_timestamp=datetime.now(timezone.utc).isoformat(),
        content_hash=digest,
    )
    return payload, prov


def write_projection(repo_name: str, filename: str, payload: dict, provenance: Provenance, trace: Trace):
    path = WORKSPACE / "repositories" / repo_name
    path.mkdir(parents=True, exist_ok=True)

    record = {
        "payload": payload,
        "provenance": asdict(provenance),
        "trace": asdict(trace),
    }

    with (path / filename).open("w", encoding="utf-8") as fh:
        json.dump(record, fh, ensure_ascii=False, indent=2)


def fetch_csv() -> list[dict]:
    if not SPREADSHEET_URL:
        raise RuntimeError(
            "MASORAH_SPREADSHEET_URL is not configured. Supply the spreadsheet URL when ready."
        )

    with urllib.request.urlopen(SPREADSHEET_URL, timeout=30) as response:
        text = response.read().decode("utf-8-sig")

    return list(csv.DictReader(text.splitlines()))


def run():
    WORKSPACE.mkdir(parents=True, exist_ok=True)

    if not SPREADSHEET_URL:
        print("CONFIG ONLY: spreadsheet URL is not supplied yet.")
        print(f"Spreadsheet ID: {SPREADSHEET_ID}")
        return

    rows = fetch_csv()
    processed = 0

    for row in rows:
        location = row.get("where", "")
        modification = row.get("what", "")

        if not location or location.lower() == "various":
            if "AC" in modification or "LC" in modification:
                print("Global codex candidate:", modification[:80])
            continue

        processed += 1
        payload, provenance = build_payload(row, processed)
        book = payload["book"]
        chapter = payload["chapter"]
        filename = f"sync_{book}_{chapter}_{processed}.json"

        # The four repositories are projections of one source event.
        projections = [
            "Masorah-Central-Core",
            "Masorah-Codex-Imperial",
            f"Book-{book}",
            f"Chapter-{book}-{chapter}",
        ]

        topology_trace = AGENTS["topology"].trace(
            "PLAN_REPOSITORY_FANOUT",
            provenance.source_reference,
            ",".join(projections),
            "PLANNED",
        )

        for repo in projections:
            write_projection(repo, filename, payload, provenance, topology_trace)

        enforcement_status = "DRY_RUN_APPROVAL_REQUIRED" if DRY_RUN else "READY_FOR_GITHUB_PUSH"
        enforcement_trace = AGENTS["enforcement"].trace(
            "VALIDATE_AND_STAGE_PUSH",
            provenance.source_reference,
            filename,
            enforcement_status,
        )

        with (WORKSPACE / "trace.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(enforcement_trace), ensure_ascii=False) + "\n")

    print(f"Processed records: {processed}")
    print(f"Workspace: {WORKSPACE.resolve()}")
    print(f"Mode: {'DRY_RUN' if DRY_RUN else 'PUSH_ENABLED'}")


if __name__ == "__main__":
    run()
