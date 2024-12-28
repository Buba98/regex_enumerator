class RegexTree:
    pass


class CharClass:
    def __init__(self, chars_list: list[str], min_len: int, max_len: int | None):
        self._index = 0
        self._chars: str = ''.join(sorted(set(''.join(chars_list))))
        self._min_len = min_len
        self._max_len = max_len
        self._base = len(self._chars)
        self.done = self._base == 0 or self._max_len == 0
        self.current: list[str] = self._first()

    def _first(self) -> list[str]:
        if self.done:
            return []

        if self._base == 1 and self._max_len is not None:
            self.done = True
            result = [self._chars *
                      i for i in range(self._min_len, self._max_len + 1)]
            return result

        if self._max_len is not None and self._max_len == self._min_len:
            self.done = True

        if self._min_len == 0:
            self._last = ['']
            return ['']

        result = ['']
        for _ in range(self._min_len):
            result = [pfx + sfx for pfx in self._chars for sfx in result]

        self._last = result
        return result

    def next(self) -> list[str]:
        assert not self.done

        self._index += 1
        if self._max_len is not None and self._index + self._min_len == self._max_len:
            self.done = True

        result = [pfx + sfx for pfx in self._last for sfx in self._chars]
        self.current.extend(result)
        self._last = result
        return result


class BackReference:
    def __init__(self, reference: RegexTree, min_len: int, max_len: int | None):
        self._min_len = min_len
        self._max_len = max_len
        self._index = 0
        self.reference: RegexTree = reference
        self.done = max_len == 0 or (
            reference.done and len(reference.current) == 0)
        self.current = self._first()

    def update_reference(self, new_strings: set[str]) -> None:
        assert all(string not in self.current for string in new_strings)

        for string in new_strings:
            self.current[string] = [
                string * i for i in range(self._min_len, self._min_len + self._index + 1)]

    def _first(self) -> dict[str, list[str]]:
        if self.done:
            return {}

        if self._max_len is not None:
            self.index = self._max_len - self._min_len
            self.done = True
            result: dict[str, list[str]] = {}
            for string in self.reference.current:
                result[string] = [
                    string * i for i in range(self._min_len, self._max_len + 1)]
            return result

        result: dict[str, list[str]] = {}
        for string in self.reference.current:
            result[string] = [string * self._min_len]
        return result

    def next(self) -> dict[str, list[str]]:
        assert not self.done

        self._index += 1
        for key, values in self.current.items():
            values.append(values[-1] + key)

        return self.current


class Alternative:
    def __init__(self, elements: list[CharClass | RegexTree | BackReference]):
        self._index = 0
        self._elements = [e for e in elements if not e.done or len(e.current)]
        self._base = len(self._elements)
        self.done = self._base == 0
        self.current = self._first()

    def next(self) -> set[str]:
        assert not self.done
        assert not isinstance(self._elements[0], BackReference)

        index = self._index + 1
        if index >= self._base:
            index = 0
        while self._elements[index].done:
            index += 1
            if index >= self._base:
                index = 0

        self._index = index
        result: list[tuple[str, dict[RegexTree, str]]] = []

        if isinstance(self._elements[0], CharClass):
            for string in self._elements[0].next() if index == 0 else self._elements[0].current:
                result.append((string, {}))
        else:
            for string in self._elements[0].next() if index == 0 else self._elements[0].current:
                result.append((string, {self._elements[0]: string}))

        done = self._elements[0].done

        for i, element in enumerate(self._elements[1:], start=1):
            temp = []
            if isinstance(element, CharClass):
                for sfx in element.next() if i == index else element.current:
                    for pfx in result:
                        temp.append((pfx[0] + sfx, pfx[1]))
            elif isinstance(element, RegexTree):
                for sfx in element.next() if i == index else element.current:
                    for pfx in result:
                        temp.append((pfx[0] + sfx, {**pfx[1], element: sfx}))
            else:
                if i == index:
                    element.next()
                for pfx in result:
                    reference = pfx[1][element.reference]
                    assert reference is not None
                    for sfx in element.current[reference]:
                        temp.append(
                            (pfx[0] + sfx, pfx[1]))
            result = temp
            done = done and element.done

        self.done = done
        new_strings = {struct[0] for struct in result} - self.current
        self.current.update(new_strings)
        return new_strings

    def _first(self) -> set[str]:
        if self.done:
            return {''}

        assert not isinstance(self._elements[0], BackReference)

        result: list[tuple[str, dict[RegexTree, str]]] = []

        if isinstance(self._elements[0], CharClass):
            for char in self._elements[0].current:
                result.append((char, {}))
        else:
            for char in self._elements[0].current:
                result.append((char, {self._elements[0]: char}))

        done = self._elements[0].done

        for element in self._elements[1:]:
            temp: list[tuple[str, dict[RegexTree, str]]] = []
            done = done and element.done
            if isinstance(element, CharClass):
                for pfx in result:
                    for sfx in element.current:
                        temp.append((pfx[0] + sfx, pfx[1]))
            elif isinstance(element, RegexTree):
                for pfx in result:
                    for sfx in element.current:
                        temp.append((pfx[0] + sfx, {**pfx[1], element: sfx}))
            else:
                for pfx in result:
                    reference = pfx[1][element.reference]
                    assert reference is not None
                    for sfx in element.current[reference]:
                        temp.append(
                            (pfx[0] + sfx, pfx[1]))
            result = temp

        self.done = done
        return {struct[0] for struct in result}


class RegexTree:
    def __init__(self, alternatives: list[Alternative], min_len: int, max_len: int | None):
        self.references: list[BackReference] = []
        self._alternatives: list[Alternative] = alternatives
        self._min_len = min_len
        self._max_len = max_len
        self._base = len(self._alternatives)
        self.done = self._max_len == 0
        self._gen_charset = False
        self._index_charset = 0
        self._index_repetition = 0
        self._done_repetition = False
        self._current_chars: set[str] = self._first_charset()
        self.current: set[str] = self._first_repetition()

    def _first_repetition(self) -> set[str]:
        if self.done:
            return {''}

        if self._min_len == self._max_len:
            self._done_repetition = True
            if self._done_charset:
                self.done = True

        result = {''}
        for _ in range(self._min_len):
            result = {pfx + sfx for pfx in result for sfx in self._current_chars}

        if self._max_len is not None and self._base == 1:
            self._index_repetition = self._max_len - self._min_len
            self._done_repetition = True
            if self._done_charset:
                self.done = True
            for _ in range(self._index_repetition):
                result.update(
                    {pfx + sfx for pfx in result for sfx in self._current_chars})

        return result

    def add_reference(self, reference: BackReference) -> None:
        if reference.done and len(reference.current) == 0:
            return
        self.references.append(reference)

    def _next_charset(self) -> set[str]:
        index_charset = self._index_charset + 1

        if index_charset >= self._base:
            index_charset = 0
        while self._alternatives[index_charset].done:
            index_charset += 1
            if index_charset >= self._base:
                index_charset = 0

        self._index_charset = index_charset
        new_chars = self._alternatives[index_charset].next()
        self._done_charset = all(alt.done for alt in self._alternatives)
        self._current_chars.update(new_chars)

        if self._done_repetition and self._done_charset:
            self.done = True

        result = set()
        for i in range(self._min_len + self._index_repetition):
            temp = set(self._current_chars)
            for _ in range(i):
                temp.update(
                    {pfx + sfx for pfx in temp for sfx in self._current_chars})
            result.update(temp)

        return result

    def next(self) -> set[str]:
        assert not self.done

        if self._done_charset:
            self._gen_charset = False
        elif self._done_repetition:
            self._gen_charset = True

        if self._gen_charset:
            result = self._next_charset()
        else:
            result = self._next_repetition()

        self._gen_charset = not self._gen_charset
        result -= self.current
        if len(result) == 0:
            return result

        self.current.update(result)
        if len(self.references) == 0:
            return result

        for reference in self.references:
            reference.update_reference(result)
        return result

    def _next_repetition(self) -> set[str]:
        self._index_repetition += 1

        if self._max_len is not None and self._index_repetition + self._min_len >= self._max_len:
            self._done_repetition = True
            if self._done_charset:
                self.done = True

        result = set(self._current_chars)
        for _ in range(1, self._min_len + self._index_repetition):
            result = {pfx + sfx for pfx in result for sfx in self._current_chars}

        return result

    def _first_charset(self) -> set[str]:
        result = set()
        done_charset = True

        for alternative in self._alternatives:
            result.update(alternative.current)
            done_charset = done_charset and alternative.done

        self._done_charset = done_charset
        return result
