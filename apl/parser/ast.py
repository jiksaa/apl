class AST:
    pass


class BinaryOperator(AST):
    def __init__(self, operator, left, right):
        self.token = self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return 'ast.binary.operator<%s, %s, %s>' % (self.left, self.operator, self.right)


class Number(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __str__(self):
        return 'ast.number<%s>' % self.value


class Program(AST):
    def __init__(self, instructions):
        self.instructions = instructions

    def __str__(self):
        return 'ast.program<%s>' % ', '.join([str(instr) for instr in self.instructions])


class Instruction(AST):
    pass


class Assignation(Instruction):
    def __init__(self, left_op, right_op):
        self.left_op = left_op
        self.right_op = right_op

    def __str__(self):
        return 'ast.assignation<%s, %s>' % (self.left_op, self.right_op)


class Var(AST):
    def __init__(self, token):
        self.token = self.var_name = token

    def __str__(self):
        return 'ast.var<%s>' % self.var_name.value


class VarInit(Var):
    def __str__(self):
        return 'ast.var.init<%s>' % self.var_name.value

class VarEval(Var):
    def __str__(self):
        return 'ast.var.eval<%s>' % self.var_name.value


class ASTNodeVisitor:
    def visit(self, node):
        method_name = 'visit_%s' % type(node).__name__
        visitor = getattr(self, method_name, self.default_visit)
        return visitor(node)

    def default_visit(self, node):
        raise Exception('No existing visitor method for %s' % type(node).__name__)
