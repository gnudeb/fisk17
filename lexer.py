import re
from typing import List


class Rule:
    def __init__(self, name, pattern, post_action=None):
        self.name = name
        self.regex = re.compile(pattern)
        self.post_action = post_action


class Lexer:

    def __init__(self, *rules):
        self.rules: List[Rule] = [Rule(*args) for args in rules]

    def produce_tokens(self, code: str):
        tokens = []
        shift = 0

        while shift < len(code):
            match = None
            for rule in self.rules:
                match = rule.regex.match(code, pos=shift)
                if match:
                    _, shift = match.span()
                    value = match.group()
                    if rule.post_action:
                        tokens.append((rule.name, rule.post_action(value)))
                    break
            if not match:
                raise Exception

        return tokens
