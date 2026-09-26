"""Canonical 22-letter Hebrew base alphabet."""
from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass(frozen=True)
class LetterNode:
    index: int
    symbol: str
    name: str
    gematria: int

HEBREW_22: Tuple[LetterNode, ...] = (
    LetterNode(1,"א","aleph",1), LetterNode(2,"ב","bet",2),
    LetterNode(3,"ג","gimel",3), LetterNode(4,"ד","dalet",4),
    LetterNode(5,"ה","he",5), LetterNode(6,"ו","vav",6),
    LetterNode(7,"ז","zayin",7), LetterNode(8,"ח","het",8),
    LetterNode(9,"ט","tet",9), LetterNode(10,"י","yod",10),
    LetterNode(11,"כ","kaf",20), LetterNode(12,"ל","lamed",30),
    LetterNode(13,"מ","mem",40), LetterNode(14,"נ","nun",50),
    LetterNode(15,"ס","samekh",60), LetterNode(16,"ע","ayin",70),
    LetterNode(17,"פ","pe",80), LetterNode(18,"צ","tsadi",90),
    LetterNode(19,"ק","qof",100), LetterNode(20,"ר","resh",200),
    LetterNode(21,"ש","shin",300), LetterNode(22,"ת","tav",400),
)
LETTER_BY_SYMBOL: Dict[str, LetterNode] = {n.symbol:n for n in HEBREW_22}
