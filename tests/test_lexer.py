from lexer import Lexer, ignore


def test_empty_input():
    lexer = Lexer()
    assert lexer.produce_tokens("") == []


def test_simple_input():
    lexer = Lexer(
        ("WHITESPACE", "[ \t\n]+", ignore),
        ("NUMBER", "[0-9]+", int),
    )
    assert lexer.produce_tokens("2 5 10") == [
        ("NUMBER", 2),
        ("NUMBER", 5),
        ("NUMBER", 10),
    ]
