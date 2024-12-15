from .regex_tree import Alternative, CharClasses, RegexTree


class RegexParser:
    charset = [chr(c) for c in range(32, 127)]

    def __init__(self, regex: str):
        self.regex = regex

    def parse(self) -> RegexTree:
        self.index = 0
        return self._parseRegex(False)

    def _parseRegex(self, to_close: bool) -> RegexTree:
        alternatives: list[Alternative] = []
        charClassesList: list[CharClasses | RegexTree] = []
        min_len, max_len = 1, 1

        while self.index < len(self.regex):
            match self.regex[self.index]:
                case'(':
                    self.index += 1
                    subTree = self._parseRegex(True)
                    charClassesList.append(subTree)
                case ')':
                    if to_close:
                        self.index += 1
                        min_len, max_len = self._parseQuantifier()
                        to_close = False
                        break
                    raise ValueError('Invalid regex')
                case '|':
                    alternatives.append(Alternative(charClassesList))
                    charClassesList = []
                    self.index += 1
                case _:
                    charClasses = self._parse_char_classes()
                    charClassesList.append(charClasses)

        if to_close:
            raise ValueError('Invalid regex')

        alternatives.append(Alternative(charClassesList))
        return RegexTree(alternatives, min_len, max_len)

    def _parse_char_classes(self) -> CharClasses:
        chars_list: list[str] = []

        char = self.regex[self.index]
        self.index += 1

        match char:
            case '[':   chars_list = self._parseCharClass()
            case '\\':  chars_list = self._parseEscapeChar()
            case '.':   chars_list = list(self.charset)
            case _:     chars_list = [char]

        min_len, max_len = self._parseQuantifier()
        return CharClasses(chars_list, min_len, max_len)

    def _parseEscapeChar(self) -> str:

        if len(self.regex) <= self.index:
            raise ValueError('Invalid escape character')

        char = self.regex[self.index]
        self.index += 1

        match char:
            case 'd': return '0123456789'
            case 'D': return ''.join([c for c in self.charset if c not in '0123456789'])
            case 'w': return 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
            case 'W': return ''.join([c for c in self.charset if c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'])
            case 's': return ' \t\n\r\f\v'
            case 'S': return ''.join([c for c in self.charset if c not in ' \t\n\r\f\v'])
            case 't': return '\t'
            case 'r': return '\r'
            case 'n': return '\n'
            case 'v': return '\v'
            case 'f': return '\f'
            case 'x':
                if len(self.regex) < self.index + 1 or self.regex[self.index] not in '0123456789abcdefABCDEF':
                    raise ValueError('Invalid escape character')
                if len(self.regex) < self.index + 2 or self.regex[self.index + 1] not in '0123456789abcdefABCDEF':
                    num = int(self.regex[self.index], 16)
                    self.index += 1
                else:
                    num = int(self.regex[self.index: self.index + 2], 16)
                    self.index += 2
                if num < 32 or num > 126:
                    raise ValueError('Invalid escape character')
                return chr(num)
            case _: return char

    def _parseCharClass(self) -> list[str]:
        chars_list: list[str] = []
        first_char = None
        range_divider = False
        negated = False

        if len(self.regex) <= self.index:
            raise ValueError('Invalid character class')

        if self.regex[self.index] == '^':
            negated = True
            self.index += 1

        len_regex = len(self.regex)

        while self.index < len_regex and self.regex[self.index] != ']':
            char = self.regex[self.index]
            self.index += 1

            if char == '-' and first_char is not None and not range_divider:
                range_divider = True
                continue
            elif char == '\\':
                escape_char = self._parseEscapeChar()
                if len(escape_char) > 1 or escape_char == '-':
                    chars_list.append(escape_char)
                    continue
                char = escape_char

            if first_char is None:
                first_char = char
            elif range_divider:
                chars_list.extend([chr(c) for c in range(
                    ord(first_char), ord(char) + 1)])
                first_char = None
                range_divider = False
            else:
                if first_char is not None:
                    chars_list.append(first_char)
                    first_char = None
                chars_list.append(char)

        if len(self.regex) <= self.index:
            raise ValueError('Invalid character class')

        if self.regex[self.index] != ']':
            raise ValueError('Invalid character class')

        self.index += 1

        if range_divider:
            chars_list.append('-')
        if first_char is not None:
            chars_list.append(first_char)

        if negated:
            chars_list = [c for c in self.charset if c not in chars_list]

        return chars_list

    def _parseQuantifier(self) -> tuple[int, int]:

        if len(self.regex) <= self.index:
            return 1, 1

        char = self.regex[self.index]

        match char:
            case '*':
                self.index += 1
                return 0, None
            case '+':
                self.index += 1
                return 1, None
            case '?':
                self.index += 1
                return 0, 1
            case '{':
                self.index += 1
                return self._parseMinMax()
            case _: return 1, 1

    def _parseMinMax(self) -> tuple[int, int]:
        min_len = 0
        max_len = 0

        while self.index < len(self.regex) and self.regex[self.index] == ' ':
            self.index += 1

        if self.index >= len(self.regex) or self.regex[self.index] not in '0123456789':
            raise ValueError('Invalid quantifier')

        while self.index < len(self.regex) and self.regex[self.index] in '0123456789':
            min_len = min_len * 10 + int(self.regex[self.index])
            self.index += 1

        while self.index < len(self.regex) and self.regex[self.index] == ' ':
            self.index += 1

        if self.index >= len(self.regex):
            raise ValueError('Invalid quantifier')
        elif self.regex[self.index] == '}':
            self.index += 1
            return min_len, min_len
        elif self.regex[self.index] != ',':
            raise ValueError('Invalid quantifier')

        self.index += 1

        while self.index < len(self.regex) and self.regex[self.index] == ' ':
            self.index += 1

        if self.index >= len(self.regex) or self.regex[self.index] not in '0123456789}':
            raise ValueError('Invalid quantifier')

        if self.regex[self.index] == '}':
            self.index += 1
            return min_len, None

        while self.index < len(self.regex) and self.regex[self.index] in '0123456789':
            max_len = max_len * 10 + int(self.regex[self.index])
            self.index += 1

        if max_len < min_len:
            raise ValueError('Invalid quantifier')

        while self.index < len(self.regex) and self.regex[self.index] == ' ':
            self.index += 1

        if self.index >= len(self.regex) or self.regex[self.index] != '}':
            raise ValueError('Invalid quantifier')

        self.index += 1

        return min_len, max_len
