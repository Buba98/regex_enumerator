from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite


def test_empty_regex():
    regexEnumerator = RegexEnumerator(r'')
    possibilities = ['']

    f_finite(regexEnumerator, possibilities)


def test_single_literal_char():
    regexEnumerator = RegexEnumerator(r'a')
    possibilities = ['a']

    f_finite(regexEnumerator, possibilities)


def test_zero_or_more_quantifier():
    regexEnumerator = RegexEnumerator(r'a*')
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)


def test_one_or_more_quantifier():
    regexEnumerator = RegexEnumerator(r'a+')
    possibilities = ['a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)


def test_zero_or_one_quantifier():
    regexEnumerator = RegexEnumerator(r'a?')
    possibilities = ['', 'a']

    f_finite(regexEnumerator, possibilities)


def test_exact_repetition_quantifier():
    regexEnumerator = RegexEnumerator(r'a{2}')
    possibilities = ['aa']

    f_finite(regexEnumerator, possibilities)


def test_min_repetition_quantifier():
    regexEnumerator = RegexEnumerator(r'a{2,}')
    possibilities = ['aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)


def test_min_max_repetition_quantifier():
    regexEnumerator = RegexEnumerator(r'a{2,4}')
    possibilities = ['aa', 'aaa', 'aaaa']

    f_finite(regexEnumerator, possibilities)


def test_zero_repetition_quantifier():
    regexEnumerator = RegexEnumerator(r'a{0}')
    possibilities = ['']

    f_finite(regexEnumerator, possibilities)


def test_literal_special_characters():
    regexEnumerator = RegexEnumerator(r'\*\+\?')
    possibilities = ['*+?']

    f_finite(regexEnumerator, possibilities)
