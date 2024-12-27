from .test_function import f_finite


def test_digit_escape():
    regex = r'\d'
    possibilities = [str(i) for i in range(10)]

    f_finite(regex, possibilities)


def test_digit_escape_with_quantifier():
    regex = r'\d{1 , 2 }'
    possibilities = [str(i) for i in range(10)] + [str(i) + str(j)
                                                   for i in range(10) for j in range(10)]

    f_finite(regex, possibilities)


def test_non_digit_escape():
    regex = r'\D'
    possibilities = [chr(i)
                     for i in range(32, 127) if chr(i) not in '0123456789']

    f_finite(regex, possibilities)


def test_word_escape():
    regex = r'\w'
    possibilities = [chr(i) for i in range(
        32, 127) if chr(i).isalnum() or chr(i) == '_']

    f_finite(regex, possibilities)


def test_non_word_escape():
    regex = r'\W'
    possibilities = [chr(i) for i in range(
        32, 127) if not (chr(i).isalnum() or chr(i) == '_')]

    f_finite(regex, possibilities)


def test_whitespace_escape():
    regex = r'\s'
    possibilities = [' ', '\t', '\n', '\r', '\f', '\v']

    f_finite(regex, possibilities)


def test_non_whitespace_escape():
    regex = r'\S'
    possibilities = [chr(i) for i in range(
        32, 127) if chr(i) not in ' \t\n\r\f\v']

    f_finite(regex, possibilities)


def test_tab_escape():
    regex = r'\t'
    possibilities = ['\t']

    f_finite(regex, possibilities)


def test_carriage_return_escape():
    regex = r'\r'
    possibilities = ['\r']

    f_finite(regex, possibilities)


def test_newline_escape():
    regex = r'\n'
    possibilities = ['\n']

    f_finite(regex, possibilities)


def test_vertical_tab_escape():
    regex = r'\v'
    possibilities = ['\v']

    f_finite(regex, possibilities)


def test_form_feed_escape():
    regex = r'\f'
    possibilities = ['\f']

    f_finite(regex, possibilities)


def test_hex_escape():
    regex = r'\x41'
    possibilities = ['A']

    f_finite(regex, possibilities)


def test_escaped_open_square_bracket():
    regex = r'\['
    possibilities = ['[']

    f_finite(regex, possibilities)


def test_escaped_open_close_square_brackets():
    regex = r'\[\]'
    possibilities = ['[]']

    f_finite(regex, possibilities)


def test_escaped_characters_inside_character_class():
    regex = r'[\[\]]'
    possibilities = ['[', ']']

    f_finite(regex, possibilities)


def test_escaped_char_interrups_range_after_divider():
    regex = r'[a-\d]'
    possibilities = ['a', '-', '0', '1', '2',
                     '3', '4', '5', '6', '7', '8', '9']

    f_finite(regex, possibilities)


def test_escaped_char_interrups_range_after_1st_char():

    regex = r'[\[\d]'
    possibilities = ['[', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    f_finite(regex, possibilities)


def test_escaped_unicode_literal():
    regex = r'\u00E0'
    possibilities = ['à']

    f_finite(regex, possibilities)
