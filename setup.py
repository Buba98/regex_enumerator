from setuptools import setup, find_packages

setup(
    name='regex_enumerator',
    version='0.1.0',
    packages=find_packages(include=['regex_enumerator', 'regex_enumerator.*']),
    description='Enumerate all strings that match a given regex',
    author='Vincenzo Greco',
    author_email='grecovincenzo98@gmail.com',
    extras_require={
        'dev': ['pytest', 'pytest-benchmark'],  # Development dependencies, e.g., for testing
    },
)