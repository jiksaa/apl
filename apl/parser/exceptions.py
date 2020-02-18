class ParserError(Exception):
    """
    Generic Exception raised during Parsing process
    """
    pass


class SyntaxParseError(ParserError):
    """
    ParsingErrror indicating that an Syntax error occurs
    during parsing process
    """
    pass
