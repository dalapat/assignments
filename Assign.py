from Instruction import Instruction

class Assign(Instruction):
    def __init__(self, location, expression):
        self.location = location
        self.expression = expression

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_assign(self)

    def __str__(self):
        return "Assign"