from . import ast
from apl.tokens import token_type


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self, expected):
        raise ParsingError('Syntax error: expecting %s and found %s %s' % (expected, self.current_token.typename, self.current_token.value))

    def consume(self, token_type):
        if self.current_token.typename == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    def factor(self):
        """
        factor := NUMBER | OPEN_PAR expr CLOSING_PAR

        :return: factor AST Node
        """
        token = self.current_token
        if token.typename == token_type.NUMBER:
            self.consume(token_type.NUMBER)
            return ast.Number(token)
        elif token.typename == token_type.OPEN_PAR:
            self.consume(token_type.OPEN_PAR)
            expr_node = self.expr()
            self.consume(token_type.CLOSING_PAR)
            return expr_node

    def term(self):
        """
        term := factor ((MULT | DIV) factor)*

        :return: term AST node
        """
        node = self.factor()
        while self.current_token.typename in (token_type.MULT, token_type.DIV):
            operator_token = self.current_token
            if operator_token.typename == token_type.MULT:
                self.consume(token_type.MULT)
            elif operator_token.typename == token_type.DIV:
                self.consume(token_type.DIV)

            node = ast.BinaryOperator(operator=operator_token, left=node, right=self.factor())
        return node

    def expr(self):
        """
        expr := term ((PLUS | MINUS) term)*

        :return: expr AST node
        """
        node = self.term()
        while self.current_token.typename in (token_type.PLUS, token_type.MINUS):
            operator_token = self.current_token
            if operator_token.typename == token_type.PLUS:
                self.consume(token_type.PLUS)
            elif operator_token.typename == token_type.MINUS:
                self.consume(token_type.MINUS)

            node = ast.BinaryOperator(operator=operator_token, left=node, right=self.term())
        return node

    def parse(self):
        return self.expr()
