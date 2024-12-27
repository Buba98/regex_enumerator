from .test_function import f_finite, f_infinite


def test_empty_pattern_yields_empty_string():
    regex = r''
    possibilities = ['']
    f_finite(regex, possibilities)


def test_single_literal_character():
    regex = r'a'
    possibilities = ['a']
    f_finite(regex, possibilities)


def test_zero_or_more_quantifier_on_single_char():
    regex = r'a*'
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']
    f_infinite(regex, possibilities)


def test_one_or_more_quantifier_on_single_char():
    regex = r'a+'
    possibilities = ['a', 'aa', 'aaa', 'aaaa', 'aaaaa']
    f_infinite(regex, possibilities)


def test_zero_or_one_quantifier_on_single_char():
    regex = r'a?'
    possibilities = ['', 'a']
    f_finite(regex, possibilities)


def test_exact_repetition_quantifier_on_single_char():
    regex = r'a{2}'
    possibilities = ['aa']
    f_finite(regex, possibilities)


def test_minimum_repetition_quantifier_on_single_char():
    regex = r'a{2,}'
    possibilities = ['aa', 'aaa', 'aaaa', 'aaaaa']
    f_infinite(regex, possibilities)


def test_min_max_repetition_quantifier_on_single_char():
    # `a{2,4}` yields 'aa', 'aaa', 'aaaa'.
    regex = r'a{2,4}'
    possibilities = ['aa', 'aaa', 'aaaa']
    f_finite(regex, possibilities)


def test_zero_times_repetition_quantifier_on_single_char():
    regex = r'a{0}'
    possibilities = ['']
    f_finite(regex, possibilities)


def test_escaped_literal_special_characters():
    regex = r'\*\+\?'
    possibilities = ['*+?']
    f_finite(regex, possibilities)


def test_single_character_class():
    regex = r'[abc]'
    possibilities = ['a', 'b', 'c']
    f_finite(regex, possibilities)


def test_single_escaped_character():
    regex = r'\n'
    possibilities = ['\n']
    f_finite(regex, possibilities)


def test_literal_dot_character():
    regex = r'\.'
    possibilities = ['.']
    f_finite(regex, possibilities)
