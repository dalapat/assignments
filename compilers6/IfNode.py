from InstructionNode import InstructionNode
import sys

class IfNode(InstructionNode):

    def __init__(self, _next, condition, instructions_true, instructions_false):
        InstructionNode.__init__(self, _next)
        self.condition = condition
        self.instructions_true = instructions_true
        self.instructions_false = instructions_false

    def to_string(self):
        output = "condition: {0}\ninstructions_true: {1}\n" \
                 "instructons_false: {2}".format(self.condition,
                                                 self.instructions_true,
                                                 self.instructions_false)
        sys.stdout.write(output+'\n')

    def visit(self, visitor):
        visitor.visitIfNode(self)

    def int_visit(self, visitor):
        return visitor.visitIf(self)