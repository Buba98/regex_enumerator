from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite

def test_char_class_surronded_by_other_chars():
    regexEnumerator = RegexEnumerator('a[0-9]b')
    possibilities = ['a0b', 'a1b', 'a2b', 'a3b', 'a4b', 'a5b', 'a6b', 'a7b', 'a8b', 'a9b']

    f_finite(regexEnumerator, possibilities)