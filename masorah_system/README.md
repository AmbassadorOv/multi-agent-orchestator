# Masorah Agent Constellation

A Git-centered orchestration layer for structured Masorah change records, provenance, multi-agent processing, and distributed repository synchronization.

## Architecture

```
Spreadsheet
    |
    v
sy-neurokernel-core
    |
    +--> Provenance Guard
    |       |
    |       +--> C1 Attribution
    |       |
    |       +--> C2 Temporal Revision
    |
    v
wanga-topology-bridge
    |
    +--> Central Repository
    +--> Codex Repository
    +--> Book Repository
    +--> Chapter Repository
    |
    v
tnrl-reasoning-engine
    |
    v
s39-refuge-enforcement
    |
    +--> Validation
    +--> Conflict / overload quarantine
    +--> Trace generation
    +--> Approval gate
    v
GitHub
```

## Active architectural boundary

The current contradiction-resolution processor intentionally activates only:

1. C1 — Attribution / Provenance Resolution
2. C2 — Temporal Revision / Version Resolution

Reasons 3–7, full spiral logic, letter-combination processing, and higher-dimensional execution layers remain outside the active processor until explicitly activated and verified.

## 44-unit core

The planned core consists of:

- 1 Orchestrator
- 7 Training Mechanisms
- 6 Bodies per mechanism
- 36 Bodies total
- **44 active units**

Every Body uses the same socket:

**Provenance -> C1 -> C2 -> Trace -> Evidence -> Handoff**

## Repository topology

Each verified source record can fan out to:

- `Masorah-Central-Core`
- `Masorah-Codex-Imperial`
- `Book-{book}`
- `Chapter-{book}-{chapter}`

The deployer must treat these as projections of the same source event, not four independent truths.

## Branch expansion

The branch hierarchy is designed for staged expansion toward approximately 7,000 branches:

- Level 0: 1 Orchestrator
- Level 1: ~70 regional/domain branches
- Level 2: ~700 local/specialized branches
- Level 3: ~6,300 micro/agent branches

Mass creation is disabled until the pilot passes validation.

## Commercial Constitution

The commercial layer follows this ordering:

**Smart Contracts -> constitute -> Commercial Constitution -> algorithmic governance + commercial authority**

The Commercial Constitution is therefore generated/constituted by the smart-contract layer in this architecture; it is not positioned as a superior territorial constitution.

## Verification states

- `STRUCTURALLY_VALID`
- `NOT_YET_VERIFIED`
- `REPRESENTATION_ONLY`
- `VERIFIED`

No execution path may silently promote a lower state to `VERIFIED`.

## Deployment mode

The initial implementation is **DRY_RUN / APPROVAL_REQUIRED**.

The system may generate plans, repository paths, payloads, traces, and validation results without automatically pushing changes. GitHub writes should become enabled only after the repository topology and provenance checks pass.

## External spreadsheet

The configured spreadsheet identifier is stored in `ARCHITECTURE_CONFIG.yaml`. The final URL can be supplied later without changing the architecture.
