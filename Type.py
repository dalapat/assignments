from Entry import Entry

class Type(Entry):
    def __init__(self):
        """Initializes a type object."""
        self.kind = "Type"

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_type(self)

    def __str__(self):
        return self.kind