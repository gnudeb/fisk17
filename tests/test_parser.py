from parser import Terminal, NonTerminal, Token, RepeatingProduction, Node, \
    OrProduction


def test_terminal():
    production = Terminal("NUMBER")

    tokens = [
        Token("NUMBER", 5),
        Token("END", None)
    ]

    tree, remaining_tokens = production.match(tokens)

    assert tree == \
           Node("NUMBER", (
               Node(5),
        ))
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

    assert tree == \
           Node("number", (
               Node("NUMBER", (
                   Node(5),
            )),
        ))
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

    assert tree == \
        Node("expr", (
            Node("NUMBER", (
                Node(5),
            )),
            Node("PLUS"),
            Node("NUMBER", (
                Node(3),
            )),
        ))
    assert remaining_tokens == []


def test_repeating_terminal():
    production = RepeatingProduction(Terminal("NUMBER"))

    tokens = [
        Token("NUMBER", 5),
        Token("NUMBER", 2),
        Token("NUMBER", 4),
        Token("PLUS", None),
        Token("NUMBER", 3),
    ]

    tree, remaining_tokens = production.match(tokens)

    assert tree == \
           Node(children=(
               Node("NUMBER", (
                   Node(5),
            )),
               Node("NUMBER", (
                   Node(2),
            )),
               Node("NUMBER", (
                   Node(4),
            )),
        ))
    assert remaining_tokens == [
        Token("PLUS", None),
        Token("NUMBER", 3),
    ]


def test_or_production_operator():
    number = Terminal("NUMBER")
    dot = Terminal("DOT")

    assert number | dot == OrProduction(number, dot)
    assert number | dot != OrProduction(dot, number)
    assert dot | number != OrProduction(number, dot)


def test_or_production():
    production = Terminal("NUMBER") | Terminal("DOT")

    tokens = [
        Token("NUMBER", 5),
        Token("DOT"),
        Token("NUMBER", 4),
    ]

    tree, remaining_tokens = production.match(tokens)

    assert tree == \
        Node("NUMBER", (
            Node(5),
        ))

    tree, remaining_tokens = production.match(remaining_tokens)

    assert tree == Node("DOT")
    assert remaining_tokens == [Token("NUMBER", 4)]
