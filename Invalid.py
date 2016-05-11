# Eric Calder
# ecalder6@jhu.edu

from Type import Type

# An invalid type that is used for errors.
class Invalid(Type):
    def accept(self, visitor):
        """Use Visitor to produce output. For debugging purposes only."""
        return visitor.visit_invalid(self)

    def __str__(self):
        return "INVALID"