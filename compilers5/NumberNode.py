from ExpressionNode import ExpressionNode
from Integer import integerInstance

class NumberNode(ExpressionNode):

    def __init__(self, constant):
        # type should be integer in universe scope
        ExpressionNode.__init__(self, integerInstance)
        self.constant = constant

    def to_string(self):
        pass

