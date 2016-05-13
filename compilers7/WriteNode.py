from InstructionNode import InstructionNode
import sys
class WriteNode(InstructionNode):

    def __init__(self, _next, expression):
        InstructionNode.__init__(self, _next)
        self.expression = expression

    def to_string(self):
        output = "expression: {0}\n".format(self.expression)
        sys.stdout.write(output+'\n')

    def visit(self, visitor):
        visitor.visitWriteNode(self)

    def int_visit(self, visitor):
        return visitor.visitWriteNode(self)

    def ncg_visit(self, visitor):
        return visitor.visitWriteNode(self)