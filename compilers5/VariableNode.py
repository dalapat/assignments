# how do we get the name of the variable rather than the type?
from ExpressionNode import ExpressionNode
from Integer import integerInstance

import sys
class VariableNode(ExpressionNode):

    def __init__(self, type, variable, var_name):
        ExpressionNode.__init__(self, type)
        self.variable = variable
        self.variable_name = var_name

    def to_string(self):
        # how to get name from variable object
        pass
