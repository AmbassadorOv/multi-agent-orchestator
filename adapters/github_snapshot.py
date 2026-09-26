"""GitHub state adapter contracts.

The adapter intentionally separates repository identity from repository state.
A live implementation can use GitHub REST/GraphQL, GitHub App auth, or another
approved client. This module never invents a commit/ref.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, Mapping, Protocol, Sequence


class GitHubClient(Protocol):
    def repository(self, full_name: str) -> Mapping[str, Any]:
        ...

    def commit(self, full_name: str, ref: str) -> Mapping[str, Any]:
        ...

    def branch_refs(self, full_name: str) -> Sequence[Mapping[str, Any]]:
        ...


@dataclass(frozen=True)
class RepositoryTemporalState:
    repository: str
    observed_at_utc: str
    default_branch: str | None
    head_sha: str | None
    refs: Sequence[Mapping[str, Any]]
    metadata: Mapping[str, Any]

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


class GitHubTemporalSnapshotAdapter:
    def __init__(self, client: GitHubClient) -> None:
        self.client = client

    def snapshot(
        self,
        repositories: Sequence[str],
        at: datetime,
    ) -> Dict[str, Any]:
        observed = at.isoformat().replace("+00:00", "Z")
        states = []

        for full_name in repositories:
            meta = dict(self.client.repository(full_name))
            branch = meta.get("default_branch")

            head_sha = None
            if branch:
                commit = dict(self.client.commit(full_name, branch))
                head_sha = commit.get("sha")

            refs = list(self.client.branch_refs(full_name))

            states.append(
                RepositoryTemporalState(
                    repository=full_name,
                    observed_at_utc=observed,
                    default_branch=branch,
                    head_sha=head_sha,
                    refs=refs,
                    metadata={
                        "repository_id": meta.get("id"),
                        "visibility": meta.get("visibility"),
                        "archived": meta.get("archived"),
                        "updated_at": meta.get("updated_at"),
                    },
                ).as_dict()
            )

        return {
            "provider": "github",
            "observed_at_utc": observed,
            "repositories": states,
            "verification_status": "OBSERVED",
        }
