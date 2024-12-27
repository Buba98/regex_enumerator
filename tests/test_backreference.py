from .test_function import f_finite, f_infinite


def test_backreference():
    regex = r'(a)\1'
    possibilities = ['aa']

    f_finite(regex, possibilities)


def test_backreference_with_group_quantifier():
    regex = r'(a)+\1'
    possibilities = ['aa' * i for i in range(1, 6)]

    f_infinite(regex, possibilities)


def test_backreference_with_quantifier():
    regex = r'(a)\1+'
    possibilities = ['a' * i + 'a' for i in range(1, 6)]

    f_infinite(regex, possibilities)


def test_backreference_with_named_group():
    regex = r'(?<name>[a-b])\k<name>'
    possibilities = ['aa', 'bb']

    f_finite(regex, possibilities)


def test_backreference_with_named_group_and_quantifier():
    regex = r'(?<name>[a-b])\k<name>{1, 2}'
    possibilities = ['aa', 'bb', 'aaa', 'bbb']

    f_finite(regex, possibilities)


def test_zero_width_backreference():
    regex = r'(a)?\1{0}'
    possibilities = ['a', '']

    f_finite(regex, possibilities)


def test_10_backreference():
    regex = r'(a)(b)(c)(d)(e)(f)(g)(h)(i)(j)\10'
    possibilities = ['abcdefghijj']

    f_finite(regex, possibilities)


def test_multiple_backreferences():
    regex = r'(a)(b)\2\1'
    possibilities = ['abba']

    f_finite(regex, possibilities)


def test_backreference_with_mismatch():
    regex = r'(a)(b)\1'
    possibilities = ['aba']

    f_finite(regex, possibilities)


def test_named_group_with_backreference():
    regex = r'(?<letter>[ab])\k<letter>'
    possibilities = [
        'aa', 'bb'
    ]

    f_finite(regex, possibilities)


def test_named_group_infinite_repetition_with_backreference():
    regex = r'(?<letter>[ab])+\k<letter>'
    possibilities = [
        'aa', 'bb', 'abab', 'baba', 'aaaa', 'bbbb'
    ]

    f_infinite(regex, possibilities)


def test_backreference_with_group_quantifier_and_mismatch():
    regex = r'(a){1,3}\1{0,2}'
    possibilities = ['a', 'aa', 'aaa', 'aaaa', 'aaaaaa', 'aaaaaaaaa']

    f_finite(regex, possibilities)


def test_backreference_with_group_quantifier_and_mismatch_complex():
    regex = r'(a){1,3}[c-d]\1{0,2}'
    possibilities = ['ac', 'ad', 'aca', 'ada', 'acaa', 'adaa',
                     'aac', 'aad', 'aacaa', 'aadaa', 'aacaaaa', 'aadaaaa',
                     'aaac', 'aaad', 'aaacaaa', 'aaadaaa', 'aaacaaaaaa', 'aaadaaaaaa']

    f_finite(regex, possibilities)
