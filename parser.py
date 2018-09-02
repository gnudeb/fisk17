from typing import NamedTuple, Union, List, Tuple, Any


class Node(NamedTuple):
    value: Any = ""
    children: Tuple['Node', ...] = tuple()


class Token(NamedTuple):
    name: str
    value: Union[str, int, None] = None


Tokens = List[Token]


class UnmatchedProduction(Exception):
    pass


class Production:
    """
    An abstract production.

    All concrete productions inherit from this class.
    """
    def __init__(self, name):
        self.name = name

    def __or__(self, other):
        return OrProduction(self, other)

    def match(self, tokens: List[Token]) -> Tuple[Node, Tokens]:
        """Match self's rule to `tokens` and return derived tree."""
        raise NotImplementedError

    def repeat(self):
        """Return new """
        pass


class OrProduction(Production):
    """
    An equivalent to `p1 | p2 | ... | pn` in EBNF.

    It will try to match each production in strict order and return first that
    matched. If none were matched, `UnmatchedProduction` will be raised.
    """
    def __init__(self, *productions):
        super().__init__("")
        self.productions = []
        for production in productions:
            if isinstance(production, OrProduction):
                self.productions.extend(production.productions)
            else:
                self.productions.append(production)

    def __eq__(self, other):
        if not isinstance(other, OrProduction):
            return False
        return self.productions == other.productions

    def __ne__(self, other):
        return not self == other

    def match(self, tokens: List[Token]):
        for production in self.productions:
            try:
                return production.match(tokens)
            except UnmatchedProduction:
                pass
        raise UnmatchedProduction


class NonTerminal(Production):
    """
    A non-terminal production.

    It will match given productions in strict order. If any of given
    productions raise exceptions, it is up to caller to catch them.
    """
    def __init__(self, name, productions):
        super().__init__(name)
        self.productions = productions

    def match(self, tokens: List[Token]) -> Tuple[Node, Tokens]:
        subtrees: List[Node] = []
        remaining_tokens = tokens
        for production in self.productions:
            subtree, remaining_tokens = production.match(remaining_tokens)
            subtrees.append(subtree)
        return Node(self.name, tuple(subtrees)), remaining_tokens


class Terminal(Production):
    """
    A terminal production.

    It will match any token that has the same name as `self.name`. If a token
    cannot be matched, `Terminal` will raise `UnmatchedProduction`.
    If matched token has no value, the returned `Node` will have no children,
    instead of having a child with value of `None`.

    This class is equivalent to a terminal production in EBNF.
    """
    def match(self, tokens: List[Token]) -> Tuple[Node, Tokens]:
        first_token: Token = tokens[0]
        if first_token.name == self.name:
            if first_token.value is not None:
                children = (Node(first_token.value),)
            else:
                children = ()
            return Node(self.name, children), tokens[1:]
        raise UnmatchedProduction


class RepeatingProduction(Production):
    """
    An equivalent to `{production}` in EBNF.

    It will match a given production zero or more times and return anonymous
    node.
    """
    def __init__(self, production):
        super().__init__("")
        self.production = production

    def match(self, tokens: List[Token]):
        subtrees = []
        remaining_tokens = tokens
        while True:
            try:
                subtree, remaining_tokens = \
                    self.production.match(remaining_tokens)
                subtrees.append(subtree)
            except UnmatchedProduction:
                break

        return Node(self.name, tuple(subtrees)), remaining_tokens
