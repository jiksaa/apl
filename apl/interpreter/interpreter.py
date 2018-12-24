from apl.parser import ast
from apl.tokens import token_type


class Interpreter(ast.ASTNodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinaryOperator(self, node):
        op_type = node.operator.typename
        if op_type == token_type.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif op_type == token_type.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif op_type == token_type.MULT:
            return self.visit(node.left) * self.visit(node.right)
        elif op_type == token_type.DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Number(self, node):
        try:
            return int(node.value)
        except:
            return float(node.value)

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)