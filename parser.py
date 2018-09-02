from typing import NamedTuple, Union, List, Tuple


class Tree(list):
    def __init__(self, *values):
        super().__init__(values)


class Token(NamedTuple):
    name: str
    value: Union[str, int, None]


Tokens = List[Token]


class UnmatchedProduction(Exception):
    pass


class Production:
    def __init__(self, name):
        self.name = name

    def match(self, tokens: List[Token]) -> Tuple[Tree, Tokens]:
        """Match self's rule to `tokens` and return derived tree."""
        raise NotImplementedError

    def repeat(self):
        """Return new """
        pass


class NonTerminal(Production):
    def __init__(self, name, productions):
        super().__init__(name)
        self.productions = productions

    def match(self, tokens: List[Token]) -> Tuple[Tree, Tokens]:
        tree = Tree()
        remaining_tokens = tokens
        for production in self.productions:
            subtree, remaining_tokens = production.match(remaining_tokens)
            tree.append(subtree)
        return Tree(self.name, tree), remaining_tokens


class Terminal(Production):
    def match(self, tokens: List[Token]) -> Tuple[Tree, Tokens]:
        first_token: Token = tokens[0]
        if first_token.name == self.name:
            return Tree(self.name, first_token.value), tokens[1:]
        raise UnmatchedProduction


class RepeatingProduction(Production):
    """
    Match a given production zero or more times and return anonymous node.

    This class is equivalent to `{production}` in EBNF.
    """
    def __init__(self, production):
        super().__init__("")
        self.production = production

    def match(self, tokens: List[Token]):
        tree = Tree()
        remaining_tokens = tokens
        while True:
            try:
                subtree, remaining_tokens = \
                    self.production.match(remaining_tokens)
                tree.append(subtree)
            except UnmatchedProduction:
                break

        return Tree(self.name, tree), remaining_tokens
