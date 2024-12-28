from .test_function import f_finite, f_infinite


def test_single_character_class():
    regex = r'[a]'
    possibilities = ['a']

    f_finite(regex, possibilities)


def test_character_class_with_two_literals():
    regex = r'[ab]'
    possibilities = ['a', 'b']

    f_finite(regex, possibilities)


def test_character_class_with_zero_or_more_quantifier():
    regex = r'[a]*'
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regex, possibilities)


def test_range_character_class():
    regex = r'[a-c]'
    possibilities = ['a', 'b', 'c']

    f_finite(regex, possibilities)


def test_range_character_class_with_repetition():
    regex = r'[a-c]{1,2}'
    possibilities = ['a', 'b', 'c', 'aa', 'ab',
                     'ac', 'ba', 'bb', 'bc', 'ca', 'cb', 'cc']

    f_finite(regex, possibilities)


def test_range_character_class_with_zero_repetition():
    regex = r'[a-c]{0}'
    possibilities = ['']

    f_finite(regex, possibilities)

def test_empty_character_class():
    regex = r'[]'
    possibilities = ['']

    f_finite(regex, possibilities)

def test_range_character_class_with_one_or_more_quantifier():
    regex = r'[a-b]+'
    possibilities = ['a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa',
                     'aab', 'aba', 'abb', 'baa', 'bab', 'bba', 'bbb']

    f_infinite(regex, possibilities)


def test_two_ranges_with_optional_quantifier():
    regex = r'[a-cf-g]?'
    possibilities = ['', 'a', 'b', 'c', 'f', 'g']

    f_finite(regex, possibilities)


def test_literal_in_character_class():
    regex = r'[.]'
    possibilities = ['.']

    f_finite(regex, possibilities)


def test_negated_character_class():
    regex = r'[^a]'
    possibilities = [chr(i) for i in range(32, 127) if chr(i) != 'a']

    f_finite(regex, possibilities)


def test_character_class_with_escaped_special_char_at_start():
    regex = r'[\]-a]'
    possibilities = [chr(i) for i in range(93, 98)]

    f_finite(regex, possibilities)


def test_character_class_with_escaped_special_char_at_end():
    regex = r'[Z-\]]'
    possibilities = [chr(i) for i in range(90, 94)]

    f_finite(regex, possibilities)


def test_character_class_with_escape_sequence():
    regex = r'[\d]'
    possibilities = [str(i) for i in range(10)]

    f_finite(regex, possibilities)


def test_incomplete_range_character_class():
    regex = r'[a-]'
    possibilities = ['a', '-']

    f_finite(regex, possibilities)


def test_2_ranges():
    regex = r'[1a-crf-g3]'
    possibilities = ['1', 'a', 'b', 'c', 'f', 'g', 'r', '3']

    f_finite(regex, possibilities)


def test_unicode_character_class():
    regex = r'[à-å]'
    possibilities = ['à', 'á', 'â', 'ã', 'ä', 'å']

    f_finite(regex, possibilities)


def test_additional_charset():
    regex = r'[^\w\d\s]'
    additional_charset = ['γ', 'β', 'α']
    possibilities = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':',
                     ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~', 'α', 'β', 'γ']

    f_finite(regex, possibilities, additional_charset)


def test_charclass_with_quantifier_from_0():
    regex = r'[b-d]{0,2}'
    possibilities = ['', 'b', 'c', 'd', 'bb', 'bc',
                     'bd', 'cb', 'cc', 'cd', 'db', 'dc', 'dd']

    f_finite(regex, set(possibilities))
