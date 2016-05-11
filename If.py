from Instruction import Instruction

class If(Instruction):
    def __init__(self, condition, instructions_true, instructions_false):
        self.condition = condition
        self.instructions_true = instructions_true
        self.instructions_false = instructions_false

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_if(self)

    def __str__(self):
        return "If"