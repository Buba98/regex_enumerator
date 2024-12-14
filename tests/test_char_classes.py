from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite

def test_single_char_class():
    regexEnumerator = RegexEnumerator(r'[a]')
    possibilities = ['a']

    f_finite(regexEnumerator, possibilities)

def test_single_char_class_with_2_char():
    regexEnumerator = RegexEnumerator(r'[ab]')
    possibilities = ['a', 'b']

    f_finite(regexEnumerator, possibilities)


def test_single_char_class_with_quantifier():
    regexEnumerator = RegexEnumerator(r'[a]*')
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regexEnumerator, possibilities)

def test_multiple_char_class():
    regexEnumerator = RegexEnumerator(r'[a-c]')
    possibilities = ['a', 'b', 'c']

    f_finite(regexEnumerator, possibilities)

def test_multiple_char_class_with_quantifier():
    regexEnumerator = RegexEnumerator(r'[a-c]{1,2}')
    possibilities = ['a', 'b', 'c', 'aa', 'ab', 'ac', 'ba', 'bb', 'bc', 'ca', 'cb', 'cc']

    f_finite(regexEnumerator, possibilities)

def test_multiple_char_class_with_quantifier_0():
    regexEnumerator = RegexEnumerator(r'[a-c]{0}')
    possibilities = ['']

    f_finite(regexEnumerator, possibilities)

def test_multiple_char_class_with_quantifier_plus():
    regexEnumerator = RegexEnumerator(r'[a-b]+')
    possibilities = ['a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa', 'aab', 'aba', 'abb', 'baa', 'bab', 'bba', 'bbb']

    f_infinite(regexEnumerator, possibilities)

def test_2_multiple_char_class_with_quantifier_question():
    regexEnumerator = RegexEnumerator(r'[a-cf-g]?')
    possibilities = ['', 'a', 'b', 'c', 'f', 'g']

    f_finite(regexEnumerator, possibilities)