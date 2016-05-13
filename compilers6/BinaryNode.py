from ExpressionNode import ExpressionNode
# is type of BinaryNode integer?
from Integer import integerInstance

import sys
class BinaryNode(ExpressionNode):

    def __init__(self, operator, left, right):
        ExpressionNode.__init__(self, integerInstance)
        self.operator = operator
        self.exp_left = left
        self.exp_right = right

    def to_string(self):
        sys.stdout.write("---\n")
        sys.stdout.write("BinaryNode\n")
        sys.stdout.write("operator: {0}\nexpleft: {1}\nexpright: {2}".format(self.operator,
                                                               self.exp_left.to_string(),
                                                               self.exp_right.to_string())+'\n')
        # sys.stdout.write(output+'\n')

    def visit(self, visitor):
        visitor.visitBinaryNode(self)

    def int_visit(self, visitor):
        return visitor.visitBinaryNode(self)

