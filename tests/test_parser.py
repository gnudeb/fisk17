from parser import Terminal, NonTerminal, Token


def test_terminal():
    production = Terminal("NUMBER")

    tokens = [
        Token("NUMBER", 5),
        Token("END", None)
    ]

    tree, remaining_tokens = production.match(tokens)

    assert tree == ["NUMBER", 5]
    assert remaining_tokens == [Token("END", None)]


def test_non_terminal():
    production = NonTerminal("number", [
        Terminal("NUMBER")
    ])

    tokens = [
        Token("NUMBER", 5),
        Token("END", None)
    ]

    tree, remaining_tokens = production.match(tokens)

    assert tree == [
        "number", [
            ["NUMBER", 5]
        ]
    ]
    assert remaining_tokens == [Token("END", None)]


def test_compound_non_terminal():
    production = NonTerminal("expr", [
        Terminal("NUMBER"),
        Terminal("PLUS"),
        Terminal("NUMBER")
    ])

    tokens = [
        Token("NUMBER", 5),
        Token("PLUS", None),
        Token("NUMBER", 3),
    ]

    tree, remaining_tokens = production.match(tokens)

    assert tree == [
        "expr", [
            ["NUMBER", 5],
            ["PLUS", None],
            ["NUMBER", 3]
        ]
    ]
    assert remaining_tokens == []


def test_repeating_terminal():
    production = Terminal("NUMBER").repeat()

    tokens = [
        Token("NUMBER", 5),
        Token("NUMBER", 2),
        Token("NUMBER", 4),
        Token("PLUS", None),
        Token("NUMBER", 3),
    ]

    tree, remaining_tokens = production.match(tokens)

    assert tree == [
        "expr", [
            ["NUMBER", 5],
            ["NUMBER", 2],
            ["NUMBER", 4],
        ]
    ]
    assert remaining_tokens == [
        Token("PLUS", None),
        Token("NUMBER", 3),
    ]
