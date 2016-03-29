from InstructionNode import InstructionNode
import sys
class WriteNode(InstructionNode):

    def __init__(self, next, expression):
        InstructionNode.__init__(self, next)
        self.expression = expression

    def to_string(self):
        output = "expression: {0}\n".format(self.expression)
        sys.stdout.write(output+'\n')