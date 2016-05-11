from Expression import Expression

class Binary(Expression):
    def __init__(self, operator, left, right, btype):
        super(Binary, self).__init__("Binary")
        self.operator = operator
        self.left = left
        self.right = right
        self.type = btype

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_binary(self)

    def __str__(self):
        return (
            "Binary(" + str(self.left) + " " + str(self.operator) 
            + " " + str(self.right) + ")"
        )