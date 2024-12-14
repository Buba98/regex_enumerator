# Regex enumerator
This library is ment to generate all the strings that match a given regex pattern. It is written in python and uses no external libraries.

## Usage
```python
from regex_enumerator import RegexEnumerator

# Create a RegexEnumerator
re = RegexEnumerator('a[0-9]b')

# Get the next string that matches the regex
print(re.next()) # a0b
print(re.next()) # a1b
print(re.next()) # a2b
```

## What is supported
- [x] Character classes
- [x] Quantifiers for character classes
- [x] Quantifiers for groups
- [x] Groups
- [x] Alternation 

## How it works
This library works by parsing the regex pattern. Once the pattern is parsed, it performs a breadth-first search on the tree of the pattern. This ensures to be able to generate all the strings and don't get stuck on a unbounded quantifier for a character class or group.

## Tests
The library contains a test suite that can be run with the following command:
```bash
pytest
```

## License
I don't know what license to use, so I'm going to use the MIT license. If you have any suggestions, please let me know.

## Contributors
Feel free to contribute to this project. I'm open to suggestions and improvements.
