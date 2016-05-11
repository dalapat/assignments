from Location import Location
from Invalid import Invalid

class Index(Location):
    def __init__(self, location, expression):
        super(Index, self).__init__()
        self.location = location
        self.expression = expression

        # If type is not array, set the type of location to be invalid.
        try:
            self.type = self.location.type.element_type
        except AttributeError:
            self.type = Invalid()

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_index(self)

    def __str__(self):
        return "Index"