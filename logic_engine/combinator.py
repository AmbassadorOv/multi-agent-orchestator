"""Lazy combinatorial operations over the 22-letter symbolic alphabet."""
from dataclasses import dataclass
from itertools import combinations, permutations, product
from math import comb, factorial
from typing import Iterator, Sequence, Tuple, TypeVar

T = TypeVar("T")

@dataclass(frozen=True)
class CombinationResult:
    operation: str
    input_size: int
    arity: int
    cardinality: int
    values: Tuple[Tuple[T, ...], ...] | None = None

class CombinationEngine:
    def __init__(self, alphabet: Sequence[T]):
        if not alphabet:
            raise ValueError("alphabet must not be empty")
        self.alphabet = tuple(alphabet)

    @property
    def size(self) -> int:
        return len(self.alphabet)

    def combination_count(self, k: int) -> int:
        self._validate_k(k)
        return comb(self.size, k)

    def permutation_count(self, k: int | None = None) -> int:
        k = self.size if k is None else k
        self._validate_k(k)
        return factorial(self.size) // factorial(self.size-k)

    def combinations(self, k: int) -> Iterator[Tuple[T, ...]]:
        self._validate_k(k)
        yield from combinations(self.alphabet, k)

    def permutations(self, k: int | None = None) -> Iterator[Tuple[T, ...]]:
        k = self.size if k is None else k
        self._validate_k(k)
        yield from permutations(self.alphabet, k)

    def cartesian(self, k: int, repeat: bool = True) -> Iterator[Tuple[T, ...]]:
        if k < 0:
            raise ValueError("arity must be >= 0")
        if repeat:
            yield from product(self.alphabet, repeat=k)
        else:
            yield from permutations(self.alphabet, k)

    def summary(self, k: int) -> dict:
        return {"alphabet_size":self.size,"arity":k,
                "combinations_without_repetition":self.combination_count(k),
                "ordered_selections_without_repetition":self.permutation_count(k),
                "cartesian_with_repetition":self.size**k}

    def _validate_k(self, k: int) -> None:
        if not 0 <= k <= self.size:
            raise ValueError(f"arity must be between 0 and {self.size}")
