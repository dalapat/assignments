from InstructionNode import InstructionNode

import sys

class AssignNode(InstructionNode):

    def __init__(self, next, location, expression):
        InstructionNode.__init__(self, next)
        self.location = location
        self.expression = expression

    def to_string(self):
        output = "location: {0}\nexpression: {1}\n".format(self.location, self.expression)
        sys.stdout.write(output+'\n')