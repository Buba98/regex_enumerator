from regex_enumerator import RegexEnumerator
from .test_function import f_finite


def test_digit_escape(benchmark):
    regexEnumerator = RegexEnumerator(r'\d')
    possibilities = [str(i) for i in range(10)]

    benchmark(f_finite, regexEnumerator, possibilities)


def test_digit_escape_with_quantifier(benchmark):
    regexEnumerator = RegexEnumerator(r'\d{1 , 2 }')
    possibilities = [str(i) for i in range(10)] + [str(i) + str(j)
                                                   for i in range(10) for j in range(10)]

    benchmark(f_finite, regexEnumerator, possibilities)


def test_non_digit_escape(benchmark):
    regexEnumerator = RegexEnumerator(r'\D')
    possibilities = [chr(i)
                     for i in range(32, 127) if chr(i) not in '0123456789']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_word_escape(benchmark):
    regexEnumerator = RegexEnumerator(r'\w')
    possibilities = [chr(i) for i in range(
        32, 127) if chr(i).isalnum() or chr(i) == '_']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_non_word_escape(benchmark):
    regexEnumerator = RegexEnumerator(r'\W')
    possibilities = [chr(i) for i in range(
        32, 127) if not (chr(i).isalnum() or chr(i) == '_')]

    benchmark(f_finite, regexEnumerator, possibilities)


def test_whitespace_escape(benchmark):
    regexEnumerator = RegexEnumerator(r'\s')
    possibilities = [' ', '\t', '\n', '\r', '\f', '\v']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_non_whitespace_escape(benchmark):
    regexEnumerator = RegexEnumerator(r'\S')
    possibilities = [chr(i) for i in range(
        32, 127) if chr(i) not in ' \t\n\r\f\v']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_tab_escape(benchmark):
    regexEnumerator = RegexEnumerator(r'\t')
    possibilities = ['\t']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_carriage_return_escape(benchmark):
    regexEnumerator = RegexEnumerator(r'\r')
    possibilities = ['\r']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_newline_escape(benchmark):
    regexEnumerator = RegexEnumerator(r'\n')
    possibilities = ['\n']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_vertical_tab_escape(benchmark):
    regexEnumerator = RegexEnumerator(r'\v')
    possibilities = ['\v']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_form_feed_escape(benchmark):
    regexEnumerator = RegexEnumerator(r'\f')
    possibilities = ['\f']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_hex_escape(benchmark):
    regexEnumerator = RegexEnumerator(r'\x41')
    possibilities = ['A']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_escaped_open_square_bracket(benchmark):
    regexEnumerator = RegexEnumerator(r'\[')
    possibilities = ['[']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_escaped_open_close_square_brackets(benchmark):
    regexEnumerator = RegexEnumerator(r'\[\]')
    possibilities = ['[]']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_escaped_characters_inside_character_class(benchmark):
    regexEnumerator = RegexEnumerator(r'[\[\]]')
    possibilities = ['[', ']']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_escaped_char_interrups_range_after_divider(benchmark):
    regexEnumerator = RegexEnumerator(r'[a-\d]')
    possibilities = ['a', '-', '0', '1', '2',
                     '3', '4', '5', '6', '7', '8', '9']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_escaped_char_interrups_range_after_1st_char(benchmark):

    regexEnumerator = RegexEnumerator(r'[\[\d]')
    possibilities = ['[', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_escaped_unicode_literal(benchmark):
    regexEnumerator = RegexEnumerator(r'\u00E0')
    possibilities = ['à']

    benchmark(f_finite, regexEnumerator, possibilities)
