from regex_enumerator import RegexEnumerator
from .test_function import f_finite


def test_character_class_between_literals():
    regex = r'a[0-9]b'
    possibilities = ['a0b', 'a1b', 'a2b', 'a3b',
                     'a4b', 'a5b', 'a6b', 'a7b', 'a8b', 'a9b']

    f_finite(regex, possibilities)


def test_single_wildcard():
    regex = r'.'
    possibilities = [chr(i) for i in range(32, 127)]

    f_finite(regex, possibilities)


def test_wildcard_with_unicode():
    regex = r'.'
    additional_charset = '¡¢£'
    possibilities = [chr(i) for i in range(32, 127)] + ['¡', '¢', '£']

    f_finite(regex, possibilities, additional_charset)


def test_done():
    regex = r''
    possibilities = ['', None]

    f_finite(regex, possibilities)


def test_empty_additional_charset():
    regexEnumerator = RegexEnumerator(r'')
    assert regexEnumerator.next() == ''
    assert regexEnumerator.next() == None


def test_weak_password():
    regex = r'[Ll][Oo0][Vv][Ee3]([Yy][Oo0][Uu])?(2023|2024|123)?[!1.]{1,2}'
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
                        for year in ['2023', '2024', '123', '']:
                            for special_1 in ['!', '1', '.']:
                                for special_2 in ['!', '1', '.', '']:
                                    possibilities.append(
                                        l_char + o + v + e + y + year + special_1 + special_2)

    f_finite(regex, possibilities)


def test_complete_regex():
    regex = r'[Ll]([Uu])?\1{0,2}(0|1){0,3}[!1.]'
    possibilities = []

    for l_char in 'Ll':
        for u in ['U', 'UU', 'UUU', 'u', 'uu', 'uuu', '']:
            for num in ['0', '1', '00', '01', '10', '11', '000', '001', '010', '011', '100', '101', '110', '111', '']:
                for special in ['!', '1', '.']:
                    possibilities.append(l_char + u + num + special)

    f_finite(regex, possibilities)
