from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite


def test_single_character_class(benchmark):
    regexEnumerator = RegexEnumerator(r'[a]')
    possibilities = ['a']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_character_class_with_two_literals(benchmark):
    regexEnumerator = RegexEnumerator(r'[ab]')
    possibilities = ['a', 'b']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_character_class_with_zero_or_more_quantifier(benchmark):
    regexEnumerator = RegexEnumerator(r'[a]*')
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_range_character_class(benchmark):
    regexEnumerator = RegexEnumerator(r'[a-c]')
    possibilities = ['a', 'b', 'c']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_range_character_class_with_repetition(benchmark):
    regexEnumerator = RegexEnumerator(r'[a-c]{1,2}')
    possibilities = ['a', 'b', 'c', 'aa', 'ab',
                     'ac', 'ba', 'bb', 'bc', 'ca', 'cb', 'cc']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_range_character_class_with_zero_repetition(benchmark):
    regexEnumerator = RegexEnumerator(r'[a-c]{0}')
    possibilities = ['']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_range_character_class_with_one_or_more_quantifier(benchmark):
    regexEnumerator = RegexEnumerator(r'[a-b]+')
    possibilities = ['a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa',
                     'aab', 'aba', 'abb', 'baa', 'bab', 'bba', 'bbb']

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_two_ranges_with_optional_quantifier(benchmark):
    regexEnumerator = RegexEnumerator(r'[a-cf-g]?')
    possibilities = ['', 'a', 'b', 'c', 'f', 'g']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_literal_in_character_class(benchmark):
    regexEnumerator = RegexEnumerator(r'[.]')
    possibilities = ['.']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_negated_character_class(benchmark):
    regexEnumerator = RegexEnumerator(r'[^a]')
    possibilities = [chr(i) for i in range(32, 127) if chr(i) != 'a']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_character_class_with_escaped_special_char_at_start(benchmark):
    regexEnumerator = RegexEnumerator(r'[\]-a]')
    possibilities = [chr(i) for i in range(93, 98)]

    benchmark(f_finite, regexEnumerator, possibilities)


def test_character_class_with_escaped_special_char_at_end(benchmark):
    regexEnumerator = RegexEnumerator(r'[Z-\]]')
    possibilities = [chr(i) for i in range(90, 94)]

    benchmark(f_finite, regexEnumerator, possibilities)


def test_character_class_with_escape_sequence(benchmark):
    regexEnumerator = RegexEnumerator(r'[\d]')
    possibilities = [str(i) for i in range(10)]

    benchmark(f_finite, regexEnumerator, possibilities)


def test_incomplete_range_character_class(benchmark):
    regexEnumerator = RegexEnumerator(r'[a-]')
    possibilities = ['a', '-']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_2_ranges(benchmark):
    regexEnumerator = RegexEnumerator(r'[1a-crf-g3]')
    possibilities = ['1', 'a', 'b', 'c', 'f', 'g', 'r', '3']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_unicode_character_class(benchmark):
    regexEnumerator = RegexEnumerator(r'[à-å]')
    possibilities = ['à', 'á', 'â', 'ã', 'ä', 'å']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_additional_charset(benchmark):
    regexEnumerator = RegexEnumerator(
        r'[^\w\d\s]', additional_charset=['γ', 'β', 'α'])
    possibilities = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':',
                     ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~', 'α', 'β', 'γ']

    benchmark(f_finite, regexEnumerator, possibilities)

def test_charclass_with_quantifier_from_0(benchmark):
    regexEnumerator = RegexEnumerator(r'[b-d]{0,2}')
    possibilities = ['', 'b', 'c', 'd', 'bb', 'bc', 'bd', 'cb', 'cc', 'cd', 'db', 'dc', 'dd']

    f_finite(regexEnumerator, set(possibilities))
