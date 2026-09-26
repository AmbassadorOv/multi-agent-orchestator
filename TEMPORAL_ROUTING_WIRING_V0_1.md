# Temporal Routing Wiring

The runtime should be composed as four independent components:

    ChartTemporalSnapshotAdapter
                |
                v
    TemporalNetworkRouter <---- GitHubTemporalSnapshotAdapter
                |
                v
    build_instruction_envelope()
                |
                v
    ThinkingMachineGateway
                |
                v
    normalized response

## One request = one frozen temporal state

The router must resolve the state once at the beginning of the request.

Do not do this:

    query -> repository A at t0
          -> chart at t1
          -> repository B at t2

Do this:

    query -> freeze t
          -> chart(t)
          -> GitHub-state(t)
          -> route_id
          -> Thinking Machine

This prevents temporal drift inside a single reasoning episode.

## Moving GitHub state

GitHub is not treated as a physical coordinate system. What moves is the
observable software state: refs, commits, files, workflows and configuration.

The temporal address therefore identifies a state snapshot, not merely a URL.

## Route secrecy

If a secret is configured, the route identifier uses HMAC-SHA256.
This provides an authenticated opaque identifier, not a claim that the whole
network payload is encrypted.

Actual transport encryption must still be supplied by TLS or another secure
transport.

## Astronomy image binding

Every map artifact should be bound to:

    route_id
    observed_at_utc
    map_image_hash

A later rendering must produce a different artifact hash if its contents
differ.

## Thinking Machine

The Thinking Machine is downstream of the temporal resolver. It receives the
frozen envelope and returns processing results.

It does not decide the repository address itself.
