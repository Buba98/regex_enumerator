from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite


def test_backreference(benchmark):
    regexEnumerator = RegexEnumerator(r'(a)\1')
    possibilities = ['aa']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_backreference_with_group_quantifier(benchmark):
    regexEnumerator = RegexEnumerator(r'(a)+\1')
    possibilities = ['aa' * i for i in range(1, 6)]

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_backreference_with_quantifier(benchmark):
    regexEnumerator = RegexEnumerator(r'(a)\1+')
    possibilities = ['a' * i + 'a' for i in range(1, 6)]

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_backreference_with_named_group(benchmark):
    regexEnumerator = RegexEnumerator(r'(?<name>[a-b])\k<name>')
    possibilities = ['aa', 'bb']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_backreference_with_named_group_and_quantifier(benchmark):
    regexEnumerator = RegexEnumerator(r'(?<name>[a-b])\k<name>{1, 2}')
    possibilities = ['aa', 'bb', 'aaa', 'bbb']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_zero_width_backreference(benchmark):
    regexEnumerator = RegexEnumerator(r'(a)?\1{0}')
    possibilities = ['a', '']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_10_backreference(benchmark):
    regexEnumerator = RegexEnumerator(r'(a)(b)(c)(d)(e)(f)(g)(h)(i)(j)\10')
    possibilities = ['abcdefghijj']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_multiple_backreferences(benchmark):
    regexEnumerator = RegexEnumerator(r'(a)(b)\2\1')
    possibilities = ['abba']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_backreference_with_mismatch(benchmark):
    regexEnumerator = RegexEnumerator(r'(a)(b)\1')
    possibilities = ['aba']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_named_group_with_backreference(benchmark):
    regexEnumerator = RegexEnumerator(r'(?<letter>[ab])\k<letter>')
    possibilities = [
        'aa', 'bb'
    ]

    benchmark(f_finite, regexEnumerator, possibilities)


def test_named_group_infinite_repetition_with_backreference(benchmark):
    regexEnumerator = RegexEnumerator(r'(?<letter>[ab])+\k<letter>')
    possibilities = [
        'aa', 'bb', 'abab', 'baba', 'aaaa', 'bbbb'
    ]

    benchmark(f_infinite, regexEnumerator, possibilities)