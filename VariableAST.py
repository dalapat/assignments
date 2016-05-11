from Location import Location

class VariableAST(Location):
    def __init__(self, name, variable):
        self.name = name
        self.variable = variable
        self.type = self.variable.type

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_variableAST(self)

    def __str__(self):
        return "Variable(" + str(self.name) + ", " + str(self.variable) + ")"