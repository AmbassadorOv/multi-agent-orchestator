"""Orchestration boundary between forms, symbolic logic, and neural agents."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Sequence
from .combinator import CombinationEngine
from .hebrew22 import HEBREW_22, LETTER_BY_SYMBOL
from .modes28 import THOUGHT_MODES_28, get_mode

@dataclass(frozen=True)
class OrchestrationRequest:
    user_input: str
    letters: Sequence[str] = field(default_factory=tuple)
    mode_id: str = "TM-01"
    arity: int = 2
    include_combinations: bool = True
    include_permutations: bool = False
    max_preview: int = 16

@dataclass(frozen=True)
class OrchestrationResult:
    mode_id: str
    operation: str
    normalized_letters: tuple[str,...]
    topology: Dict[str,Any]
    combinatorics: Dict[str,Any]
    trace: List[Dict[str,Any]]

class NeuralLogicOrchestrator:
    def __init__(self, alphabet=HEBREW_22):
        self.alphabet = tuple(alphabet)
        self.engine = CombinationEngine([n.symbol for n in self.alphabet])

    def prepare(self, request: OrchestrationRequest) -> OrchestrationResult:
        mode = get_mode(request.mode_id)
        letters = self._normalize_letters(request.letters)
        if not letters:
            letters = tuple(n.symbol for n in self.alphabet)
        engine = CombinationEngine(letters)
        arity = min(request.arity, len(letters))
        trace = [
            {"stage":"FORM_INPUT","status":"ACCEPTED","user_input":request.user_input},
            {"stage":"SYMBOL_NORMALIZATION","status":"ACCEPTED","letters":list(letters)},
            {"stage":"MODE_SELECTION","status":"SELECTED","mode_id":mode.mode_id},
            {"stage":"COMBINATORIAL_ENGINE","status":"READY","arity":arity},
        ]
        combinatorics = {
            "alphabet_size":len(letters),
            "arity":arity,
            "combination_count":engine.combination_count(arity),
            "permutation_count":engine.permutation_count(arity),
        }
        if request.include_combinations:
            combinatorics["combination_preview"] = [
                "".join(item) for _,item in zip(range(request.max_preview),engine.combinations(arity))
            ]
        if request.include_permutations:
            combinatorics["permutation_preview"] = [
                "".join(item) for _,item in zip(range(request.max_preview),engine.permutations(arity))
            ]
        topology = {
            "node_count":len(letters),
            "nodes":[{"symbol":s,"index":LETTER_BY_SYMBOL[s].index,
                      "gematria":LETTER_BY_SYMBOL[s].gematria} for s in letters],
            "mode_count":len(THOUGHT_MODES_28),
            "selected_mode":mode.mode_id,
        }
        trace.append({"stage":"OUTPUT_OBJECT","status":"READY_FOR_NEURAL_LAYER",
                      "invariant":"symbolic representation is not the physical referent"})
        return OrchestrationResult(mode.mode_id,mode.operation,letters,topology,combinatorics,trace)

    def _normalize_letters(self, letters: Sequence[str]) -> tuple[str,...]:
        normalized=[]; seen=set()
        for symbol in letters:
            if symbol not in LETTER_BY_SYMBOL:
                raise ValueError(f"unsupported base-alphabet symbol: {symbol!r}")
            if symbol not in seen:
                normalized.append(symbol); seen.add(symbol)
        return tuple(normalized)
