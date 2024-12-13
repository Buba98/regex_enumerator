from regex_enumerator import RegexEnumerator


def f_finite(regexEnumerator: RegexEnumerator, possibilities: list[str]):
    while len(possibilities) != 0:
        res = regexEnumerator.next()
        assert res in possibilities
        possibilities.remove(res)
        
    assert regexEnumerator.done

def f_infinite(regexEnumerator: RegexEnumerator, possibilities: list[str]):
    while len(possibilities) != 0:
        res = regexEnumerator.next()
        assert res in possibilities
        possibilities.remove(res)
    
    assert not regexEnumerator.done