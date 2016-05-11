from Type import Type

class Record(Type):
    def __init__(self, scope):
        """Initializes a record object with a scope."""
        self.scope = scope

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_record(self)

    def __str__(self):
        return "Record"