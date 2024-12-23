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


def test_wildcard_with_unicode():
    regexEnumerator = RegexEnumerator(r'.', additional_charset='¡¢£')
    possibilities = [chr(i) for i in range(32, 127)] + ['¡', '¢', '£']


def test_done():
    regexEnumerator = RegexEnumerator(r'')
    possibilities = ['', None]

    f_finite(regexEnumerator, possibilities)


def test_weak_password(benchmark):
    regexEnumerator = RegexEnumerator(
        r'[Ll][Oo0][Vv][Ee3]([Yy][Oo0][Uu])?(2023|2024)[!1.]{1,2}')
    possibilities = []

    you_or_not = []
    for y in 'Yy':
        for o in 'Oo0':
            for u in 'Uu':
                you_or_not.append(y + o + u)
    you_or_not.append('')

    for l_char in 'Ll':
        for o in 'Oo0':
            for v in 'Vv':
                for e in 'Ee3':
                    for y in you_or_not:
                        for year in ['2023', '2024']:
                            for special_1 in ['!', '1', '.']:
                                for special_2 in ['!', '1', '.', '']:
                                    possibilities.append(
                                        l_char + o + v + e + y + year + special_1 + special_2)

    benchmark(f_finite, regexEnumerator, possibilities)
