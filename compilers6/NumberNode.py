from ExpressionNode import ExpressionNode
from Integer import integerInstance

class NumberNode(ExpressionNode):

    def __init__(self, constant):
        # type should be integer in universe scope
        ExpressionNode.__init__(self, integerInstance)
        self.constant = constant

    def to_string(self):
        pass

    def visit(self, visitor):
        visitor.visitNumberNode(self)

    def int_visit(self, visitor):
        return visitor.visitNumberNode(self)

    #def int_visit(self, visitor):
    #    visitor.visitNode(self)

