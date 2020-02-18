from apl.lexer import Lexer
from apl.lexer.exceptions import LexerError

from apl.parser import Parser
from apl.parser.exceptions import ParserError

from apl.interpreter import Interpreter
from apl.interpreter.exceptions import InterpreterError


def main():
    while True:
        try:
            text = input('apl> ')
        except EOFError:
            break
        if not text:
            continue

        if text == "exit":
            break
        try:
            apl_lexer = Lexer(text)
            apl_parser = Parser(apl_lexer)
            apt_interpreter = Interpreter(apl_parser)
            result = apt_interpreter.interpret()
            print(apt_interpreter.symbol_table)
            print(result)
        except LexerError as tk_match_err:
            print(tk_match_err)
        except ParserError as parsing_err:
            print(parsing_err)
        except InterpreterError as int_err:
            print(int_err)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()
