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
