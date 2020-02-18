from apl.lexer import lexer

from . import code_test


token_list, error_msg = lexer.Lexer.tokenize(code_test.CODE)
for token in token_list:
    print(token)
