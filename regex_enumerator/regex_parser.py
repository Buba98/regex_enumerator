from .regex_tree import Alternative, CharClasses, RegexTree


class RegexParser:
    charset = [chr(c) for c in range(32, 127)]

    def parse(self, regex) -> RegexTree:
        _, regexTree = self._parseRegex(regex, False)
        return regexTree

    def _parseRegex(self, regex: str, to_close: bool) -> tuple[int, RegexTree]:
        alternatives: list[Alternative] = []
        charClassesList: list[CharClasses | RegexTree] = []
        min_len = 1
        max_len = 1
        closed = not to_close

        i = 0
        while i < len(regex):
            if regex[i] == '(':
                incr, subTree = self._parseRegex(regex[i + 1:], True)
                charClassesList.append(subTree)
                i += incr + 1
            elif regex[i] == ')':
                if to_close:
                    i += 1
                    incr, min_len, max_len = self._parseQuantifier(regex[i:])
                    i += incr
                    closed = True
                    break
                raise ValueError('Invalid regex')
            elif regex[i] == '|':
                alternatives.append(Alternative(charClassesList))
                charClassesList = []
                i += 1
            else:
                incr, charClasses = self._parseCharClasses(regex[i:])
                charClassesList.append(charClasses)
                i += incr

        if not closed:
            raise ValueError('Invalid regex')

        alternatives.append(Alternative(charClassesList))
        return i, RegexTree(alternatives, min_len, max_len)

    def _parseCharClasses(self, regex: str) -> tuple[int, CharClasses]:
        i = 0
        chars_list: list[str] = []

        if regex[i] == '[':
            i += 1
            inc, chars_list = self._parseCharClass(regex[i:])
            i += inc
        elif regex[i] == '\\':
            raise NotImplementedError(
                'Escape characters are not supported yet')
        elif regex[i] == '.':
            chars_list = [chr(c) for c in range(0, 128)]
        else:
            chars_list = [regex[i]]
            i = 1

        incr, min_len, max_len = self._parseQuantifier(regex[i:])
        i += incr

        charClasses = CharClasses(chars_list, min_len, max_len)
        return i, charClasses

    def _parseCharClass(self, regex: str) -> tuple[int, list[str]]:
        i = 0
        chars_list: list[str] = []
        first_char = None
        range_divider = False
        negated = False

        if regex[i] == '^':
            negated = True
            i += 1

        while i < len(regex) and regex[i] != ']':
            if regex[i] == '\\':
                raise NotImplementedError(
                    'Escape characters are not supported yet')
            elif first_char is None:
                first_char = regex[i]
            elif regex[i] == '-':
                range_divider = True
            elif range_divider:
                chars_list.extend([chr(c) for c in range(
                    ord(first_char), ord(regex[i]) + 1)])
                first_char = None
                range_divider = False
            else:
                if first_char is not None:
                    chars_list.append(first_char)
                    first_char = None
                chars_list.append(regex[i])
            i += 1

        if regex[i] != ']':
            raise ValueError('Invalid character class')

        i += 1

        if range_divider:
            chars_list.append('-')
        if first_char is not None:
            chars_list.append(first_char)

        if negated:
            chars_list = [c for c in self.charset if c not in chars_list]

        return i, chars_list

    def _parseQuantifier(self, regex: str) -> tuple[int, int, int]:
        i = 0

        if len(regex) == 0:
            return 0, 1, 1

        match regex[i]:
            case '*':
                return 1, 0, None
            case '+':
                return 1, 1, None
            case '?':
                return 1, 0, 1
            case '{':
                i += 1
                incr, min_len, max_len = self._parseMinMax(regex[i:])
                return i + incr, min_len, max_len
            case _:
                return 0, 1, 1

    def _parseMinMax(self, regex: str) -> tuple[int, int, int]:
        i = 0
        min_len = 0
        max_len = 0

        while i < len(regex) and regex[i] == ' ':
            i += 1

        if i >= len(regex) or regex[i] not in '0123456789':
            raise ValueError('Invalid quantifier')

        while i < len(regex) and regex[i] in '0123456789':
            min_len = min_len * 10 + int(regex[i])
            i += 1

        while i < len(regex) and regex[i] == ' ':
            i += 1

        if i >= len(regex):
            raise ValueError('Invalid quantifier')
        elif regex[i] == '}':
            return i + 1, min_len, min_len
        elif regex[i] != ',':
            raise ValueError('Invalid quantifier')

        i += 1

        while i < len(regex) and regex[i] == ' ':
            i += 1

        if i >= len(regex) or regex[i] not in '0123456789}':
            raise ValueError('Invalid quantifier')

        if regex[i] == '}':
            return i + 1, min_len, None

        while i < len(regex) and regex[i] in '0123456789':
            max_len = max_len * 10 + int(regex[i])
            i += 1

        if max_len < min_len:
            raise ValueError('Invalid quantifier')

        while i < len(regex) and regex[i] == ' ':
            i += 1

        if i >= len(regex) or regex[i] != '}':
            raise ValueError('Invalid quantifier')

        i += 1

        return i, min_len, max_len
