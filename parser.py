from typing import NamedTuple, Union, List, Tuple, Any


class Node(NamedTuple):
    value: Any = ""
    children: Tuple['Node', ...] = tuple()

    def __repr__(self):
        return f"{self.value}:{self.children}"

    def as_tree(self, indent=2, level=0):
        head = str(self.value)
        tail = "\n".join(
            child.as_tree(indent, level+1) for child in self.children)
        indent_block = " "*indent*level
        if tail:
            return f"{indent_block}{head}\n{tail}"
        else:
            return f"{indent_block}{head}"

    @property
    def is_anonymous(self):
        return self.value == ""

    def normalized(self):
        """Replace each anonymous `Node` in the tree with it's children."""
        children = []
        for child in self.children:
            if child.is_anonymous:
                children.extend(child.normalized().children)
            else:
                children.append(child.normalized())
        return Node(self.value, tuple(children))


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
    def __init__(self, name, value=None):
        super().__init__(name)
        self.value = value

    def match(self, tokens: List[Token]) -> Tuple[Node, Tokens]:
        try:
            first_token: Token = tokens[0]
        except IndexError:
            raise UnmatchedProduction

        if first_token.name != self.name:
            raise UnmatchedProduction
        if self.value is not None and first_token.value != self.value:
            raise UnmatchedProduction
        if first_token.value is None:
            return Node(self.name, tuple()), tokens[1:]
        children = (Node(first_token.value),)
        return Node(self.name, children), tokens[1:]


class RepeatingProduction(Production):
    """
    An equivalent to `{production}` in EBNF.

    It will match a given production zero or more times and return anonymous
    node.
    """
    def __init__(self, *productions):
        super().__init__("")
        self.productions = productions

    def match(self, tokens: List[Token]):
        subtrees = []
        remaining_tokens = tokens
        while True:
            draft_subtrees = []
            try:
                for production in self.productions:
                    subtree, remaining_tokens = \
                        production.match(remaining_tokens)
                    draft_subtrees.append(subtree)
                subtrees.extend(draft_subtrees)
            except UnmatchedProduction:
                break

        return Node(self.name, tuple(subtrees)), remaining_tokens


class OptionalProduction(Production):
    """
    An equivalent to `[p1 p2 p3 ... pn]` in EBNF.

    It will try to match a given production once and return an anonymous `Node`
    on success and empty `Node` on failure.
    """
    def __init__(self, *productions):
        super().__init__("")
        self.productions = productions

    def match(self, tokens: List[Token]):
        subtrees = []
        remaining_tokens = tokens
        for production in self.productions:
            try:
                subtree, remaining_tokens = \
                    production.match(remaining_tokens)
            except UnmatchedProduction:
                return Node(), tokens
            subtrees.append(subtree), tokens
        return Node(self.name, tuple(subtrees)), remaining_tokens
