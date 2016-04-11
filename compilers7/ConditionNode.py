import sys
from Node import Node

class ConditionNode(Node):

    def __init__(self, exp_left, exp_right, relation):
        self.exp_left = exp_left
        self.exp_right = exp_right
        self.relation = relation

    def to_string(self):
        output = "left: {0}\nright: {1}\nrelation: {2}".format(self.exp_left,
                                                               self.exp_right,
                                                               self.relation)
        sys.stdout.write(output+'\n')

    def visit(self, visitor):
        visitor.visitConditionNode(self)

    def int_visit(self, visitor):
        visitor.visitNode(self)