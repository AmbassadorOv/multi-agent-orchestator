"""Typed symbolic connectivity graph for the 22-letter layer."""
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
from .hebrew22 import LETTER_BY_SYMBOL

@dataclass(frozen=True)
class NeuralEdge:
    source: str
    target: str
    relation: str
    weight: float = 1.0
    direction: str = "directed"
    status: str = "MODEL"

class LetterConnectivityGraph:
    RELATIONS = {"adjacency","filling","filling_of_filling","final_form",
                 "phonetic","numeric_equivalence","mirror","composition"}

    def __init__(self):
        self._edges: List[NeuralEdge] = []

    def add_edge(self, source, target, relation, *, weight=1.0,
                 direction="directed", status="MODEL"):
        if source not in LETTER_BY_SYMBOL or target not in LETTER_BY_SYMBOL:
            raise ValueError(f"edge endpoints must be base 22-letter symbols: {source!r}, {target!r}")
        if relation not in self.RELATIONS:
            raise ValueError(f"unsupported relation: {relation!r}")
        self._edges.append(NeuralEdge(source,target,relation,weight,direction,status))

    def add_undirected(self, a, b, relation, *, weight=1.0, status="MODEL"):
        self.add_edge(a,b,relation,weight=weight,direction="undirected",status=status)
        self.add_edge(b,a,relation,weight=weight,direction="undirected",status=status)

    def edges(self, relation=None):
        return tuple(e for e in self._edges if relation is None or e.relation == relation)

    def neighbors(self, symbol, relation=None):
        return tuple(e.target for e in self.edges(relation) if e.source == symbol)

    def propagate(self, activations: Dict[str,float], *, relation=None, threshold=0.0):
        out = dict(activations)
        for edge in self.edges(relation):
            value = activations.get(edge.source, 0.0) * edge.weight
            if value > threshold:
                out[edge.target] = out.get(edge.target, 0.0) + value
        return out

    def as_dict(self):
        return {"node_count":22, "edge_count":len(self._edges),
                "edges":[asdict(e) for e in self._edges],
                "invariant":"symbolic connectivity is a computational graph, not a claim about biological neurons"}

def build_base_connectivity():
    g = LetterConnectivityGraph()
    symbols = tuple(LETTER_BY_SYMBOL)
    for a,b in zip(symbols,symbols[1:]):
        g.add_undirected(a,b,"adjacency")
    for a in ("כ","נ","פ","צ","מ"):
        g.add_edge(a,a,"final_form",status="MODEL")
    g.add_undirected("י","ס","numeric_equivalence",status="SOURCE_CLAIM")
    g.add_undirected("ק","ל","numeric_equivalence",status="SOURCE_CLAIM")
    for a,b in (("א","פ"),("ה","ק"),("ד","ת"),("ג","ע"),("ז","נ")):
        g.add_undirected(a,b,"mirror",status="SOURCE_CLAIM")
    return g
