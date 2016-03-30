from ExpressionNode import ExpressionNode
from Integer import integerInstance

class IndexNode(ExpressionNode):

    def __init__(self, type, location, expression):
        ExpressionNode.__init__(self,  type)
        self.location = location
        self.expression = expression

    def to_string(self):
        pass