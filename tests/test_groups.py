from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite


def test_single_capturing_group_with_literal():
    regexEnumerator = RegexEnumerator(r'(a)')
    possibilities = ['a']

    f_finite(regexEnumerator, possibilities)


def test_single_capturing_group_with_class_single_char():
    regexEnumerator = RegexEnumerator(r'([a])')
    possibilities = ['a']

    f_finite(regexEnumerator, possibilities)


def test_single_capturing_group_with_class_multi_char():
    regexEnumerator = RegexEnumerator(r'([a-c])')
    possibilities = ['a', 'b', 'c']

    f_finite(regexEnumerator, possibilities)


def test_capturing_group_with_star_quantifier():
    regexEnumerator = RegexEnumerator(r'(a)*')
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)


def test_named_capturing_group_with_optional_subgroup():
    regexEnumerator = RegexEnumerator(r'(?<name>a[bcd](e)?)')
    possibilities = ['ab', 'abe', 'ac', 'ace', 'ad', 'ade']

    f_finite(regexEnumerator, possibilities)


def test_literal_followed_by_group_with_star_quantifier():
    regexEnumerator = RegexEnumerator(r'a(b)*')
    possibilities = ['a' + 'b' * i for i in range(6)]

    f_infinite(regexEnumerator, possibilities)


def test_two_capturing_groups_with_star_quantifiers():
    regexEnumerator = RegexEnumerator(r'(a)*(b)*')
    possibilities = ['a' * i + 'b' * j for i in range(6) for j in range(6)]

    f_infinite(regexEnumerator, possibilities)


def test_nested_capturing_groups():
    regexEnumerator = RegexEnumerator(r'(a(b(c)))')
    possibilities = ['abc']

    f_finite(regexEnumerator, possibilities)


def test_capturing_groups_in_sequence():
    regexEnumerator = RegexEnumerator(r'((a)(b))')
    possibilities = ['ab']

    f_finite(regexEnumerator, possibilities)


def test_non_capturing_group():
    regexEnumerator = RegexEnumerator(r'(?:a|b)*')
    possibilities = ['', 'a', 'b', 'aa', 'ab', 'ba', 'bb']

    f_infinite(regexEnumerator, possibilities)


def test_non_capturing_group_with_quantifier():
    regexEnumerator = RegexEnumerator(r'(?:ab)+')
    possibilities = ['ab', 'abab', 'ababab']

    f_infinite(regexEnumerator, possibilities)


def test_named_capturing_group_with_quantifier():
    regexEnumerator = RegexEnumerator(r'(?<chars>[ab]{1,2})')
    possibilities = ['a', 'b', 'aa', 'ab', 'ba', 'bb']

    f_finite(regexEnumerator, possibilities)


def test_nested_non_capturing_groups():
    regexEnumerator = RegexEnumerator(r'(?:a(?:b(?:c)))?')
    possibilities = ['', 'abc']

    f_finite(regexEnumerator, possibilities)


def test_group_for_quantifier_scope():
    regexEnumerator = RegexEnumerator(r'(ab)+')
    possibilities = ['ab', 'abab', 'ababab']

    f_infinite(regexEnumerator, possibilities)

def test_group_with_char_class_infinite_repetition():
    regexEnumerator = RegexEnumerator(r'([ab])+')
    possibilities = ['a', 'b', 'aa', 'ab', 'ba', 'bb']

    f_infinite(regexEnumerator, possibilities)