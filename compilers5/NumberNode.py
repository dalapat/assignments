from ExpressionNode import ExpressionNode

class NumberNode(ExpressionNode):

    def __init__(self, type, constant):
        ExpressionNode.__init__(self, type)
        self.constant = constant

    def to_string(self):
        pass