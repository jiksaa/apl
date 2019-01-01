from apl.parser import ast
from apl.tokens import token_type


class ProgrammingError(Exception):
    pass


class Interpreter(ast.ASTNodeVisitor):

    symbol_table = {}

    def __init__(self, parser):
        self.parser = parser

    def visit_binary_operator(self, node):
        op_type = node.operator.typename
        if op_type == token_type.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif op_type == token_type.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif op_type == token_type.MULT:
            return self.visit(node.left) * self.visit(node.right)
        elif op_type == token_type.DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_number(self, node):
        try:
            return int(node.value)
        except:
            return float(node.value)

    def visit_var(self, node):
        if node.var_name in self.symbol_table:
            return node.var_name
        raise ProgrammingError('Can\'t assign value to undeclared \'%s\' variable' % node.var_name)

    def visit_var_init(self, node):
        return node.var_name

    def visit_var_eval(self, node):
        try:
            return self.symbol_table[node.var_name]
        except KeyError:
            raise ProgrammingError('Variable %s doesn\'t exist' % node.var_name)

    def visit_assignation(self, node):
        self.symbol_table[self.visit(node.left_op)] = self.visit(node.right_op)

    def visit_program(self, node):
        instruction_list = node.instructions
        try:
            for instr in instruction_list:
                self.visit(instr)
        except Exception as ex:
            print(ex)
            return False
        return True

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
