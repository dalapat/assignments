from InstructionNode import InstructionNode

import sys

class AssignNode(InstructionNode):

    def __init__(self, _next, location, expression):
        InstructionNode.__init__(self, _next)
        self.location = location
        self.expression = expression

    def to_string(self):
        output = "location: {0}\nexpression: {1}\n".format(self.location, self.expression)
        sys.stdout.write(output+'\n')

    def visit(self, visitor):
        visitor.visitAssignNode(self)

    def int_visit(self, visitor):
        visitor.visitAssignNode(self)

    def ncg_visit(self, visitor):
        return visitor.visitAssignNode(self)

    #def int_visit(self, visitor):
    #    visitor.visitNode(self)
