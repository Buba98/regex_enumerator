from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite

def test_d_escape():
    regexEnumerator = RegexEnumerator(r'\d')
    possibilities = [str(i) for i in range(10)]

    f_finite(regexEnumerator, possibilities)

def test_d_escape_with_quantifier():
    regexEnumerator = RegexEnumerator(r'\d{1,2}')
    possibilities = [str(i) for i in range(10)] + [str(i) + str(j) for i in range(10) for j in range(10)]

    f_finite(regexEnumerator, possibilities)

def test_D_escape():
    regexEnumerator = RegexEnumerator(r'\D')
    possibilities = [chr(i) for i in range(32, 127) if chr(i) not in '0123456789']

    f_finite(regexEnumerator, possibilities)

def test_w_escape():
    regexEnumerator = RegexEnumerator(r'\w')
    possibilities = [chr(i) for i in range(32, 127) if chr(i).isalnum() or chr(i) == '_']

    f_finite(regexEnumerator, possibilities)

def test_W_escape():
    regexEnumerator = RegexEnumerator(r'\W')
    possibilities = [chr(i) for i in range(32, 127) if not (chr(i).isalnum() or chr(i) == '_')]

    f_finite(regexEnumerator, possibilities)

def test_s_escape():
    regexEnumerator = RegexEnumerator(r'\s')
    possibilities = [' ', '\t', '\n', '\r', '\f', '\v']

    f_finite(regexEnumerator, possibilities)

def test_S_escape():
    regexEnumerator = RegexEnumerator(r'\S')
    possibilities = [chr(i) for i in range(32, 127) if chr(i) not in ' \t\n\r\f\v']

    f_finite(regexEnumerator, possibilities)

def test_t_escape():
    regexEnumerator = RegexEnumerator(r'\t')
    possibilities = ['\t']

    f_finite(regexEnumerator, possibilities)

def test_r_escape():
    regexEnumerator = RegexEnumerator(r'\r')
    possibilities = ['\r']

    f_finite(regexEnumerator, possibilities)

def test_n_escape():
    regexEnumerator = RegexEnumerator(r'\n')
    possibilities = ['\n']

    f_finite(regexEnumerator, possibilities)

def test_v_escape():
    regexEnumerator = RegexEnumerator(r'\v')
    possibilities = ['\v']

    f_finite(regexEnumerator, possibilities)

def test_f_escape():
    regexEnumerator = RegexEnumerator(r'\f')
    possibilities = ['\f']

    f_finite(regexEnumerator, possibilities)

def test_x_escape():
    regexEnumerator = RegexEnumerator(r'\x41')
    possibilities = ['A']

    f_finite(regexEnumerator, possibilities)

def test_escaped_special_char():
    regexEnumerator = RegexEnumerator(r'\[')
    possibilities = ['[']

    f_finite(regexEnumerator, possibilities)

def test_escaped_special_char_with_quantifier():
    regexEnumerator = RegexEnumerator(r'\[\]')
    possibilities = ['[]']

    f_finite(regexEnumerator, possibilities)

def test_escaped_inside_char_class():
    regexEnumerator = RegexEnumerator(r'[\[\]]')
    possibilities = ['[', ']']

    f_finite(regexEnumerator, possibilities)