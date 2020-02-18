class InterpreterError(Exception):
    """
    Generic Exception raised in case of error during interpretation process
    """
    pass


class ProgrammingError(InterpreterError):
    """
    Exception describing a programming error
    """
    pass


class UndeclaredVariableError(ProgrammingError):
    """
    Exception raised when a variable is used before it has been declared
    """
    pass
