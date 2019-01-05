from unittest import TestCase
from unittest.mock import MagicMock
import logging as log

from apl.tokens.tokens import Token
from apl.tokens.token_type import *
from apl.parser import parser
from apl.parser import ast
from apl.interpreter import interpreter


log.basicConfig(
    format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s",
    level=log.INFO
)


class TestInterpreter(TestCase):

    def get_mock_parser(self, next_token_result, parse_result):
        mock_lexer = MagicMock()
        mock_lexer.get_next_token = MagicMock(return_value=next_token_result)
        mocked_parser = parser.Parser(mock_lexer)
        mocked_parser.parse = MagicMock(return_value=parse_result)
        return mocked_parser

    def test_visit_binary_operator(self):
        log.info('Starting test...')
        next_token_val = Token(EOF, '')
        ast_result = ast.BinaryOperator(
            Token(PLUS, '+'),
            ast.Number(Token(NUMBER, '45')),
            ast.BinaryOperator(
                Token(MULT, '*'),
                ast.Number(Token(NUMBER, '3')),
                ast.Number(Token(NUMBER, '3'))
            )
        )

        mocked_parser = self.get_mock_parser(next_token_val, ast_result)

        apl_interpreter = interpreter.Interpreter(mocked_parser)
        apl_interpreter.symbol_table = {}
        result = apl_interpreter.interpret()

        self.assertEqual(result, 54, 'Test failed on BinOp visit')

    def test_visit_number(self):
        log.info('Starting test...')
        next_token_val = Token('EOF', '')
        ast_result = ast.Number(Token('NUMBER', '100'))

        mocked_parser = self.get_mock_parser(next_token_val, ast_result)

        apl_interpreter = interpreter.Interpreter(mocked_parser)
        apl_interpreter.symbol_table = {}
        result = apl_interpreter.interpret()

        self.assertEqual(result, 100, 'Result value should be equal')

    def test_visit_var(self):
        log.info('Starting test...')
        # Mock return values
        next_token_return_val = Token(EOF, '')
        parse_return_val = ast.Var(Token(IDENTIFIER, 'expect_var_name'))
        expected_result = 'expect_var_name'

        mocked_parser = self.get_mock_parser(next_token_return_val, parse_return_val)

        apl_interpreter = interpreter.Interpreter(mocked_parser)
        apl_interpreter.symbol_table = {
            expected_result: 0
        }
        result = apl_interpreter.interpret()

        self.assertEqual(result, expected_result)

    def test_visit_var_init(self):
        log.info('Starting test...')
        # Mock return values
        next_token_return_val = Token(EOF, '')
        parse_return_val = ast.VarInit(Token(IDENTIFIER, 'expect_var_name'))
        expected_result = 'expect_var_name'

        mocked_parser = self.get_mock_parser(next_token_return_val, parse_return_val)

        apl_interpreter = interpreter.Interpreter(mocked_parser)
        result = apl_interpreter.interpret()

        self.assertEqual(result, expected_result)

    def test_visit_var_eval(self):
        log.info('Starting test...')
        # Mock return values
        next_token_return_val = Token(EOF, '')
        parse_return_val = ast.VarEval(Token(IDENTIFIER, 'expect_var_name'))
        expected_result = 0

        mocked_parser = self.get_mock_parser(next_token_return_val, parse_return_val)

        apl_interpreter = interpreter.Interpreter(mocked_parser)
        apl_interpreter.symbol_table = {
            'expect_var_name': 0
        }
        result = apl_interpreter.interpret()

        self.assertEqual(result, expected_result)

    def test_visit_assignation(self):
        log.info('Starting test...')
        next_token_val = Token(EOF, '')
        ast_result = ast.Assignation(
            ast.VarInit(Token(IDENTIFIER, 'var_name')),
            ast.Number(Token(NUMBER, '0'))
        )
        expected = {
            'var_name': 0
        }

        mocked_parser = self.get_mock_parser(next_token_val, ast_result)

        apl_interpreter = interpreter.Interpreter(mocked_parser)
        apl_interpreter.symbol_table = {}
        apl_interpreter.interpret()

        self.assertDictEqual(apl_interpreter.symbol_table, expected)

    def test_visit_program(self):
        log.info('Starting test...')
        next_token_val = Token(EOF, '')
        ast_result = ast.Program([
            ast.Assignation(
                ast.VarInit(Token(IDENTIFIER, 'var_name')),
                ast.Number(Token(NUMBER, '0'))
            ),
            ast.Assignation(
                ast.Var(Token(IDENTIFIER, 'var_name')),
                ast.BinaryOperator(
                    Token(PLUS, '+'),
                    ast.VarEval(Token(IDENTIFIER, 'var_name')),
                    ast.Number(Token(NUMBER, '1'))
                )
            )
        ])
        expected = {
            'var_name': 1
        }

        mocked_parser = self.get_mock_parser(next_token_val, ast_result)

        apl_interpreter = interpreter.Interpreter(mocked_parser)
        apl_interpreter.symbol_table = {}
        apl_interpreter.interpret()

        self.assertDictEqual(apl_interpreter.symbol_table, expected)
