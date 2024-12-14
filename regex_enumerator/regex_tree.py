class RegexTree:
    pass


class CharClasses:
    def __init__(self, chars_list: list[str], min_len: int, max_len: int):
        self.index = 0
        self.chars: str = ''.join(sorted(set(''.join(chars_list))))
        self.min_len = min_len
        self.max_len = max_len
        self.done = False
        self.base = len(self.chars)

        if self.base == 0 or self.max_len == 0:
            self.done = True
            self.current: set[str] = {''}
            return

        if self.max_len is None:
            self.max_index = None
        elif self.base == 1:
            self.max_index = self.max_len - self.min_len
        else:
            self.max_index = ((self.base ** self.min_len - self.base **
                              (self.max_len + 1)) // (1 - self.base)) - 1

        self.current: set[str] = {self.calculate()}

    def calculate(self) -> str:
        if self.max_len is not None and self.index >= self.max_index:
            self.done = True

        if self.base == 1:
            return self.chars[0] * (self.min_len + self.index)

        res = []

        num = self.base ** self.min_len + self.index

        while num > 1:
            res.append(self.chars[num % self.base])
            num //= self.base

        return ''.join(reversed(res))

    def next(self) -> str:
        assert not self.done

        self.index += 1
        res = self.calculate()
        self.current.add(res)
        return res


class Alternative:
    def __init__(self, classes_or_regex_list: list[CharClasses | RegexTree]):
        self.index = 0
        self.classes_or_regex_list: list[CharClasses |
                                         RegexTree] = classes_or_regex_list

        i = 0
        while i < len(self.classes_or_regex_list):
            if self.classes_or_regex_list[i].done and len(self.classes_or_regex_list[i].current) == 0:
                self.classes_or_regex_list.pop(i)
            else:
                i += 1

        self.base = len(self.classes_or_regex_list)

        if self.base == 0:
            self.done = True
            self.current: set[str] = {''}
            return

        self.done = False
        self.current: set[str] = self.calculate()

    def next(self) -> set[str]:
        assert not self.done

        res = set()
        self.index += 1
        for i in range(self.index, self.index + self.base):
            if self.classes_or_regex_list[i % self.base].done:
                self.index += 1
            else:
                break

        if 0 == self.index % self.base:
            if isinstance(self.classes_or_regex_list[0], CharClasses):
                res.add(self.classes_or_regex_list[0].next())
            else:
                res.update(self.classes_or_regex_list[0].next())
        else:
            res.update(self.classes_or_regex_list[0].current)

        done = self.classes_or_regex_list[0].done

        for i, classes_or_regex in enumerate(self.classes_or_regex_list[1:], start=1):
            temp = set()

            if i == self.index % self.base:
                next_str = classes_or_regex.next()
                if isinstance(next_str, str):
                    for prv_str in res:
                        temp.add(prv_str + next_str)
                else:
                    for prv_str in res:
                        for string in next_str:
                            temp.add(prv_str + string)
            else:
                for prv_str in res:
                    for string in classes_or_regex.current:
                        temp.add(prv_str + string)

            done = done and classes_or_regex.done
            res = temp

        self.done = done

        new_res = res - self.current
        self.current.update(new_res)
        return new_res

    def calculate(self) -> set[str]:
        res = set()
        res.update(self.classes_or_regex_list[0].current)

        done = self.classes_or_regex_list[0].done

        for classes_or_regex in self.classes_or_regex_list[1:]:
            temp = set()
            done = done and classes_or_regex.done
            for prv_str in res:
                for string in classes_or_regex.current:
                    temp.add(prv_str + string)

            res = temp

        self.done = done
        return res


class RegexTree:
    def __init__(self, alternatives: list[Alternative], min_len: int, max_len: int):
        self.alternatives: list[Alternative] = alternatives
        self.min_len = min_len
        self.max_len = max_len

        i = 0
        while i < len(self.alternatives):
            if self.alternatives[i].done and len(self.alternatives[i].current) == 0:
                self.alternatives.pop(i)
            else:
                i += 1

        self.base = len(self.alternatives)

        if self.base == 0 or self.max_len == 0:
            self.done = True
            self.current: set[str] = set()
            return

        self.done = False
        self.gen_charset = False
        self.index_charset = 0
        self.index_repetition = 0
        self.done_repetition = False
        self.current_charset: set[str] = self.calculate_charset()
        self.current: set[str] = self.calculate()

    def next(self) -> set[str]:
        assert not self.done

        if self.done_charset:
            self.gen_charset = False
        elif self.done_repetition:
            self.gen_charset = True

        if self.gen_charset:
            next_charset: set[str] = self.next_charset()
            # optimize it by using only the new charset
        else:
            if not self.done_repetition:
                self.index_repetition += 1

        res: set[str] = self.calculate()

        self.gen_charset = not self.gen_charset
        new_res = res - self.current
        self.current.update(new_res)
        return new_res

    def calculate(self) -> set[str]:
        if self.max_len is not None and self.index_repetition + self.min_len >= self.max_len:
            self.done_repetition = True
            if self.done_charset:
                self.done = True

        if self.index_repetition + self.min_len == 0:
            return {''}

        res = set(self.current_charset)

        for i in range(1, self.min_len + self.index_repetition):
            temp = set()
            for prv_str in res:
                for string in self.current_charset:
                    temp.add(prv_str + string)
            res = temp

        return res

    def next_charset(self) -> set[str]:
        assert not self.done_charset

        self.index_charset += 1

        for i in range(self.index_charset, self.index_charset + self.base):
            if self.alternatives[i % self.base].done:
                self.index_charset += 1
            else:
                break

        res = self.alternatives[self.index_charset % self.base].next()

        done_charset = True

        for alternative in self.alternatives:
            if not alternative.done:
                done_charset = False
                break

        new_res = res - self.current_charset
        self.current_charset.update(new_res)
        self.done_charset = done_charset
        return new_res

    def calculate_charset(self) -> set[str]:
        res = set()

        done_charset = True

        for alternative in self.alternatives:
            res.update(alternative.current)
            done_charset = done_charset and alternative.done

        self.done_charset = done_charset

        return res
