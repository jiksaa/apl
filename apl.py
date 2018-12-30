from apl.lexer.lexer import Lexer, TokenMatchingError
from apl.parser.parser import Parser, ParsingError
from apl.interpreter.interpreter import Interpreter


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
            print(result)
        except TokenMatchingError as tk_match_err:
            print(tk_match_err)
        except ParsingError as parsing_err:
            print(parsing_err)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()
