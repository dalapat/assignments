from Node import Node

class Expression(Node):
    def __init__(self, expression_type):
        super(Expression, self).__init__()
        self.type = expression_type

    def __str__(self):
        return "Expression"