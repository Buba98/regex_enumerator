from .test_function import f_finite, f_infinite


def test_single_capturing_group_with_literal():
    regex = r'(a)'
    possibilities = ['a']

    f_finite(regex, possibilities)


def test_single_capturing_group_with_class_single_char():
    regex = r'([a])'
    possibilities = ['a']

    f_finite(regex, possibilities)


def test_single_capturing_group_with_class_multi_char():
    regex = r'([a-c])'
    possibilities = ['a', 'b', 'c']

    f_finite(regex, possibilities)


def test_capturing_group_with_star_quantifier():
    regex = r'(a)*'
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    f_infinite(regex, possibilities)


def test_named_capturing_group_with_optional_subgroup():
    regex = r'(?<name>a[bcd](e)?)'
    possibilities = ['ab', 'abe', 'ac', 'ace', 'ad', 'ade']

    f_finite(regex, possibilities)


def test_literal_followed_by_group_with_star_quantifier():
    regex = r'a(b)*'
    possibilities = ['a' + 'b' * i for i in range(6)]

    f_infinite(regex, possibilities)


def test_two_capturing_groups_with_star_quantifiers():
    regex = r'(a)*(b)*'
    possibilities = ['a' * i + 'b' * j for i in range(6) for j in range(6)]

    f_infinite(regex, possibilities)


def test_nested_capturing_groups():
    regex = r'(a(b(c)))'
    possibilities = ['abc']

    f_finite(regex, possibilities)


def test_capturing_groups_in_sequence():
    regex = r'((a)(b))'
    possibilities = ['ab']

    f_finite(regex, possibilities)


def test_non_capturing_group():
    regex = r'(?:a|b)*'
    possibilities = ['', 'a', 'b', 'aa', 'ab', 'ba', 'bb']

    f_infinite(regex, possibilities)


def test_non_capturing_group_with_quantifier():
    regex = r'(?:ab)+'
    possibilities = ['ab', 'abab', 'ababab']

    f_infinite(regex, possibilities)


def test_named_capturing_group_with_quantifier():
    regex = r'(?<chars>[ab]{1,2})'
    possibilities = ['a', 'b', 'aa', 'ab', 'ba', 'bb']

    f_finite(regex, possibilities)


def test_nested_non_capturing_groups():
    regex = r'(?:a(?:b(?:c)))?'
    possibilities = ['', 'abc']

    f_finite(regex, possibilities)


def test_group_for_quantifier_scope():
    regex = r'(ab)+'
    possibilities = ['ab', 'abab', 'ababab']

    f_infinite(regex, possibilities)


def test_group_with_char_class_infinite_repetition():
    regex = r'([ab])+'
    possibilities = ['a', 'b', 'aa', 'ab', 'ba', 'bb']

    f_infinite(regex, possibilities)


def test_group_with_multiple_elements_with_qunatifiers():
    regex = r'(a[b-d]{0,2}){0, 3}'
    possibilities = ['']
    char_class = ['', 'b', 'c', 'd', 'bb', 'bc',
                  'bd', 'cb', 'cc', 'cd', 'db', 'dc', 'dd']
    one = [f'a{c}' for c in char_class]
    two = [f'{c1}{c2}' for c1 in one for c2 in one]
    three = [f'{c1}{c2}{c3}' for c1 in one for c2 in one for c3 in one]
    possibilities.extend(one)
    possibilities.extend(two)
    possibilities.extend(three)

    f_finite(regex, set(possibilities))


def test_nested_groups_with_multiple_elements_with_quantifiers():
    regex = r'(a([e-g]){1, 3}){0, 3}'
    possibilities = ['']
    group = ['e', 'f', 'g', 'ee', 'ef', 'eg', 'fe', 'ff', 'fg', 'ge', 'gf', 'gg', 'eee', 'eef', 'eeg', 'efe', 'eff', 'efg', 'ege', 'egf', 'egg',
             'fee', 'fef', 'feg', 'ffe', 'fff', 'ffg', 'fge', 'fgf', 'fgg', 'gee', 'gef', 'geg', 'gfe', 'gff', 'gfg', 'gge', 'ggf', 'ggg']
    one = [f'a{g}' for g in group]
    two = [f'{g1}{g2}' for g1 in one for g2 in one]
    three = [f'{g1}{g2}{g3}' for g1 in one for g2 in one for g3 in one]
    possibilities.extend(one)
    possibilities.extend(two)
    possibilities.extend(three)

    f_finite(regex, set(possibilities))


def test_group_with_alternative_empty():
    regex = r'(a|[]){3}'
    possibilities = ['', 'a', 'aa', 'aaa']

    f_finite(regex, possibilities)
