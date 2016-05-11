from Instruction import Instruction

class Write(Instruction):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_write(self)

    def __str__(self):
        return "Write"