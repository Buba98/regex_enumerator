from .regex_parser import RegexParser
from .regex_tree import RegexTree


class RegexEnumerator:
    def __init__(self, regex: str, additional_charset: str | list[str] = None) -> None:
        default_charset = [chr(c) for c in range(32, 127)]

        if additional_charset is None:
            additional = []
        elif isinstance(additional_charset, list):
            additional = list(''.join(additional_charset))
        else:
            additional = list(additional_charset)

        charset = ''.join(sorted(set(default_charset + additional)))
        parser = RegexParser(regex, charset)
        self.regexTree: RegexTree = parser.parse()
        self.current: list[str] = list(self.regexTree.current)
        self.done: bool = self.regexTree.done and len(self.current) == 0

    def next(self) -> str | None:
        if len(self.current) != 0:
            res = self.current.pop()
            self.done = self.regexTree.done and len(self.current) == 0
            return res

        while True:
            if self.regexTree.done:
                self.done = True
                return None
            self.current = list(self.regexTree.next())
            if len(self.current) != 0:
                break

        res = self.current.pop()
        self.done = self.regexTree.done and len(self.current) == 0
        return res
