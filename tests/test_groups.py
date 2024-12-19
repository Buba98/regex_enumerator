from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite


def test_single_group_literal_char():
    regexEnumerator = RegexEnumerator(r'(a)')
    possibilities = ['a']

    f_finite(regexEnumerator, possibilities)


def test_single_character_class():
    regexEnumerator = RegexEnumerator(r'([a])')
    possibilities = ['a']

    f_finite(regexEnumerator, possibilities)


def test_multiple_character_class():
    regexEnumerator = RegexEnumerator(r'([a-c])')
    possibilities = ['a', 'b', 'c']

    f_finite(regexEnumerator, possibilities)


def test_group_with_zero_or_more_quantifier():
    regexEnumerator = RegexEnumerator(r'(a)*')
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)


def test_named_group():
    regexEnumerator = RegexEnumerator(r'(?<name>a[bcd](e)?)')
    possibilities = ['ab', 'abe', 'ac', 'ace', 'ad', 'ade']

    f_finite(regexEnumerator, possibilities)


def test_group_with_range_quantifier_after_literal():
    regexEnumerator = RegexEnumerator(r'a(b)*')
    possibilities = ['a' + 'b' * i for i in range(6)]

    f_infinite(regexEnumerator, possibilities)


def test_2_groups_with_range_quantifier():
    regexEnumerator = RegexEnumerator(r'(a)*(b)*')
    possibilities = ['a' * i + 'b' * j for i in range(6) for j in range(6)]

    f_infinite(regexEnumerator, possibilities)


def test_nested_groups():
    regexEnumerator = RegexEnumerator(r'(a(b(c)))')
    possibilities = ['abc']

    f_finite(regexEnumerator, possibilities)


def test_group_of_groups():
    regexEnumerator = RegexEnumerator(r'((a)(b))')
    possibilities = ['ab']

    f_finite(regexEnumerator, possibilities)
