from . import regex_type as regex
from . import token_type

"""
TOKEN REGULAR EXPRESSIONS
"""
TOKEN_REGEX = [
    (token_type.SPACE, regex.SKIP, ' '),
    (token_type.TAB, regex.SKIP, '\t'),
    (token_type.OPEN_PAR, regex.SINGLE_CHAR, '('),
    (token_type.CLOSING_PAR, regex.SINGLE_CHAR, ')'),
    (token_type.PLUS, regex.SINGLE_CHAR, '+'),
    (token_type.MINUS, regex.SINGLE_CHAR, '-'),
    (token_type.MULT, regex.SINGLE_CHAR, '*'),
    (token_type.DIV, regex.SINGLE_CHAR, '/'),
    (token_type.EQUAL, regex.SINGLE_CHAR, '='),
    (token_type.NUMBER, regex.PATTERN, '[0-9]+(\.[0-9]+)?'),
    (token_type.IDENTIFIER, regex.PATTERN, '_*[a-zA-Z0-9]*'),
    (token_type.STRING, regex.PATTERN, '\".*\"')
]


class Token:
    """
    Represent an token identified by a lexer
    """
    typename = str()
    value = str()

    def __init__(self, typename, value):
        self.typename = typename
        self.value = value

    def __str__(self):
        return 'Token(%s, \'%s\')' % (self.typename, self.value)
