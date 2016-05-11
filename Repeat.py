from Instruction import Instruction

class Repeat(Instruction):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_repeat(self)

    def __str__(self):
        return "Repeat"