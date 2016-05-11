from Entry import Entry

class Constant(Entry):
    """Initializes a constant object."""
    def __init__(self, ctype, value):
        self.type = ctype
        self.value = value
        self.kind = "Constant"

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_const(self)

    def __str__(self):
        return self.kind + "(" + str(self.type) + ": " + str(self.value) + ")"