# Eric Calder
# ecalder6@jhu.edu

from Token import *

# Currently all custom exceptions are defined here. Each exception has a string
# representation to be easily printed.
class Error(Exception):
    """Base class for exceptions in this module."""
    # Some code are from the Python Documentation on Exceptions.
    pass

class ArgvError(Error):
    def __init__(self):
        """Initializes an argument error with error message."""

        self.message = "error: the inputted option(s) is invalid."

    def __str__(self):
        """The string representation is defined in init."""

        return repr(self.message)

class ScannerAllError(Error):
    def __init__(self):
        """Initializes a scanner error with error message."""

        self.message = "error: cannot call all after calling next"

    def __str__(self):
        """The string representation is defined in init."""

        return repr(self.message)

class ScannerInvalidInputError(Error):
    def __init__(self, code, pos):
        """Initializes an invalid input error with error message containing
        the position of the invalid character."""

        self.message = (
            "error: the input " + str(code) + " at position "
             + str(pos) + " is invalid"
        )

    def __str__(self):
        """The string representation is defined in init."""

        return repr(self.message)


class ScannerInvalidCommentNestingError(Error):
    def __init__(self, start_pos):
        """Initializes an invalid comment error with error message containing
        the position of the invalid comment's start symbol."""

        self.message = (
            "error: the comment starting at " + str(start_pos) + " is invalid"
        )
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class ParserInvalidKindError(Error):
    def __init__(self, kind, token):
        """Initializes an invalid kind error with error message containing
        the expected kind and the invalid token."""

        self.message = (
            "error: expected kind " + str(kind) + ", but encountered a "
            + str(token)
        )
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class DuplicateDeclarationError(Error):
    def __init__(self, dup):
        """Initializes a duplicate declaration error with error message
        containing the duplicate."""

        self.message = "error: duplicate declaration of " + str(dup)
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class IdentifierUsedBeforeDeclared(Error):
    def __init__(self, identifier):
        """Initializes an identifier used before declared error with the
        error message containing the identifier."""

        self.message = (
            "error: " + str(identifier) + " is used before it's declared."
        )
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class ProgramNameMismatch(Error):
    def __init__(self, begin, end):
        """Initializes an program name mismatch error with the error message
        containing the two different program names."""

        self.message = (
            "error: the identifier after PROGRAM: " + str(begin)
            + " does not match the identifier after END: " + str(end)
        )
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class IdentifierDoesNotDenoteType(Error):
    def __init__(self, identifier, entry):
        """Initializes an identifier does not denote type error with the error
        message containing the identifier and the entry it denotes."""

        self.message = (
            "error: the identifier: " + str(identifier)
            + " denotes a " + str(entry) + " instead of a type."
        )
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class EntryNotFoundInSymbolTable(Error):
    def __init__(self, identifier):
        """Initializes an entry not found in symbol table error with the error
        message containing the identifier of the entry."""

        self.message = (
            "error: the identifier: " + str(identifier)
            + " has not been declared before use."
        )
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class InvalidArraySize(Error):
    def __init__(self, size, identifier):
        """Initializes an invalid array size error with the error
        message containing the invalid size."""

        self.message = (
            "error: " + str(size) + " is not a valid array size at "
            + str(identifier) + "."
        )
        
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class InvalidConstantValue(Error):
    def __init__(self, value, identifier):
        """Initializes an invalid constant value error with the error
        message containing the invalid value."""

        self.message = (
            "error: " + str(value) + " is not a valid array size at "
            + str(identifier) + "."
        )
        
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class InvalidArithmeticOperation(Error):
    def __init__(self, variable, identifier):
        """Initializes an invalid arithmetic operation error with the error
        message containing the invalid variable."""

        self.message = (
            "error: " + str(variable) + " at " + str(identifier) + " is not an "
            "INTEGER and thus cannot be in an arithmetic operation."
        )
        
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class InvalidDesignator(Error):
    def __init__(self, designator, identifier):
        """Initializes an invalid designator error with the error
        message containing the invalid designator."""

        self.message = (
            "error: " + str(designator) + " at " + str(identifier) + " is not a"
            + " valid designator."
        )
        
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class InvalidAssignment(Error):
    def __init__(self, left, right, identifier):
        """Initializes an invalid assignment error with the error
        message containing the left and right side of the assignment."""

        self.message = (
            "error: Invalid assignment. " + str(left) + " cannot have the value"
            " of " + str(right) + " at " + str(identifier) + "."        
        )
        
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class InvalidCondition(Error):
    def __init__(self, left, right, identifier):
        """Initializes an invalid condition error with the error
        message containing the left and right side of the condition."""

        self.message = (
            "error: Invalid condition. " + str(left) + " cannot be compared to " 
            + str(right) + " at " + str(identifier) + "."        
        )
        
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class InvalidWrite(Error):
    def __init__(self, expression, identifier):
        """Initializes an invalid write error with the error
        message containing the invalid expression."""

        self.message = (
            "error: Invalid write. " + str(expression) + " at "
            + str(identifier) + " cannot be written." 
        )
        
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class InvalidRead(Error):
    def __init__(self, location, identifier):
        """Initializes an invalid read error with the error
        message containing the invalid location."""

        self.message = (
            "error: Invalid read. " + str(location) + " at " + str(identifier)
            + " cannot be read." 
        )
        
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class InvalidArray(Error):
    def __init__(self, location, identifier):
        """Initializes an invalid array error with the error
        message containing the invalid array."""

        self.message = (
            "error: Invalid array. " + str(location) + " at " + str(identifier)
            + " is not an array variable." 
        )

    def __str__(self):
        """The string representation is defined in init."""

        return repr(self.message)

class InvalidRecord(Error):
    def __init__(self, location, identifier):
        """Initializes an invalid record error with the error
        message containing the invalid record."""

        self.message = (
            "error: Invalid record. " + str(location) + " at " + str(identifier)
            + " is not a record variable." 
        )

    def __str__(self):
        """The string representation is defined in init."""

        return repr(self.message)

class DivideByZero(Error):
    def __init__(self, identifier):
        """Initializes an divide by 0 error with the error
        message containing the token of 0."""

        self.message = "error: divide by 0 for token " + str(identifier) + "."
        
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class InvalidInputForRead(Error):
    def __init__(self, invalid, token):
        """Initializes an invalid input for read error with the error
        message containing the invalid input."""

        # Remove the line break in input
        invalid = invalid.replace("\n", "")

        self.message = (
            "error: invalid input " + str(invalid) + " at "
            + str(token) + "."
        )
        
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)

class InvalidArrayIndex(Error):
    def __init__(self, index, size, token):
        """Initializes an invalid array index error with the error
        message containing the invalid index."""

        self.message = (
            "error: " + str(index) + " is not a valid array index at "
            + str(token) + ". The index for this array must be in (0, "
            + str(size - 1) + ")."
        )
        
    def __str__(self):
        """The string representation is defined in init."""
        
        return repr(self.message)