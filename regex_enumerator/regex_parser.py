from .regex_tree import Alternative, BackReference, CharClass, RegexTree


class RegexError(Exception):
    def __init__(self, regex: str, index: int, message: str):
        self.regex = regex
        self.index = index
        self.message = message

    def __str__(self):
        caret_line = ' ' * self.index + '^'
        return f"\n{self.regex}\n{caret_line}\n{self.message}"


class RegexParser:
    WORDS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
    HEX = '0123456789abcdefABCDEF'
    DIGITS = '0123456789'
    SPACES = ' \t\n\r\f\v'

    def __init__(self, regex: str, charset: str) -> None:
        self.regex = regex
        self.charset = charset

    def parse(self) -> RegexTree:
        self.index = 0
        return self._parseRegex(False)

    def _parseRegex(self, to_close: bool) -> RegexTree:
        alternatives: list[Alternative] = []
        elements: list[CharClass | RegexTree | BackReference] = []
        named_groups: dict[str, RegexTree] = {}
        ordered_groups: list[RegexTree] = []
        min_len_group, max_len_group = 1, 1

        while self.index < len(self.regex):
            char = self.regex[self.index]
            self.index += 1
            match char:
                case'(':
                    if self.index < len(self.regex) and self.regex[self.index] == '?':
                        self.index += 1
                        if self.index >= len(self.regex):
                            self._raise_error("Invalid group")
                        elif self.regex[self.index] == '<':
                            self.index += 1
                            name = ''
                            while self.index < len(self.regex) and self.regex[self.index] != '>':
                                name += self.regex[self.index]
                                self.index += 1
                            if self.index >= len(self.regex) or self.regex[self.index] != '>' or name == '':
                                self._raise_error("Invalid named group")
                            self.index += 1
                            if name in named_groups:
                                self._raise_error("Duplicate named group")
                            subTree = self._parseRegex(True)
                            named_groups[name] = subTree
                            ordered_groups.append(subTree)
                        elif self.regex[self.index] == ':':
                            self.index += 1
                            subTree = self._parseRegex(True)
                        else:
                            self._raise_error("Invalid group")
                    else:
                        subTree = self._parseRegex(True)
                        ordered_groups.append(subTree)
                    elements.append(subTree)
                case ')':
                    if not to_close:
                        self._raise_error("Unmatched closing parenthesis")
                    min_len_group, max_len_group = self._parseQuantifier()
                    to_close = False
                    break
                case '|':
                    alternatives.append(Alternative(elements))
                    elements = []
                    named_groups = {}
                    ordered_groups = []
                case '[':
                    chars = self._parseCharClass()
                    min_len, max_len = self._parseQuantifier()
                    elements.append(
                        CharClass(chars, min_len, max_len))
                case '.':
                    chars = list(self.charset)
                    min_len, max_len = self._parseQuantifier()
                    elements.append(
                        CharClass(chars, min_len, max_len))
                case '\\':
                    reference = self._parseBackReferenceLookahead()
                    if reference is None:
                        chars = self._parseEscapeChar()
                        min_len, max_len = self._parseQuantifier()
                        elements.append(
                            CharClass([chars], min_len, max_len))
                        continue
                    if isinstance(reference, str):
                        if reference not in named_groups:
                            self._raise_error("Named back reference not found")
                        group = named_groups[reference]
                    else:
                        if reference < 1 or reference > len(ordered_groups):
                            self._raise_error(
                                "Positional back reference not found")
                        group = ordered_groups[reference - 1]
                    min_len, max_len = self._parseQuantifier()
                    reference = BackReference(group, min_len, max_len)
                    group.add_reference(reference)
                    elements.append(reference)
                case _:
                    min_len, max_len = self._parseQuantifier()
                    elements.append(
                        CharClass([char], min_len, max_len))

        if to_close:
            self._raise_error("Unmatched opening parenthesis")

        alternatives.append(Alternative(elements))
        return RegexTree(alternatives, min_len_group, max_len_group)

    def _parseBackReferenceLookahead(self) -> str | int | None:
        if len(self.regex) <= self.index:
            self._raise_error("Incomplete escape sequence")

        char = self.regex[self.index]

        match char:
            case 'k':
                self.index += 1
                name = ''
                if len(self.regex) <= self.index or self.regex[self.index] != '<':
                    self._raise_error("Invalid named back reference")
                self.index += 1
                while self.index < len(self.regex) and self.regex[self.index] != '>':
                    name += self.regex[self.index]
                    self.index += 1
                if len(self.regex) <= self.index or self.regex[self.index] != '>' or name == '':
                    self._raise_error("Invalid named back reference")
                self.index += 1
                return name
            case char if char.isdigit():
                num = int(char)
                self.index += 1
                while self.index < len(self.regex) and self.regex[self.index].isdigit():
                    num = num * 10 + int(self.regex[self.index])
                    self.index += 1
                return num

    def _parseEscapeChar(self) -> str:

        if len(self.regex) <= self.index:
            self._raise_error("Incomplete escape sequence")

        char = self.regex[self.index]
        self.index += 1

        match char:
            case 'd': return self.DIGITS
            case 'D': return ''.join([c for c in self.charset if not c.isdigit()])
            case 'w': return self.WORDS
            case 'W': return ''.join([c for c in self.charset if c not in self.WORDS])
            case 's': return self.SPACES
            case 'S': return ''.join([c for c in self.charset if c not in self.SPACES])
            case 't': return '\t'
            case 'r': return '\r'
            case 'n': return '\n'
            case 'v': return '\v'
            case 'f': return '\f'
            case 'x':
                if len(self.regex) < self.index + 1 or self.regex[self.index] not in self.HEX:
                    self._raise_error('Invalid ASCII escape character')
                if len(self.regex) < self.index + 2 or self.regex[self.index + 1] not in self.HEX:
                    num = int(self.regex[self.index], 16)
                    self.index += 1
                else:
                    num = int(self.regex[self.index: self.index + 2], 16)
                    self.index += 2
                if num < 32 or num > 126:
                    self._raise_error(f"Invalid ASCII escape character {num}")
                return chr(num)
            case 'u':
                code = []
                for _ in range(4):
                    if len(self.regex) <= self.index or self.regex[self.index] not in self.HEX:
                        self._raise_error("Invalid unicode escape character")
                    code.append(self.regex[self.index])
                    self.index += 1
                num = int(''.join(code), 16)
                return chr(num)
            case 'p' | 'P':
                self._raise_error("Unicode property not supported")
            case _: return char

    def _parseCharClass(self) -> list[str]:
        chars_list: list[str] = []
        first_char = None
        range_divider = False
        negated = False

        if len(self.regex) <= self.index:
            self._raise_error("Unclosed character class")

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
            if char == '\\':
                escape_char = self._parseEscapeChar()
                if len(escape_char) > 1 or escape_char == '-':
                    chars_list.append(escape_char)
                    if range_divider:
                        chars_list.append('-')
                        assert first_char is not None
                        chars_list.append(first_char)
                    elif first_char is not None:
                        chars_list.append(first_char)
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
                chars_list.append(first_char)
                first_char = char

        if len(self.regex) <= self.index or self.regex[self.index] != ']':
            self._raise_error("Unclosed character class")

        self.index += 1

        if range_divider:
            chars_list.append('-')
            assert first_char is not None
            chars_list.append(first_char)
        elif first_char is not None:
            chars_list.append(first_char)

        if negated:
            chars_list = [
                c for c in self.charset if c not in ''.join(chars_list)]

        return chars_list

    def _parseQuantifier(self) -> tuple[int, int | None]:

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

    def _parseMinMax(self) -> tuple[int, int | None]:
        self._skipSpaces()

        min_len = 0
        if self.index >= len(self.regex) or not self.regex[self.index].isdigit():
            self._raise_error("Invalid quantifier")
        while self.index < len(self.regex) and self.regex[self.index].isdigit():
            min_len = min_len * 10 + int(self.regex[self.index])
            self.index += 1

        self._skipSpaces()

        if self.index >= len(self.regex):
            self._raise_error("Invalid quantifier")

        if self.regex[self.index] == '}':
            self.index += 1
            return min_len, min_len
        if self.regex[self.index] != ',':
            self._raise_error("Invalid quantifier")

        self.index += 1
        self._skipSpaces()

        if self.index >= len(self.regex) or self.regex[self.index] not in '0123456789}':
            self._raise_error("Invalid quantifier")

        if self.regex[self.index] == '}':
            self.index += 1
            return min_len, None

        max_len = 0
        while self.index < len(self.regex) and self.regex[self.index].isdigit():
            max_len = max_len * 10 + int(self.regex[self.index])
            self.index += 1

        if max_len < min_len:
            self._raise_error(
                "Max length cannot be less than min length in quantifier")

        self._skipSpaces()

        if self.index >= len(self.regex) or self.regex[self.index] != '}':
            self._raise_error("Invalid quantifier")
        self.index += 1

        return min_len, max_len

    def _skipSpaces(self):
        while self.index < len(self.regex) and self.regex[self.index] == ' ':
            self.index += 1

    def _raise_error(self, message: str):
        raise RegexError(self.regex, self.index, message)
