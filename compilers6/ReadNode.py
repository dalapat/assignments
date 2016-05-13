from InstructionNode import InstructionNode
import sys

class ReadNode(InstructionNode):

    def __init__(self, _next, location):
        InstructionNode.__init__(self, _next)
        self.location = location

    def to_string(self):
        output = "location: {0}\n".format(self.location)
        sys.stdout.write(output+'\n')

    def visit(self, visitor):
        visitor.visitReadNode(self)

    def int_visit(self, visitor):
        return visitor.visitReadNode(self)