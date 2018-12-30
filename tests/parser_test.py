from apl.lexer import lexer
from apl.parser import parser

import code_test


lexer = lexer.Lexer(code_test.CODE)
parser = parser.Parser(lexer)

result_tree = parser.parse()

print(result_tree)
