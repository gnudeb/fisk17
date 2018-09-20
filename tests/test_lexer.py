from lexer import Lexer, Rule


def test_empty_input():
    lexer = Lexer()
    assert list(lexer.tokens("")) == []


def test_simple_input():
    lexer = Lexer((
        Rule("WHITESPACE", "[ \t\n]+", ignore=True),
        Rule("NUMBER", "[0-9]+", int),
    ))
    assert list(lexer.tokens("2 5 10")) == [
        ("NUMBER", 2),
        ("NUMBER", 5),
        ("NUMBER", 10),
    ]
