from InstructionNode import InstructionNode

import sys
class RepeatNode(InstructionNode):

    def __init__(self, _next, condition, instructions):
        InstructionNode.__init__(self, _next)
        self.condition = condition
        self.instructions = instructions

    def to_string(self):
        output = "condition: {0}\ninstructions: {1}\n".format(self.condition, self.instructions)
        sys.stdout.write(output+'\n')

    def visit(self, visitor):
        visitor.visitRepeatNode(self)

    #def int_visit(self, visitor):
    #    visitor.visitNode()

    def int_visit(self, visitor):
        return visitor.visitRepeatNode(self)

    def ncg_visit(self, visitor):
        return visitor.visitRepeatNode(self)