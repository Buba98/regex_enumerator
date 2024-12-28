from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='regex_enumerator',
    version='0.10.0',
    packages=find_packages(include=['regex_enumerator', 'regex_enumerator.*']),
    description='Enumerate all strings that match a given regex',
    author='Vincenzo Greco',
    author_email='grecovincenzo98@gmail.com',
    extras_require={
        'dev': ['pytest', 'pytest-cov'],
    },
    url='https://github.com/Buba98/regex_enumerator',
    keywords=['regex', 'regex enumerator', 'regular expression', 'enumerator', 'string generation',
              'exhaustive matching', 'exhaustive search', 'regex testing', 'regex tools', 'string enumeration', 'data generation'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.10',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT',
)
