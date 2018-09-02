from parser import Terminal, NonTerminal, Token, RepeatingProduction, Node, \
    OrProduction, OptionalProduction


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


def test_terminal_with_value():
    production = NonTerminal("indirect_operand", [
        Terminal("SYMBOL", "["),
        Terminal("NUMBER"),
        Terminal("SYMBOL", "]"),
    ])

    tokens = [
        Token("SYMBOL", "["),
        Token("NUMBER", 5),
        Token("SYMBOL", "]")
    ]

    tree, remaining_tokens = production.match(tokens)

    assert tree == \
        Node("indirect_operand", (
            Node("SYMBOL", (
                Node("["),
            )),
            Node("NUMBER", (
                Node(5),
            )),
            Node("SYMBOL", (
                Node("]"),
            )),
        ))
    assert not remaining_tokens


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


def test_repeating_terminal_multiple_productions():
    production = RepeatingProduction(
        Terminal("NUMBER"),
        Terminal("DOT")
    )

    tokens = [
        Token("NUMBER", 5),
        Token("DOT"),
        Token("NUMBER", 3),
        Token("DOT"),
    ]

    tree, remaining_tokens = production.match(tokens)

    assert tree == \
        Node(children=(
            Node("NUMBER", (
                Node(5),
            )),
            Node("DOT"),
            Node("NUMBER", (
                Node(3),
            )),
            Node("DOT"),
        ))
    assert not remaining_tokens


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


def test_optional_production():
    production = OptionalProduction(
        Terminal("NUMBER"),
    )

    tokens = [
        Token("NUMBER", 5),
        Token("DOT"),
        Token("NUMBER", 4),
    ]

    tree, remaining_tokens = production.match(tokens)

    assert tree == \
        Node(children=(
            Node("NUMBER", (
                Node(5),
            )),
        ))

    tree, remaining_tokens = production.match(remaining_tokens)

    assert tree == Node()
    assert remaining_tokens == [
        Token("DOT"),
        Token("NUMBER", 4)
    ]
