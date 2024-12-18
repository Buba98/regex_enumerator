from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite

def test_single_character_class():
    regexEnumerator = RegexEnumerator(r'[a]')
    possibilities = ['a']

    f_finite(regexEnumerator, possibilities)

def test_character_class_with_two_literals():
    regexEnumerator = RegexEnumerator(r'[ab]')
    possibilities = ['a', 'b']

    f_finite(regexEnumerator, possibilities)

def test_character_class_with_zero_or_more_quantifier():
    regexEnumerator = RegexEnumerator(r'[a]*')
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)

def test_range_character_class():
    regexEnumerator = RegexEnumerator(r'[a-c]')
    possibilities = ['a', 'b', 'c']

    f_finite(regexEnumerator, possibilities)

def test_range_character_class_with_repetition():
    regexEnumerator = RegexEnumerator(r'[a-c]{1,2}')
    possibilities = ['a', 'b', 'c', 'aa', 'ab', 'ac', 'ba', 'bb', 'bc', 'ca', 'cb', 'cc']

    f_finite(regexEnumerator, possibilities)

def test_range_character_class_with_zero_repetition():
    regexEnumerator = RegexEnumerator(r'[a-c]{0}')
    possibilities = ['']

    f_finite(regexEnumerator, possibilities)

def test_range_character_class_with_one_or_more_quantifier():
    regexEnumerator = RegexEnumerator(r'[a-b]+')
    possibilities = ['a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa', 'aab', 'aba', 'abb', 'baa', 'bab', 'bba', 'bbb']

    f_infinite(regexEnumerator, possibilities)

def test_two_ranges_with_optional_quantifier():
    regexEnumerator = RegexEnumerator(r'[a-cf-g]?')
    possibilities = ['', 'a', 'b', 'c', 'f', 'g']

    f_finite(regexEnumerator, possibilities)

def test_literal_in_character_class():
    regexEnumerator = RegexEnumerator(r'[.]')
    possibilities = ['.']

    f_finite(regexEnumerator, possibilities)

def test_negated_character_class():
    regexEnumerator = RegexEnumerator(r'[^a]')
    possibilities = [chr(i) for i in range(32, 127) if chr(i) != 'a']

    f_finite(regexEnumerator, possibilities)

def test_character_class_with_escaped_special_char_at_start():
    regexEnumerator = RegexEnumerator(r'[\]-a]')
    possibilities = [chr(i) for i in range(93, 98)]

    f_finite(regexEnumerator, possibilities)

def test_character_class_with_escaped_special_char_at_end():
    regexEnumerator = RegexEnumerator(r'[Z-\]]')
    possibilities = [chr(i) for i in range(90, 94)]

    f_finite(regexEnumerator, possibilities)

def test_character_class_with_escape_sequence():
    regexEnumerator = RegexEnumerator(r'[\d]')
    possibilities = [str(i) for i in range(10)]

    f_finite(regexEnumerator, possibilities)

def test_incomplete_range_character_class():
    regexEnumerator = RegexEnumerator(r'[a-]')
    possibilities = ['a', '-']

    f_finite(regexEnumerator, possibilities)

def test_2_ranges():
    regexEnumerator = RegexEnumerator(r'[1a-crf-g3]')
    possibilities = ['1', 'a', 'b', 'c', 'f', 'g', 'r', '3']

    f_finite(regexEnumerator, possibilities)