from setuptools import setup, find_packages

setup(
    name='regex_enumerator',
    version='0.3.1',
    packages=find_packages(include=['regex_enumerator', 'regex_enumerator.*']),
    description='Enumerate all strings that match a given regex',
    author='Vincenzo Greco',
    author_email='grecovincenzo98@gmail.com',
    extras_require={
        'dev': ['pytest', 'pytest-cov'],
    },
    url='https://github.com/Buba98/regex_enumerator',
    keywords=['regex', 'regex enumerator', 'regular-expression', 'enumerator', 'string-generation',
              'exhaustive-matching', 'regex-testing', 'regex-tools', 'string-enumeration', 'data-generation'],
)
