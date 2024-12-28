# Regex enumerator

[![PyPI version](https://img.shields.io/pypi/v/regex-enumerator.svg)](https://pypi.org/project/regex-enumerator/)

This library is meant to generate all the strings that match a given regex pattern. It is written in python and uses no external libraries.

## Installation

```bash
pip install regex-enumerator
```

## Usage

Here's an example of how to use the library:

```python
from regex_enumerator import RegexEnumerator

# Create a RegexEnumerator
re = RegexEnumerator(r'a[0-9]b')

# Get the next string that matches the regex
print(re.next()) # a0b
print(re.next()) # a1b
print(re.next()) # a2b
```

## What is supported

- [x] Character classes
- [x] Quantifiers (greedy)
- [x] Groups (named and unnamed)
- [x] Alternation
- [x] Escaped characters
- [x] Backreferences (named and unnamed)
- [x] Non-capturing groups

## What I plan to support

- [ ] Lookahead and lookbehind

## What is not supported

- [ ] Unicode properties
- [ ] Word boundaries
- [ ] Anchors
- [ ] Non-greedy quantifiers

## Charset

The library supports ASCII characters by default. To handle Unicode characters, include them explicitly in your regex or define a custom character set.

```python
from regex_enumerator import RegexEnumerator

# Directly in regex
regex_enum = RegexEnumerator(r'£')
print(regex_enum.next())  # £

# Using additional_charset
unicode_charset = [chr(i) for i in range(ord('¡'), ord('£'))]
unicode_charset = ['¡', '¢', '£']
unicode_charset = '¡¢£'
unicode_charset = ['¡¢', '£']

regex_enum = RegexEnumerator(r'.', additional_charset=unicode_charset)

result = []
while (char := regex_enum.next()) is not None:
    result.append(char)

assert '¡' in result
assert '¢' in result
assert '£' in result
```

## How it works

This library works by parsing the regex pattern into a tree structure. Once parsed, it performs a breadth-first search (BFS) on the tree to generate all matching strings. This ensures it does not get stuck on unbounded quantifiers for character classes or groups.

## Tests

The library includes a comprehensive test suite. To run the tests, use the following command:

```bash
pytest
```

## License

I don't know what license to use, so I'm going to use the MIT license. If you have any suggestions, please let me know.

## Contributors

Feel free to contribute to this project. I'm open to suggestions and improvements.
