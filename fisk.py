from functools import partial

from lexer import Lexer


_hex = partial(int, base=16)
_bin = partial(int, base=2)

def _empty(_):
    return None


directives = ["org", "db", "end"]
operations = ["mov", "int", "jmp"]
symbols = [",", r"\[", r"\]", "end"]


fisk_lexer = Lexer(
    ("WHITESPACE", "[ \t]"),
    ("COMMENT", ";[^;\n]+"),
    ("NEWLINE", "\n", _empty),
    ("SYMBOL", "|".join(symbols), str),
    ("DIRECTIVE", "|".join(directives), str),
    ("OPERATION", "|".join(operations), str),
    ("REGISTER", "r[lh][0-7]|r[0-9a-f]", str),
    ("NUMBER", "0x[0-9a-f]+", _hex),
    ("NUMBER", "0b[0-1]+", _bin),
    ("NUMBER", "[0-9]+", int),
    ("LABEL", "[a-zA-Z_][a-zA-Z0-9_]+:", lambda label: label[:-1]),
    ("IDENTIFIER", "[a-zA-Z_][a-zA-Z0-9_]+", str),
    ("IDENTIFIER", r"\$", str),
    ("STRING", "'[^'\n]*'", lambda s: s[1:-1]),
    ("STRING", '"[^"\n]*"', lambda s: s[1:-1]),
)
