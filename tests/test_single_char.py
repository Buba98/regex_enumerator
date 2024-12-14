from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite

def test_empty_regex():
    regexEnumerator = RegexEnumerator(r'')
    possibilities = ['']

    f_finite(regexEnumerator, possibilities)

def test_single_char():
    regexEnumerator = RegexEnumerator(r'a')
    possibilities = ['a']

    f_finite(regexEnumerator, possibilities)

def test_single_char_with_quantifier():
    regexEnumerator = RegexEnumerator(r'a*')
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)

def test_single_char_with_quantifier_plus():
    regexEnumerator = RegexEnumerator(r'a+')
    possibilities = ['a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)

def test_single_char_with_quantifier_question():
    regexEnumerator = RegexEnumerator(r'a?')
    possibilities = ['', 'a']

    f_finite(regexEnumerator, possibilities)

def test_single_char_with_quantifier_braces():
    regexEnumerator = RegexEnumerator(r'a{2}')
    possibilities = ['aa']

    f_finite(regexEnumerator, possibilities)

def test_single_char_with_quantifier_braces_comma():
    regexEnumerator = RegexEnumerator(r'a{2,}')
    possibilities = ['aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)

def test_single_char_with_quantifier_braces_comma_max():
    regexEnumerator = RegexEnumerator(r'a{2,4}')
    possibilities = ['aa', 'aaa', 'aaaa']

    f_finite(regexEnumerator, possibilities)

def test_single_char_with_quantifier_0():
    regexEnumerator = RegexEnumerator(r'a{0}')
    possibilities = ['']

    f_finite(regexEnumerator, possibilities)