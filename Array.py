from Type import Type

class Array(Type):
    def __init__(self, element_type, length):
        """Initializes an Array object."""
        self.element_type = element_type
        self.length = length

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_array(self)

    def __str__(self):
        return (
            "Array length " + str(self.length) + " of " + str(self.element_type)
        )