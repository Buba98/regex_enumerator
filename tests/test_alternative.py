from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite


def test_two_alternatives():
    regexEnumerator = RegexEnumerator(r'a|b')
    possibilities = ['a', 'b']

    f_finite(regexEnumerator, possibilities)


def test_alternatives_with_quantifier_on_second_option():
    regexEnumerator = RegexEnumerator(r'a|b*')
    possibilities = ['a', '', 'b', 'bb', 'bbb', 'bbbb', 'bbbbb']

    f_infinite(regexEnumerator, possibilities)


def test_alternatives_with_quantifier_plus_on_first_option():
    regexEnumerator = RegexEnumerator(r'a+|b')
    possibilities = ['b', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)


def test_multiple_alternatives():
    regexEnumerator = RegexEnumerator(r'a|b|c')
    possibilities = ['a', 'b', 'c']

    f_finite(regexEnumerator, possibilities)


def test_alternative_with_literal_and_character_class():
    regexEnumerator = RegexEnumerator(r'a|[b-d]')
    possibilities = ['a', 'b', 'c', 'd']

    f_finite(regexEnumerator, possibilities)


def test_alternative_with_character_class_and_literal():
    regexEnumerator = RegexEnumerator(r'[a-c]{ 0}|d')
    possibilities = ['', 'd']

    f_finite(regexEnumerator, possibilities)


def test_alternation_with_character_classes_and_literals():
    regexEnumerator = RegexEnumerator(r'(a|[0-2])')
    possibilities = ['a', '0', '1', '2']

    f_finite(regexEnumerator, possibilities)


def test_nested_alternation():
    regexEnumerator = RegexEnumerator(r'((a|b)|c)')
    possibilities = ['a', 'b', 'c']
    
    f_finite(regexEnumerator, possibilities)


def test_alternation_with_grouping():
    regexEnumerator = RegexEnumerator(r'(a(b|c)d|x)')
    possibilities = ['abd', 'acd', 'x']
    
    f_finite(regexEnumerator, possibilities)

def test_same_alternative_twice():
    regexEnumerator = RegexEnumerator(r'a{1,2}|a{1,2}')
    possibilities = ['a', 'aa']

    f_finite(regexEnumerator, possibilities)