from Expression import Expression

class Number(Expression):
    def __init__(self, entry):
        self.entry = entry
        self.type = self.entry.type

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_number(self)

    def __str__(self):
        return "Number(" + str(self.entry) + ")"