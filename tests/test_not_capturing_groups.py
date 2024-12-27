from .test_function import f_finite


def test_not_capturing_groups():
    regex = r'(?:a)(b)\1'
    possibilities = ['abb']

    f_finite(regex, possibilities)
