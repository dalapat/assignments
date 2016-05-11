# Eric Calder
# ecalder6@jhu.edu

# A token contains kind, value (if any), start position, and end position in
# the code. Tokens are produced by scanner after reading the input from user.
class Token:

    def __init__(self, kind, value, start_pos, end_pos):
        """Initializes a token with specified kind and position in the input."""
        self.kind = kind
        self.value = value
        self.start_pos = start_pos
        self.end_pos = end_pos

    def __str__(self):
        """Defines the string representation of a token"""
        if (self.kind == "INVALID"):
            # Invalid token does not have a string representation.

            return ''
        elif (self.value != None):
            # An identifier token with value.

            return (
                self.kind + "<" + str(self.value) + ">@" + "("
                + str(self.start_pos) + ", " + str(self.end_pos) + ")"
            )
        else:
            # A keyword token, which has no value.

            return (
                self.kind + "@" + "(" + str(self.start_pos) + ", "
                 + str(self.end_pos) + ")"
            )