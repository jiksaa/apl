from apl.tokens import regex
from apl.tokens import types

"""
TOKEN REGULAR EXPRESSIONS
"""
TOKEN_REGEX = [
    (types.SPACE, regex.SKIP, ' '),
    (types.TAB, regex.SKIP, '\t'),
    (types.OPEN_PAR, regex.SINGLE_CHAR, '('),
    (types.CLOSING_PAR, regex.SINGLE_CHAR, ')'),
    (types.PLUS, regex.SINGLE_CHAR, '+'),
    (types.MINUS, regex.SINGLE_CHAR, '-'),
    (types.MULT, regex.SINGLE_CHAR, '*'),
    (types.DIV, regex.SINGLE_CHAR, '/'),
    (types.EQUAL, regex.SINGLE_CHAR, '='),
    (types.TERMINATOR, regex.SINGLE_CHAR, ';'),
    (types.WORD_VAR, regex.PATTERN, 'var'),
    (types.NUMBER, regex.PATTERN, '[0-9]+(\.[0-9]+)?'),
    (types.IDENTIFIER, regex.PATTERN, '[a-zA-Z0-9_]*'),
    (types.STRING, regex.PATTERN, '\".*\"'),
]


class Token:
    """
    Represent a token identified by a lexer.
    Toke instance is defined by:
        - a typename: string()
        - a value: string()
    """
    typename = str()
    value = str()

    def __init__(self, typename, value):
        self.typename = typename
        self.value = value

    def __str__(self):
        return 'Token(%s, \'%s\')' % (self.typename, self.value)
