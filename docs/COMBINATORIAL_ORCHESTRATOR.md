# 22-Letter / 28-Mode Neural Logic Orchestrator

## Purpose

This module adds a deterministic symbolic layer to the existing multi-agent orchestrator. It prepares a structured object that can be passed to neural agents and records the transformation path.

## Pipeline

FORM -> SYMBOL NORMALIZATION -> LOGICAL REPRESENTATION -> 22-LETTER COMBINATORIAL ENGINE -> 28-MODE ROUTER -> NEURAL AGENT -> VERIFICATION / RESPONSE

## Base alphabet

The computational registry contains the 22 ordinary Hebrew letters:

א ב ג ד ה ו ז ח ט י כ ל מ נ ס ע פ צ ק ר ש ת

Final forms are not separate nodes in this first version.

## Combinatorial scale

For an alphabet of 22 symbols:

- 22 choose 2 = 231 unordered pairs.
- 22 permute 2 = 462 ordered pairs.
- 22 choose 3 = 1,540 unordered triples.
- 22 permute 3 = 9,240 ordered triples.
- 22 squared = 484 two-position selections when repetition is allowed.
- 22 factorial is enormous, so full permutation materialization is intentionally avoided; permutations are lazy iterators.

The engine exposes exact counts and bounded previews.

## Architectural invariant

The engine treats symbols as representations. It does not assert that a letter, combination, numerical value, or neural activation is physically identical to the thing it represents.

## 28 modes

TM-01 through TM-28 are stable computational slots. Their current operator names are implementation placeholders. Historical or source-derived names should only be introduced after source verification.

## Integration contract

NeuralLogicOrchestrator.prepare() returns the selected mode, normalized symbols, topology, exact combinatorial cardinalities, bounded previews, and an execution trace.

A later adapter can feed this object into the existing Orchestrator.route_request() without changing the existing agent implementations.
