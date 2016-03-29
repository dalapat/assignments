from ExpressionNode import ExpressionNode

import sys
class BinaryNode(ExpressionNode):

    def __init__(self, operator, left, right, type):
        ExpressionNode.__init__(self, type)
        self.operator = operator
        self.exp_left = left
        self.exp_right = right

    def to_string(self):
        output = "operator: {0}\nexpleft: {1}\nexpright: {2}".format(self.operator,
                                                               self.exp_left,
                                                               self.exp_right)
        sys.stdout.write(output+'\n')

