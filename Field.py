from Variable import Variable

class Field(Variable):
    def __init__(self, ftype):
        """Initializes a field object."""
        self.type = ftype
        self.kind = "Field"

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_field(self)

    def __str__(self):
        return self.kind + "(" + str(self.type) + ")"