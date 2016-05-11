from Type import Type

class Integer(Type):
    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_integer(self)

    def __str__(self):
        return "INTEGER"