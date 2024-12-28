from regex_enumerator import RegexEnumerator


def f_test(regexEnumerator: RegexEnumerator, possibilities: list[str]):
    while len(possibilities) != 0:
        res = regexEnumerator.next()
        assert res in possibilities, f"'{res}' is not in {possibilities}"
        possibilities.remove(res)


def f_finite(regex: str, possibilities: list[str], additional_charset: str = ''):
    regexEnumerator = RegexEnumerator(
        regex, additional_charset=additional_charset)
    f_test(regexEnumerator, possibilities)
    assert regexEnumerator.next() is None
    assert regexEnumerator.done

def f_infinite(regex: str, possibilities: list[str], additional_charset: str = ''):
    regexEnumerator = RegexEnumerator(
        regex, additional_charset=additional_charset)
    f_test(regexEnumerator, possibilities)
    assert not regexEnumerator.done