import pytest
from regex_enumerator import RegexEnumerator
from regex_enumerator.regex_parser import RegexError


def test_grammar_group():
    with pytest.raises(RegexError, match='Invalid group'):
        RegexEnumerator(r'(?)')

    with pytest.raises(RegexError, match='Invalid group'):
        RegexEnumerator(r'(?')

    with pytest.raises(RegexError, match='Invalid named group'):
        RegexEnumerator(r'(?<>)')

    with pytest.raises(RegexError, match='Invalid named group'):
        RegexEnumerator(r'(?<')

    with pytest.raises(RegexError, match='Duplicate named group'):
        RegexEnumerator(r'(?<name>a)(?<name>b)')

    with pytest.raises(RegexError, match='Invalid group'):
        RegexEnumerator(r'(?a)')

    with pytest.raises(RegexError, match='Unmatched closing parenthesis'):
        RegexEnumerator(r'a)')

    with pytest.raises(RegexError, match='Unmatched opening parenthesis'):
        RegexEnumerator(r'(a')


def test_grammar_backreference():
    with pytest.raises(RegexError, match='Named back reference not found'):
        RegexEnumerator(r'\k<name>')

    with pytest.raises(RegexError, match='Positional back reference not found'):
        RegexEnumerator(r'\1')

    with pytest.raises(RegexError, match='Incomplete escape sequence'):
        RegexEnumerator('\\')

    with pytest.raises(RegexError, match='Invalid named back reference'):
        RegexEnumerator(r'\k')

    with pytest.raises(RegexError, match='Invalid named back reference'):
        RegexEnumerator(r'\k<')

    with pytest.raises(RegexError, match='Invalid named back reference'):
        RegexEnumerator(r'\ka')

    with pytest.raises(RegexError, match='Invalid named back reference'):
        RegexEnumerator(r'\k<>')


def test_grammar_escape_character():
    with pytest.raises(RegexError, match='Incomplete escape sequence'):
        RegexEnumerator('[\\')

    with pytest.raises(RegexError, match='Invalid ASCII escape character'):
        RegexEnumerator(r'\x')

    with pytest.raises(RegexError, match='Invalid ASCII escape character'):
        RegexEnumerator(r'\xh')

    with pytest.raises(RegexError, match='Invalid ASCII escape character 0'):
        RegexEnumerator(r'[\x0]')

    with pytest.raises(RegexError, match='Invalid unicode escape character'):
        RegexEnumerator(r'\u0')

    with pytest.raises(RegexError, match='Invalid unicode escape character'):
        RegexEnumerator(r'\un')

    with pytest.raises(RegexError, match='Unicode property not supported'):
        RegexEnumerator(r'\p{L}')


def test_grammar_charclass():
    with pytest.raises(RegexError, match='Unclosed character class'):
        RegexEnumerator(r'[')

    with pytest.raises(RegexError, match='Unclosed character class'):
        RegexEnumerator(r'[a')


def test_grammar_quantifiers():
    with pytest.raises(RegexError, match='Invalid quantifier'):
        RegexEnumerator(r'a{')

    with pytest.raises(RegexError, match='Invalid quantifier'):
        RegexEnumerator(r'a{a}')

    with pytest.raises(RegexError, match='Invalid quantifier'):
        RegexEnumerator(r'a{1')

    with pytest.raises(RegexError, match='Invalid quantifier'):
        RegexEnumerator(r'a{1 d')

    with pytest.raises(RegexError, match='Invalid quantifier'):
        RegexEnumerator(r'a{1, f')

    with pytest.raises(RegexError, match='Max length cannot be less than min length in quantifier'):
        RegexEnumerator(r'a{2,1}')

    with pytest.raises(RegexError, match='Invalid quantifier'):
        RegexEnumerator(r'a{1,2 d')
