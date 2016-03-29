from ExpressionNode import ExpressionNode

class IndexNode(ExpressionNode):

    def __init__(self, type, location, expression):
        ExpressionNode.__init__(self, type)
        self.location = location
        self.expression = expression

    def to_string(self):
        pass