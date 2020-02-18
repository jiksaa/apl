import re


class NodeVisitor:
    def visit(self, node):
        camel_case_split = re.sub('(?!^)([A-Z][a-z]+)', r' \1', type(node).__name__).split()
        method_name = 'visit_%s' % '_'.join(camel_case_split).lower()
        visitor = getattr(self, method_name, self.default_visit)
        return visitor(node)

    def default_visit(self, node):
        raise Exception('No existing visitor method for %s' % type(node).__name__)
