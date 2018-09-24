from lexer import Lexer, Rule


directives = ["org", "db", "end"]
operations = ["mov", "int", "jmp"]
symbols = [",", r"\[", r"\]", "end"]


def _hex(value: str):
    return int(value, 16)


def _bin(value: str):
    return int(value, 2)


class FiskLexer(Lexer):
    def __init__(self):
        super().__init__((
            Rule("WHITESPACE", "[ \t]", ignore=True),
            Rule("COMMENT", ";[^;\n]+", ignore=True),
            Rule("NEWLINE", "\n", post_action=self.increment_line, ignore=True),
            Rule("SYMBOL", "|".join(symbols)),
            Rule("DIRECTIVE", "|".join(directives)),
            Rule("OPERATION", "|".join(operations)),
            Rule("REGISTER", "r[lh][0-7]|r[0-9a-f]"),
            Rule("NUMBER", "0x[0-9a-f]+", _hex),
            Rule("NUMBER", "0b[0-1]+", _bin),
            Rule("NUMBER", "[0-9]+", int),
            Rule("LABEL", "([a-zA-Z_][a-zA-Z0-9_]+):"),
            Rule("IDENTIFIER", "[a-zA-Z_][a-zA-Z0-9_]+"),
            Rule("IDENTIFIER", r"\$"),
            Rule("STRING", "'[^'\n]*'", lambda s: s[1:-1]),
            Rule("STRING", '"[^"\n]*"', lambda s: s[1:-1]),
        ))

    def increment_line(self):
        self.current_line += 1
