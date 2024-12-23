from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite


def test_backreference():
    regexEnumerator = RegexEnumerator(r'(a)\1')
    possibilities = ['aa']

    f_finite(regexEnumerator, possibilities)


def test_backreference_with_group_quantifier():
    regexEnumerator = RegexEnumerator(r'(a)+\1')
    possibilities = ['aa' * i for i in range(1, 6)]

    f_infinite(regexEnumerator, possibilities)


def test_backreference_with_quantifier():
    regexEnumerator = RegexEnumerator(r'(a)\1+')
    possibilities = ['a' * i + 'a' for i in range(1, 6)]

    f_infinite(regexEnumerator, possibilities)


def test_backreference_with_named_group():
    regexEnumerator = RegexEnumerator(r'(?<name>[a-b])\k<name>')
    possibilities = ['aa', 'bb']

    f_finite(regexEnumerator, possibilities)


def test_backreference_with_named_group_and_quantifier():
    regexEnumerator = RegexEnumerator(r'(?<name>[a-b])\k<name>{1, 2}')
    possibilities = ['aa', 'bb', 'aaa', 'bbb']

    f_finite(regexEnumerator, possibilities)


def test_zero_width_backreference():
    regexEnumerator = RegexEnumerator(r'(a)?\1{0}')
    possibilities = ['a', '']

    f_finite(regexEnumerator, possibilities)


def test_10_backreference():
    regexEnumerator = RegexEnumerator(r'(a)(b)(c)(d)(e)(f)(g)(h)(i)(j)\10')
    possibilities = ['abcdefghijj']

    f_finite(regexEnumerator, possibilities)


def test_multiple_backreferences():
    regexEnumerator = RegexEnumerator(r'(a)(b)\2\1')
    possibilities = ['abba']

    f_finite(regexEnumerator, possibilities)


def test_backreference_with_mismatch():
    regexEnumerator = RegexEnumerator(r'(a)(b)\1')
    possibilities = ['aba']

    f_finite(regexEnumerator, possibilities)


def test_named_group_with_backreference():
    regexEnumerator = RegexEnumerator(r'(?<letter>[ab])\k<letter>')
    possibilities = [
        'aa', 'bb'
    ]

    f_finite(regexEnumerator, possibilities)


def test_named_group_infinite_repetition_with_backreference():
    regexEnumerator = RegexEnumerator(r'(?<letter>[ab])+\k<letter>')
    possibilities = [
        'aa', 'bb', 'abab', 'baba', 'aaaa', 'bbbb'
    ]

    f_infinite(regexEnumerator, possibilities)