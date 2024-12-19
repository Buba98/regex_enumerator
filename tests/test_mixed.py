from regex_enumerator import RegexEnumerator
from .test_function import f_finite


def test_character_class_between_literals():
    regexEnumerator = RegexEnumerator(r'a[0-9]b')
    possibilities = ['a0b', 'a1b', 'a2b', 'a3b',
                     'a4b', 'a5b', 'a6b', 'a7b', 'a8b', 'a9b']

    f_finite(regexEnumerator, possibilities)


def test_single_wildcard():
    regexEnumerator = RegexEnumerator(r'.')
    possibilities = [chr(i) for i in range(32, 127)]

    f_finite(regexEnumerator, possibilities)


def test_done():
    regexEnumerator = RegexEnumerator(r'')
    possibilities = ['', None]

    f_finite(regexEnumerator, possibilities)
