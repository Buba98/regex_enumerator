from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite


def test_empty_pattern_yields_empty_string():
    regexEnumerator = RegexEnumerator(r'')
    possibilities = ['']
    f_finite(regexEnumerator, possibilities)


def test_single_literal_character():
    regexEnumerator = RegexEnumerator(r'a')
    possibilities = ['a']
    f_finite(regexEnumerator, possibilities)


def test_zero_or_more_quantifier_on_single_char():
    regexEnumerator = RegexEnumerator(r'a*')
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']
    f_infinite(regexEnumerator, possibilities)


def test_one_or_more_quantifier_on_single_char():
    regexEnumerator = RegexEnumerator(r'a+')
    possibilities = ['a', 'aa', 'aaa', 'aaaa', 'aaaaa']
    f_infinite(regexEnumerator, possibilities)


def test_zero_or_one_quantifier_on_single_char():
    regexEnumerator = RegexEnumerator(r'a?')
    possibilities = ['', 'a']
    f_finite(regexEnumerator, possibilities)


def test_exact_repetition_quantifier_on_single_char():
    regexEnumerator = RegexEnumerator(r'a{2}')
    possibilities = ['aa']
    f_finite(regexEnumerator, possibilities)


def test_minimum_repetition_quantifier_on_single_char():
    regexEnumerator = RegexEnumerator(r'a{2,}')
    possibilities = ['aa', 'aaa', 'aaaa', 'aaaaa']
    f_infinite(regexEnumerator, possibilities)


def test_min_max_repetition_quantifier_on_single_char():
    # `a{2,4}` yields 'aa', 'aaa', 'aaaa'.
    regexEnumerator = RegexEnumerator(r'a{2,4}')
    possibilities = ['aa', 'aaa', 'aaaa']
    f_finite(regexEnumerator, possibilities)


def test_zero_times_repetition_quantifier_on_single_char():
    regexEnumerator = RegexEnumerator(r'a{0}')
    possibilities = ['']
    f_finite(regexEnumerator, possibilities)


def test_escaped_literal_special_characters():
    regexEnumerator = RegexEnumerator(r'\*\+\?')
    possibilities = ['*+?']
    f_finite(regexEnumerator, possibilities)


def test_single_character_class():
    regexEnumerator = RegexEnumerator(r'[abc]')
    possibilities = ['a', 'b', 'c']
    f_finite(regexEnumerator, possibilities)


def test_single_escaped_character():
    regexEnumerator = RegexEnumerator(r'\n')
    possibilities = ['\n']
    f_finite(regexEnumerator, possibilities)


def test_literal_dot_character():
    regexEnumerator = RegexEnumerator(r'\.')
    possibilities = ['.']
    f_finite(regexEnumerator, possibilities)
