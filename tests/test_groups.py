from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite


def test_single_capturing_group_with_literal(benchmark):
    regexEnumerator = RegexEnumerator(r'(a)')
    possibilities = ['a']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_single_capturing_group_with_class_single_char(benchmark):
    regexEnumerator = RegexEnumerator(r'([a])')
    possibilities = ['a']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_single_capturing_group_with_class_multi_char(benchmark):
    regexEnumerator = RegexEnumerator(r'([a-c])')
    possibilities = ['a', 'b', 'c']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_capturing_group_with_star_quantifier(benchmark):
    regexEnumerator = RegexEnumerator(r'(a)*')
    possibilities = ['', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_named_capturing_group_with_optional_subgroup(benchmark):
    regexEnumerator = RegexEnumerator(r'(?<name>a[bcd](e)?)')
    possibilities = ['ab', 'abe', 'ac', 'ace', 'ad', 'ade']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_literal_followed_by_group_with_star_quantifier(benchmark):
    regexEnumerator = RegexEnumerator(r'a(b)*')
    possibilities = ['a' + 'b' * i for i in range(6)]

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_two_capturing_groups_with_star_quantifiers(benchmark):
    regexEnumerator = RegexEnumerator(r'(a)*(b)*')
    possibilities = ['a' * i + 'b' * j for i in range(6) for j in range(6)]

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_nested_capturing_groups(benchmark):
    regexEnumerator = RegexEnumerator(r'(a(b(c)))')
    possibilities = ['abc']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_capturing_groups_in_sequence(benchmark):
    regexEnumerator = RegexEnumerator(r'((a)(b))')
    possibilities = ['ab']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_non_capturing_group(benchmark):
    regexEnumerator = RegexEnumerator(r'(?:a|b)*')
    possibilities = ['', 'a', 'b', 'aa', 'ab', 'ba', 'bb']

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_non_capturing_group_with_quantifier(benchmark):
    regexEnumerator = RegexEnumerator(r'(?:ab)+')
    possibilities = ['ab', 'abab', 'ababab']

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_named_capturing_group_with_quantifier(benchmark):
    regexEnumerator = RegexEnumerator(r'(?<chars>[ab]{1,2})')
    possibilities = ['a', 'b', 'aa', 'ab', 'ba', 'bb']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_nested_non_capturing_groups(benchmark):
    regexEnumerator = RegexEnumerator(r'(?:a(?:b(?:c)))?')
    possibilities = ['', 'abc']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_group_for_quantifier_scope(benchmark):
    regexEnumerator = RegexEnumerator(r'(ab)+')
    possibilities = ['ab', 'abab', 'ababab']

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_group_with_char_class_infinite_repetition(benchmark):
    regexEnumerator = RegexEnumerator(r'([ab])+')
    possibilities = ['a', 'b', 'aa', 'ab', 'ba', 'bb']

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_group_with_multiple_elements_with_qunatifiers(benchmark):
    regexEnumerator = RegexEnumerator(r'(a[b-d]{0,2}){0, 3}')
    possibilities = ['']
    char_class = ['', 'b', 'c', 'd', 'bb', 'bc',
                  'bd', 'cb', 'cc', 'cd', 'db', 'dc', 'dd']
    one = [f'a{c}' for c in char_class]
    two = [f'{c1}{c2}' for c1 in one for c2 in one]
    three = [f'{c1}{c2}{c3}' for c1 in one for c2 in one for c3 in one]
    possibilities.extend(one)
    possibilities.extend(two)
    possibilities.extend(three)
    possibilities = set(possibilities)

    benchmark(f_finite, regexEnumerator, possibilities)


def test_nested_groups_with_multiple_elements_with_quantifiers(benchmark):
    regexEnumerator = RegexEnumerator(r'(a([e-g]){1, 3}){0, 3}')
    possibilities = ['']
    group = ['e', 'f', 'g', 'ee', 'ef', 'eg', 'fe', 'ff', 'fg', 'ge', 'gf', 'gg', 'eee', 'eef', 'eeg', 'efe', 'eff', 'efg', 'ege', 'egf', 'egg',
             'fee', 'fef', 'feg', 'ffe', 'fff', 'ffg', 'fge', 'fgf', 'fgg', 'gee', 'gef', 'geg', 'gfe', 'gff', 'gfg', 'gge', 'ggf', 'ggg']
    one = [f'a{g}' for g in group]
    two = [f'{g1}{g2}' for g1 in one for g2 in one]
    three = [f'{g1}{g2}{g3}' for g1 in one for g2 in one for g3 in one]
    possibilities.extend(one)
    possibilities.extend(two)
    possibilities.extend(three)
    possibilities = set(possibilities)

    benchmark(f_finite, regexEnumerator, possibilities)
