class AST:
    pass


class BinaryOperator(AST):
    def __init__(self, operator, left, right):
        self.token = self.operator = operator
        self.left = left
        self.right = right


class Number(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class ASTNodeVisitor:
    def visit(self, node):
        method_name = 'visit_%s' % type(node).__name__
        visitor = getattr(self, method_name, self.default_visit)
        return visitor(node)

    def default_visit(self, node):
        raise Exception('No existing visitor method for %s' % type(node).__name__)