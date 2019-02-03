import re
from typing import Tuple


def do_nothing():
    pass


class Rule:
    def __init__(
            self, name, pattern, mutator=str, post_action=do_nothing,
            ignore=False):

        self.name = name
        self.regex = re.compile(pattern)
        self.mutator = mutator
        self.post_action = post_action
        self.ignore = ignore

    def match(self, code, offset=0):
        """Return result and size of matching `code` against `self.regex`"""
        match = self.regex.match(code, offset)

        if not match:
            return None, 0

        try:
            result = match.groups()[0]
        except IndexError:
            result = match.group()

        start, end = match.span()
        size = end - start

        return result, size

    def __repr__(self):
        return f"Rule({self.name})"


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, rules: Tuple[Rule, ...]=None):
        self.rules: Tuple[Rule, ...] = rules or ()
        self.current_line = 1

    def tokens(self, code: str):
        shift = 0

        while shift < len(code):
            value = None
            for rule in self.rules:
                value, size = rule.match(code, offset=shift)
                if value:
                    shift += size
                    if not rule.ignore:
                        yield rule.name, rule.mutator(value)
                    rule.post_action()
                    break
            if not value:
                error_line = code.split("\n")[self.current_line-1]
                raise LexerError(
                    f"Unexpected input on line {self.current_line}:\n"
                    f"{error_line}"
                )
