from ExpressionNode import ExpressionNode

class FieldNode(ExpressionNode):

    def __init__(self, type, location, variable):
        ExpressionNode.__init__(self, type)
        self.location = location
        self.variable = variable

    def to_string(self):
        pass

    def visit(self, visitor):
        visitor.visitFieldNode(self)