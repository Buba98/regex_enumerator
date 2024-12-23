from regex_enumerator import RegexEnumerator
from .test_function import f_finite, f_infinite


def test_not_capturing_groups(benchmark):
    regexEnumerator = RegexEnumerator(r'(?:a)(b)\1')
    possibilities = ['abb']

    benchmark(f_finite, regexEnumerator, possibilities)
