
class LexerError(Exception):
    """
    Generic exception raised by Lexer
    """
    pass


class TokenMatchingError(LexerError):
    """
    Exception indicating that no matching token could be found for
    the given string
    """
    pass
