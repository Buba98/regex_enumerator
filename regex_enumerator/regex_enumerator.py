from .regex_parser import RegexParser
from .regex_tree import RegexTree


class RegexEnumerator:
    def __init__(self, regex: str, additional_charset: str | list[str] = None) -> None:
        default_charset = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
                           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
                           '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                           'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_',
                           '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                           'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

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
