from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite


def test_empty_pattern_yields_empty_string(benchmark):
    regexEnumerator = RegexEnumerator(r'')
    possibilities = ['']
    benchmark(f_finite, regexEnumerator, possibilities)


def test_single_literal_character(benchmark):
    regexEnumerator = RegexEnumerator(r'a')
    possibilities = ['a']
    benchmark(f_finite, regexEnumerator, possibilities)


def test_zero_or_more_quantifier_on_single_char(benchmark):
    regexEnumerator = RegexEnumerator(r'a*')
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']
    benchmark(f_infinite, regexEnumerator, possibilities)


def test_one_or_more_quantifier_on_single_char(benchmark):
    regexEnumerator = RegexEnumerator(r'a+')
    possibilities = ['a', 'aa', 'aaa', 'aaaa', 'aaaaa']
    benchmark(f_infinite, regexEnumerator, possibilities)


def test_zero_or_one_quantifier_on_single_char(benchmark):
    regexEnumerator = RegexEnumerator(r'a?')
    possibilities = ['', 'a']
    benchmark(f_finite, regexEnumerator, possibilities)


def test_exact_repetition_quantifier_on_single_char(benchmark):
    regexEnumerator = RegexEnumerator(r'a{2}')
    possibilities = ['aa']
    benchmark(f_finite, regexEnumerator, possibilities)


def test_minimum_repetition_quantifier_on_single_char(benchmark):
    regexEnumerator = RegexEnumerator(r'a{2,}')
    possibilities = ['aa', 'aaa', 'aaaa', 'aaaaa']
    benchmark(f_infinite, regexEnumerator, possibilities)


def test_min_max_repetition_quantifier_on_single_char(benchmark):
    # `a{2,4}` yields 'aa', 'aaa', 'aaaa'.
    regexEnumerator = RegexEnumerator(r'a{2,4}')
    possibilities = ['aa', 'aaa', 'aaaa']
    benchmark(f_finite, regexEnumerator, possibilities)


def test_zero_times_repetition_quantifier_on_single_char(benchmark):
    regexEnumerator = RegexEnumerator(r'a{0}')
    possibilities = ['']
    benchmark(f_finite, regexEnumerator, possibilities)


def test_escaped_literal_special_characters(benchmark):
    regexEnumerator = RegexEnumerator(r'\*\+\?')
    possibilities = ['*+?']
    benchmark(f_finite, regexEnumerator, possibilities)


def test_single_character_class(benchmark):
    regexEnumerator = RegexEnumerator(r'[abc]')
    possibilities = ['a', 'b', 'c']
    benchmark(f_finite, regexEnumerator, possibilities)


def test_single_escaped_character(benchmark):
    regexEnumerator = RegexEnumerator(r'\n')
    possibilities = ['\n']
    benchmark(f_finite, regexEnumerator, possibilities)


def test_literal_dot_character(benchmark):
    regexEnumerator = RegexEnumerator(r'\.')
    possibilities = ['.']
    benchmark(f_finite, regexEnumerator, possibilities)
