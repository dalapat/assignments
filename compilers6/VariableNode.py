# how do we get the name of the variable rather than the type?
from ExpressionNode import ExpressionNode
from Integer import integerInstance

import sys
class VariableNode(ExpressionNode):

    def __init__(self, _type, variable, var_name):
        ExpressionNode.__init__(self, _type)
        self.variable = variable
        self.variable_name = var_name

    def to_string(self):
        sys.stdout.write("---\n")
        sys.stdout.write("VariableNode\n")
        sys.stdout.write("name: {0}\ntype: {1}".format(self.variable_name, self.type)+"\n")

    def visit(self, visitor):
        visitor.visitVariableNode(self)

    def int_visit(self, visitor):
        return visitor.visitVariableNode(self)
