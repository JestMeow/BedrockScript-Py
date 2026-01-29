from enum import Enum, auto
from dataclasses import dataclass

class TokenKind(Enum):
    Root = auto()
    EndOfFile = auto()

    # Keywords
    KeywordDef = auto()
    KeywordExecute = auto()
    KeywordIf = auto()
    KeywordElse = auto()

    # Identifiers
    Identifier = auto()
    CommandSegment = auto()

    Number = auto()
    Target = auto()

    # Punctuators
    LeftParen = auto()
    RightParen = auto()
    LeftSquare = auto()
    RightSquare = auto()
    LeftCurly = auto()
    RightCurly = auto()

    Dot = auto()
    Colon = auto()
    Semicolon = auto()
    SingleQuote = auto()
    DoubleQuote = auto()

    # Arithmetic
    Plus = auto()
    Minus = auto()
    Asterisk = auto()
    Slash = auto()
    Modulo = auto()

    # Assignment
    Equal = auto()
    PlusEqual = auto()
    MinusEqual = auto()
    AsteriskEqual = auto()
    SlashEqual = auto()
    ModuloEqual = auto()
    Increment = auto()
    Decrement = auto()

    # Comparison
    Equals = auto()
    NotEquals = auto()
    Less = auto()
    Greater = auto()
    Leq = auto()
    Geq = auto()

    # Logical
    And = auto()
    Or = auto()
    Not = auto()

    # Misc
    Assign = auto()
    Access = auto()

    Block = auto()


    Unexpected = auto()


@dataclass
class Token:
    kind: TokenKind
    text: str