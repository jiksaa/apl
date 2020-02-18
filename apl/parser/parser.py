from apl.ast import ast
from apl.tokens import types

from apl.parser.exceptions import SyntaxParseError


class Parser:
    """
    This class define an APL parser instance.
    A Parser instance is defined by:
        - Lexer: a lexer instance that will generate token stream
        - Token: current token that the parser process
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self, expected):
        """
        Method raising error when the parser instance find an unexpected token

        :param expected: Token expected
        :type expected: apl.tokens.Tokens
        :return: None
        :raise ParsingError
        """
        raise SyntaxParseError('Syntax error: expecting {} and found {} {}'.format(
            expected,
            self.current_token.typename,
            self.current_token.value
        ))

    def consume(self, t_type):
        """
        Consume a token of the given `t_type` from the lexer token stream

        :param t_type: token type
        :type t_type: str()
        :return: None
        :rtype: None
        :raise: ParsingError() if the consumed token type does not match the given `t_type`
        """
        if self.current_token.typename == t_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(t_type)

    def factor(self):
        """
        Generate a `factor` from the Lexer token stream.
        A factor is defined by the following rule:

        factor := NUMBER | OPEN_PAR expr CLOSING_PAR | IDENTIFIER

        :return: `factor` AST Node
        :raise: ParsingError when token stream was not able to generate a `factor`
        """
        token = self.current_token
        if token.typename == types.NUMBER:
            self.consume(types.NUMBER)
            return ast.Number(token)
        elif token.typename == types.OPEN_PAR:
            self.consume(types.OPEN_PAR)
            expr_node = self.expr()
            self.consume(types.CLOSING_PAR)
            return expr_node
        elif token.typename == types.IDENTIFIER:
            self.consume(types.IDENTIFIER)
            return ast.VarEval(token)
        else:
            self.error(types.NUMBER)

    def term(self):
        """
        Generate a `term` AST Node from the Lexer token stream.
        A `term` is defined by the following rule:

        term := factor ((MULT | DIV) factor)*

        :return: `term` AST Node
        :raise: ParsingError if the token stream does not contains a `term`
        """
        node = self.factor()
        while self.current_token.typename in (types.MULT, types.DIV):
            operator_token = self.current_token
            if operator_token.typename == types.MULT:
                self.consume(types.MULT)
            elif operator_token.typename == types.DIV:
                self.consume(types.DIV)

            node = ast.BinaryOperator(operator=operator_token, left=node, right=self.factor())
        return node

    def expr(self):
        """
        expr := term ((PLUS | MINUS) term)*

        :return: expr AST node
        """
        node = self.term()
        while self.current_token.typename in (types.PLUS, types.MINUS):
            operator_token = self.current_token
            if operator_token.typename == types.PLUS:
                self.consume(types.PLUS)
            elif operator_token.typename == types.MINUS:
                self.consume(types.MINUS)

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
        if self.current_token.typename == types.WORD_VAR:
            self.consume(types.WORD_VAR)
            var_name_token = self.current_token
            self.consume(types.IDENTIFIER)
            return ast.VarInit(var_name_token)
        else:
            var_name_token = self.current_token
            self.consume(types.IDENTIFIER)
            return ast.Var(var_name_token)

    def assign(self):
        """
        assign := left_op EQUAL right_op

        :return:
        """
        left_op = self.left_op()
        self.consume(types.EQUAL)
        right_opt = self.right_op()
        return ast.Assignation(left_op, right_opt)

    def instruction(self):
        """
        instruction := (assign | [future instruction type]) TERMINATOR

        :return:
        """
        instruction = self.assign()
        self.consume(types.TERMINATOR)
        return instruction

    def program(self):
        """
        program := (instruction)*

        :return:
        """
        instructions = []
        while self.current_token.typename != types.EOF:
            instructions.append(self.instruction())
        return ast.Program(instructions)

    def parse(self):
        tree = self.program()
        if self.current_token.typename != types.EOF:
            self.error(types.EOF)
        return tree
