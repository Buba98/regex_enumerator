from regex_enumerator import RegexEnumerator
from .test_function import f_finite


def test_digit_escape():
    regexEnumerator = RegexEnumerator(r'\d')
    possibilities = [str(i) for i in range(10)]

    f_finite(regexEnumerator, possibilities)


def test_digit_escape_with_quantifier():
    regexEnumerator = RegexEnumerator(r'\d{1 , 2 }')
    possibilities = [str(i) for i in range(10)] + [str(i) + str(j)
                                                   for i in range(10) for j in range(10)]

    f_finite(regexEnumerator, possibilities)


def test_non_digit_escape():
    regexEnumerator = RegexEnumerator(r'\D')
    possibilities = [chr(i)
                     for i in range(32, 127) if chr(i) not in '0123456789']

    f_finite(regexEnumerator, possibilities)


def test_word_escape():
    regexEnumerator = RegexEnumerator(r'\w')
    possibilities = [chr(i) for i in range(
        32, 127) if chr(i).isalnum() or chr(i) == '_']

    f_finite(regexEnumerator, possibilities)


def test_non_word_escape():
    regexEnumerator = RegexEnumerator(r'\W')
    possibilities = [chr(i) for i in range(
        32, 127) if not (chr(i).isalnum() or chr(i) == '_')]

    f_finite(regexEnumerator, possibilities)


def test_whitespace_escape():
    regexEnumerator = RegexEnumerator(r'\s')
    possibilities = [' ', '\t', '\n', '\r', '\f', '\v']

    f_finite(regexEnumerator, possibilities)


def test_non_whitespace_escape():
    regexEnumerator = RegexEnumerator(r'\S')
    possibilities = [chr(i) for i in range(
        32, 127) if chr(i) not in ' \t\n\r\f\v']

    f_finite(regexEnumerator, possibilities)


def test_tab_escape():
    regexEnumerator = RegexEnumerator(r'\t')
    possibilities = ['\t']

    f_finite(regexEnumerator, possibilities)


def test_carriage_return_escape():
    regexEnumerator = RegexEnumerator(r'\r')
    possibilities = ['\r']

    f_finite(regexEnumerator, possibilities)


def test_newline_escape():
    regexEnumerator = RegexEnumerator(r'\n')
    possibilities = ['\n']

    f_finite(regexEnumerator, possibilities)


def test_vertical_tab_escape():
    regexEnumerator = RegexEnumerator(r'\v')
    possibilities = ['\v']

    f_finite(regexEnumerator, possibilities)


def test_form_feed_escape():
    regexEnumerator = RegexEnumerator(r'\f')
    possibilities = ['\f']

    f_finite(regexEnumerator, possibilities)


def test_hex_escape():
    regexEnumerator = RegexEnumerator(r'\x41')
    possibilities = ['A']

    f_finite(regexEnumerator, possibilities)


def test_escaped_open_square_bracket():
    regexEnumerator = RegexEnumerator(r'\[')
    possibilities = ['[']

    f_finite(regexEnumerator, possibilities)


def test_escaped_open_close_square_brackets():
    regexEnumerator = RegexEnumerator(r'\[\]')
    possibilities = ['[]']

    f_finite(regexEnumerator, possibilities)


def test_escaped_characters_inside_character_class():
    regexEnumerator = RegexEnumerator(r'[\[\]]')
    possibilities = ['[', ']']

    f_finite(regexEnumerator, possibilities)
