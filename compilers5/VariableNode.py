# how do we get the name of the variable rather than the type?
from ExpressionNode import ExpressionNode

import sys
class VariableNode(ExpressionNode):

    def __init__(self, type, variable):
        ExpressionNode.__init__(self, type)
        self.variable = variable

    def to_string(self):
        # how to get name from variable object
        pass
