# WANGA Ephemeral Neural Cryptography v0.1

## Principle

At every second t, the system derives a new ephemeral neural execution
configuration from the complete temporal snapshot.

    Snapshot(t)
        |
        v
    canonicalization
        |
        v
    cryptographic derivation
        |
        v
    EpochSeed(t)
        |
        +--> topology permutation
        +--> edge/routing permutation
        +--> execution configuration
        |
        v
    Ephemeral Neural Epoch(t)

The architecture is:

    t0 -> NET_EPOCH_0
    t1 -> NET_EPOCH_1
    t2 -> NET_EPOCH_2

## Important implementation distinction

The system does not require retraining neural weights from zero every second.
Instead it creates a new deterministic runtime configuration.

The configuration can alter:

- node ordering
- edge ordering
- routing paths
- activation/gating selection
- model/tool selection
- graph traversal order
- ephemeral execution identifiers

A future implementation may also derive per-epoch parameter masks, but those
must be separately versioned and tested.

## Cryptographic derivation

Without a secret:

    seed(t) = SHA-256(canonical(snapshot(t)))

With a secret:

    seed(t) = HMAC-SHA256(secret, canonical(snapshot(t)))

The HMAC form is the appropriate construction when the epoch seed must remain
unpredictable to parties that do not possess the secret.

## Temporal input

The snapshot should contain the exact observed state used by the request:

- UTC second
- chart / astronomy payload
- GitHub state
- repository routing map
- configuration state
- relevant external-provider state

Any difference in the canonical snapshot changes the derived seed.

## Reproducibility

Forensic replay requires preserving:

    epoch_id
    second
    snapshot_hash
    seed_commitment
    topology_version

A replay system can reconstruct the same epoch configuration.

## Security boundary

The temporal epoch is a cryptographic derivation layer. It is not by itself
proof of secrecy.

Confidential transport still requires TLS or equivalent secure transport.

The seed must never be logged directly when a secret is used.

## Rotation

Epoch rotation occurs at each UTC second boundary.

A request that starts during second t should retain its epoch for the complete
reasoning episode unless the protocol explicitly creates a new child epoch.

Recommended structure:

    request epoch
       |
       +-- child epoch for retrieval
       +-- child epoch for verification
       +-- child epoch for execution

Each child retains the parent epoch identifier.

## Compatibility with the Temporal Network Router

The intended chain is:

    Query
      |
      v
    TemporalNetworkRouter
      |
      v
    RouteSnapshot(t)
      |
      v
    EphemeralNetworkFactory
      |
      v
    EphemeralNeuralEpoch(t)
      |
      v
    Secondary Orchestrator
      |
      v
    Thinking Machine
      |
      v
    Response + provenance

The route and neural epoch share one temporal anchor.

## Verification states

    OBSERVED
    DERIVED
    VERIFIED
    UNVERIFIED

The generated epoch configuration is DERIVED until its implementation and
replay tests pass.
