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
        factor := NUMBER | OPEN_PAR expr CLOSING_PAR | IDENTIFIER

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
        elif token.typename == token_type.IDENTIFIER:
            self.consume(token_type.IDENTIFIER)
            return ast.VarEval(token)
        else:
            self.error(token_type.NUMBER)

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

    def right_op(self):
        """
        right_op := expr

        :return:
        """
        return self.expr()

    def left_op(self):
        """
        left_op := (VAR)? IDENTIFIER

        :return:
        """
        if self.current_token.typename == token_type.WORD_VAR:
            self.consume(token_type.WORD_VAR)
            var_name_token = self.current_token
            self.consume(token_type.IDENTIFIER)
            return ast.VarInit(var_name_token)
        else:
            var_name_token = self.current_token
            self.consume(token_type.IDENTIFIER)
            return ast.Var(var_name_token)

    def assign(self):
        """
        assign := left_op EQUAL right_op

        :return:
        """
        left_op = self.left_op()
        self.consume(token_type.EQUAL)
        right_opt = self.right_op()
        return ast.Assignation(left_op, right_opt)

    def instruction(self):
        """
        instruction := (assign | [future instruction type]) TERMINATOR

        :return:
        """
        instruction = self.assign()
        self.consume(token_type.TERMINATOR)
        return instruction

    def program(self):
        """
        program := (instruction)*

        :return:
        """
        instructions = []
        while self.current_token.typename != token_type.EOF:
            instructions.append(self.instruction())
        return ast.Program(instructions)

    def parse(self):
        tree = self.program()
        if self.current_token.typename != token_type.EOF:
            self.error(token_type.EOF)
        return tree
