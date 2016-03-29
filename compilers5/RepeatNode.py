from InstructionNode import InstructionNode

import sys
class RepeatNode(InstructionNode):

    def __init__(self, next, condition, instructions):
        InstructionNode.__init__(self, next)
        self.condition = condition
        self.instructions = instructions

    def to_string(self):
        output = "condition: {0}\ninstructions: {1}\n".format(self.condition, self.instructions)
        sys.stdout.write(output+'\n')