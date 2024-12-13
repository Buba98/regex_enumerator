from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite

def test_single_alternative():
    regexEnumerator = RegexEnumerator('a|b')
    possibilities = ['a', 'b']

    f_finite(regexEnumerator, possibilities)

def test_single_alternative_with_quantifier():
    regexEnumerator = RegexEnumerator('a|b*')
    possibilities = ['a', '', 'b', 'bb', 'bbb', 'bbbb', 'bbbbb']

    f_infinite(regexEnumerator, possibilities)

def test_single_alternative_with_quantifier_plus():
    regexEnumerator = RegexEnumerator('a+|b')
    possibilities = ['b', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)

def test_multiple_alternatives():
    regexEnumerator = RegexEnumerator('a|b|c')
    possibilities = ['a', 'b', 'c']

    f_finite(regexEnumerator, possibilities)

def test_alternative_with_char_and_class():
    regexEnumerator = RegexEnumerator('a|[b-d]')
    possibilities = ['a', 'b', 'c', 'd']

    f_finite(regexEnumerator, possibilities)

def test_alternative_with_class_with_quantifier_0_and_char():
    regexEnumerator = RegexEnumerator('[a-c]{0}|d')
    possibilities = ['', 'd']

    f_finite(regexEnumerator, possibilities)