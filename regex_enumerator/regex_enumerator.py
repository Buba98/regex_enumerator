from .regex_parser import RegexParser
from .regex_tree import RegexTree


class RegexEnumerator:
    def __init__(self, regex: str):
        self.regex: str = regex
        parser = RegexParser()
        self.regexTree: RegexTree = parser.parse(regex)
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
