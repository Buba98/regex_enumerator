from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite


def test_two_alternatives(benchmark):
    regexEnumerator = RegexEnumerator(r'a|b')
    possibilities = ['a', 'b']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_alternatives_with_quantifier_on_second_option(benchmark):
    regexEnumerator = RegexEnumerator(r'a|b*')
    possibilities = ['a', '', 'b', 'bb', 'bbb', 'bbbb', 'bbbbb']

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_alternatives_with_quantifier_plus_on_first_option(benchmark):
    regexEnumerator = RegexEnumerator(r'a+|b')
    possibilities = ['b', 'a', 'aa', 'aaa', 'aaaa', 'aaaaa']

    benchmark(f_infinite, regexEnumerator, possibilities)


def test_multiple_alternatives(benchmark):
    regexEnumerator = RegexEnumerator(r'a|b|c')
    possibilities = ['a', 'b', 'c']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_alternative_with_literal_and_character_class(benchmark):
    regexEnumerator = RegexEnumerator(r'a|[b-d]')
    possibilities = ['a', 'b', 'c', 'd']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_alternative_with_character_class_and_literal(benchmarkbenchmark):
    regexEnumerator = RegexEnumerator(r'[a-c]{ 0}|d')
    possibilities = ['', 'd']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_alternation_with_character_classes_and_literals(benchmark):
    regexEnumerator = RegexEnumerator(r'(a|[0-2])')
    possibilities = ['a', '0', '1', '2']

    benchmark(f_finite, regexEnumerator, possibilities)


def test_nested_alternation(benchmark):
    regexEnumerator = RegexEnumerator(r'((a|b)|c)')
    possibilities = ['a', 'b', 'c']
    
    benchmark(f_finite, regexEnumerator, possibilities)


def test_alternation_with_grouping(benchmark):
    regexEnumerator = RegexEnumerator(r'(a(b|c)d|x)')
    possibilities = ['abd', 'acd', 'x']
    
    benchmark(f_finite, regexEnumerator, possibilities)

def test_same_alternative_twice(benchmark):
    regexEnumerator = RegexEnumerator(r'a{1,2}|a{1,2}')
    possibilities = ['a', 'aa']

    benchmark(f_finite, regexEnumerator, possibilities)