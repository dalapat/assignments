from Node import Node

class ExpressionNode(Node):

    def __init__(self, type):
        self.type = type

    def to_string(self):
        pass

    def int_visit(self, visitor):
        visitor.visitNode(self)