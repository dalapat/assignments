from Location import Location

class FieldAST(Location):
    def __init__(self, location, variable):
        self.location = location
        self.variable = variable
        self.type = self.variable.type

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_fieldAST(self)

    def __str__(self):
        return "Field"