from .test_function import f_finite, f_infinite


def test_two_alternatives():
    regex = r'a|b'
    possibilities = ['a', 'b']

    f_finite(regex, possibilities)


def test_alternatives_with_quantifier_on_second_option():
    regex = r'a|b*'
    possibilities = ['a', '', 'b', 'bb', 'bbb', 'bbbb', 'bbbbb']

    f_infinite(regex, possibilities)


def test_alternatives_with_quantifier_plus_on_first_option():
    regex = r'a+|b'
    possibilities = ['b', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regex, possibilities)


def test_multiple_alternatives():
    regex = r'a|b|c'
    possibilities = ['a', 'b', 'c']

    f_finite(regex, possibilities)


def test_alternative_with_literal_and_character_class():
    regex = r'a|[b-d]'
    possibilities = ['a', 'b', 'c', 'd']

    f_finite(regex, possibilities)


def test_alternative_with_character_class_and_literal():
    regex = r'[a-c]{ 0}|d'
    possibilities = ['', 'd']

    f_finite(regex, possibilities)


def test_alternation_with_character_classes_and_literals():
    regex = r'(a|[0-2])'
    possibilities = ['a', '0', '1', '2']

    f_finite(regex, possibilities)


def test_nested_alternation():
    regex = r'((a|b)|c)'
    possibilities = ['a', 'b', 'c']

    f_finite(regex, possibilities)


def test_alternation_with_grouping():
    regex = r'(a(b|c)d|x)'
    possibilities = ['abd', 'acd', 'x']

    f_finite(regex, possibilities)


def test_same_alternative_twice():
    regex = r'a{1,2}|a{1,2}'
    possibilities = ['a', 'aa']

    f_finite(regex, possibilities)
