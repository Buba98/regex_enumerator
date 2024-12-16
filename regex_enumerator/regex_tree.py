class RegexTree:
    pass


class CharClasses:
    def __init__(self, chars_list: list[str], min_len: int, max_len: int):
        self._index = 0
        self._chars: str = ''.join(sorted(set(''.join(chars_list))))
        self._min_len = min_len
        self._max_len = max_len
        self._base = len(self._chars)
        self.done = self._base == 0 or self._max_len == 0
        self._max_index = self._calculate_max_index()
        self.current: set[str] = {self._calculate()} if not self.done else {''}

    def _calculate_max_index(self) -> int | None:
        if self._max_len is None or self.done:
            return None
        if self._base == 1:
            return self._max_len - self._min_len
        return ((self._base ** self._min_len - self._base ** (self._max_len + 1)) // (1 - self._base)) - 1

    def _calculate(self) -> str:
        if self._max_len is not None and self._index >= self._max_index:
            self.done = True

        if self._base == 1:
            return self._chars[0] * (self._min_len + self._index)

        res = []
        num = self._base ** self._min_len + self._index
        while num > 1:
            res.append(self._chars[num % self._base])
            num //= self._base

        return ''.join(reversed(res))

    def next(self) -> set[str]:
        assert not self.done

        self._index += 1
        res = self._calculate()
        self.current.add(res)
        return {res}


class Alternative:
    def __init__(self, elements: list[CharClasses | RegexTree]):
        self._index = 0
        self._elements: list[CharClasses | RegexTree] = [
            element for element in elements if not element.done or len(element.current) > 0]
        self._base = len(self._elements)
        self.done = self._base == 0
        self.current: set[str] = self._calculate() if not self.done else {''}

    def next(self) -> set[str]:
        assert not self.done

        self._index += 1
        for i in range(self._index, self._index + self._base):
            if self._elements[i % self._base].done:
                self._index += 1
            else:
                break

        result = set(
            self._elements[0].current) if self._index % self._base else self._elements[0].next()
        done = self._elements[0].done

        for i, element in enumerate(self._elements[1:], start=1):
            suffixes = element.next() if i == self._index % self._base else element.current
            result = {prefix + suffix for prefix in result for suffix in suffixes}
            done = done and element.done

        self.done = done
        new_res = result - self.current
        self.current.update(new_res)
        return new_res

    def _calculate(self) -> set[str]:
        result = set(self._elements[0].current)
        done = self._elements[0].done

        for element in self._elements[1:]:
            done = done and element.done
            result = {
                prefix + suffix for prefix in result for suffix in element.current}

        self.done = done
        return result


class RegexTree:
    def __init__(self, alternatives: list[Alternative], min_len: int, max_len: int, name: str | None):
        self.name = name
        self._alternatives: list[Alternative] = [
            alternative for alternative in alternatives if not alternative.done or len(alternative.current) > 0]
        self._min_len = min_len
        self._max_len = max_len
        self._base = len(self._alternatives)
        self.done = self._base == 0 or self._max_len == 0
        self._gen_charset = False
        self._index_charset = 0
        self._index_repetition = 0
        self._done_repetition = False
        self._current_charset: set[str] = self._calculate_charset()
        self.current: set[str] = self._calculate() if not self.done else set()

    def next(self) -> set[str]:
        assert not self.done

        if self._done_charset:
            self._gen_charset = False
        elif self._done_repetition:
            self._gen_charset = True

        if self._gen_charset:
            next_charset: set[str] = self._next_charset()
            # optimize it by using only the new charset
        else:
            if not self._done_repetition:
                self._index_repetition += 1

        res: set[str] = self._calculate()
        self._gen_charset = not self._gen_charset
        new_res = res - self.current
        self.current.update(new_res)
        return new_res

    def _calculate(self) -> set[str]:
        if self._max_len is not None and self._index_repetition + self._min_len >= self._max_len:
            self._done_repetition = True
            if self._done_charset:
                self.done = True

        if self._index_repetition + self._min_len == 0:
            return {''}

        result = set(self._current_charset)
        for _ in range(1, self._min_len + self._index_repetition):
            result = {
                prefix + suffix for prefix in result for suffix in self._current_charset}

        return result

    def _next_charset(self) -> set[str]:
        assert not self._done_charset

        self._index_charset += 1

        for i in range(self._index_charset, self._index_charset + self._base):
            if self._alternatives[i % self._base].done:
                self._index_charset += 1
            else:
                break

        res = self._alternatives[self._index_charset % self._base].next()
        done_charset = True

        for alternative in self._alternatives:
            if not alternative.done:
                done_charset = False
                break

        new_res = res - self._current_charset
        self._current_charset.update(new_res)
        self._done_charset = done_charset
        return new_res

    def _calculate_charset(self) -> set[str]:
        res = set()
        done_charset = True

        for alternative in self._alternatives:
            res.update(alternative.current)
            done_charset = done_charset and alternative.done

        self._done_charset = done_charset
        return res
