# Eric Calder
# ecalder6@jhu.edu

from Constant import Constant
from Variable import Variable
from Type import Type
from Integer import Integer
from Array import Array
from Record import Record
from Scope import Scope
from Invalid import Invalid

# Visitor that creates the text output for symbol table
class TextVisitor:
    def __init__(self):
        """Initializes the text visitor"""
        self.indentation = ""

    def display(self):
        """called by the Parser."""

        output = self.program_scope.accept(self)

        print(output)

    def visit_scope(self, scope):
        """Print everything in a scope."""
        output = self.indentation + "SCOPE BEGIN\n"
        self.indentation += "  "

        for name in sorted(scope.table.keys()):
            output += self.indentation + str(name) + " =>\n"
            self.indentation += "  "
            output += scope.table[name].accept(self)
            self.indentation = self.indentation[:-2]

        self.indentation = self.indentation[:-2]
        output += self.indentation + "END SCOPE\n"

        return output

    def visit_const(self, const):
        """Print const with type and value."""
        output = self.indentation + "CONST BEGIN\n"
        self.indentation += "  "
        output += self.indentation + "type:\n"

        self.indentation += "  "
        output += const.type.accept(self)
        self.indentation = self.indentation[:-2]

        output += self.indentation + "value:\n"

        self.indentation += "  "
        output += self.indentation + str(const.value) + "\n"
        self.indentation = self.indentation[:-2]

        self.indentation = self.indentation[:-2]
        output += self.indentation + "END CONST\n"

        return output

    def visit_var(self, var):
        """Print var with type."""
        output = self.indentation + "VAR BEGIN\n"
        self.indentation += "  "
        output += self.indentation + "type:\n"

        self.indentation += "  "
        output += var.type.accept(self)
        self.indentation = self.indentation[:-2]
                
        self.indentation = self.indentation[:-2]
        output += self.indentation + "END VAR\n"

        return output

    def visit_field(self, field):
        """Print field with type."""
        output = self.indentation + "VAR BEGIN\n"
        self.indentation += "  "
        output += self.indentation + "type:\n"

        self.indentation += "  "
        output += field.type.accept(self)
        self.indentation = self.indentation[:-2]
                
        self.indentation = self.indentation[:-2]
        output += self.indentation + "END VAR\n"

        return output

    def visit_integer(self, integer):
        """Print the integer type."""
        output = self.indentation + str(integer) + "\n"

        return output

    def visit_invalid(self, invalid):
        """Print the invalid type (for debugging purpose only)."""
        output = self.indentation + str(invalid) + "\n"

        return output

    def visit_array(self, array):
        """Print the array with length and element type."""
        output = self.indentation + "ARRAY BEGIN\n"
        self.indentation += "  "
        output += self.indentation + "type:\n"

        self.indentation += "  "
        output += array.element_type.accept(self)
        self.indentation = self.indentation[:-2]

        output += self.indentation + "length:\n"

        self.indentation += "  "
        output += self.indentation + str(array.length) + "\n"
        self.indentation = self.indentation[:-2]

        self.indentation = self.indentation[:-2]
        output += self.indentation + "END ARRAY\n"

        return output

    def visit_record(self, record):
        """Print the record and recurse on its scope."""
        output = self.indentation + "RECORD BEGIN\n"
        self.indentation += "  "

        output += record.scope.accept(self)

        self.indentation = self.indentation[:-2]
        output += self.indentation + "END RECORD\n"

        return output