# WANGA Temporal Network Routing v0.1

## Core model

    Query(t)
      |
      v
    Temporal Resolver
      +-- Chart/Astronomy Snapshot(t)
      +-- GitHub State Snapshot(t)
      +-- Repository Routing Map(t)
      +-- Configuration hashes
      |
      v
    Secondary Orchestrator
      |
      v
    Thinking Machine
      |
      v
    Normalized Response
      |
      v
    Main Network

## Repository position

A repository identity is stable, but repository state is time-varying:

- branches
- commits
- refs
- files
- workflows
- orchestration configuration

Therefore a static repository URL is not sufficient to reproduce a reasoning step.

The routing address is modeled as:

    Address(t) =
      F(
        RepositoryIdentity,
        GitState(t),
        ChartSnapshot(t),
        Configuration(t)
      )

## Temporal snapshot

Every query receives:

- UTC timestamp
- chart/astronomy snapshot
- GitHub repository snapshot
- hash of each snapshot
- derived route ID
- verification state

## Astronomical / astrological coordinate layer

The chart is used as a coordinate/configuration layer. It is not treated as evidence that astronomical positions causally control software or repository behavior.

The chart adapter must return the actual calculation for the requested instant.

A coordinate vector may contain:

- planetary longitude
- house position
- Ascendant
- Midheaven
- aspects
- any other explicitly returned chart points

The system records the values; it does not invent missing values.

## Map image

A rendered chart/map can be bound to the same snapshot using:

    map_image_id
    map_image_hash
    map_generated_at_utc
    map_source

The image is an artifact of the chart provider or renderer. The router stores its identity and hash.

## Route identifier

With a configured secret:

    route_id =
      HMAC-SHA256(
        secret,
        request_id || timestamp || chart_hash || repository_hash
      )

Without a secret:

    route_id =
      SHA256(
        request_id || timestamp || chart_hash || repository_hash
      )

The second form is an identifier, not encryption.

## Thinking Machine boundary

The Thinking Machine receives the temporal envelope and performs higher-order processing.

It must not silently replace the captured snapshot with a newer one.

## Verification boundary

The protocol distinguishes:

    OBSERVED
    VERIFIED
    INFERRED
    UNVERIFIED

A coordinate mapping is architectural metadata unless independently validated.

## Required adapters

1. GitHub snapshot adapter
2. Chart/astronomy snapshot adapter
3. Map rendering/artifact adapter
4. Secondary-orchestrator transport
5. Thinking Machine transport
6. Persistent temporal snapshot store

## Required response object

Every response should be able to return:

    request_id
    route_id
    observed_at_utc
    response
    repositories_consulted
    chart_hash
    repository_hash
    map_image_hash
    verification_state
    errors
