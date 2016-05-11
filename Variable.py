from Entry import Entry

class Variable(Entry):
    def __init__(self, vtype):
        """Initializes a variable object."""
        self.type = vtype
        self.kind = "Variable"

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_var(self)

    def __str__(self):
        return self.kind + "(" + str(self.type) + ")"