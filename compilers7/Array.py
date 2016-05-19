from Type import Type
import sys
class Array(Type):
    # array type for simple

    # initialize an array with array length and type of array
    def __init__(self, length, _type):
        self.length = length
        if self.length < 0:
            sys.stderr.write("error: invalid index\n")
            exit(1)
        self.unit_size = 0
        self._type = _type
        self.size = 0

    # output the length and type
    def visit(self, visitor):
        visitor.visitArray(self)

    def get_length(self):
        return self.length

    def get_size(self):
        return self.size

    def get_unit_size(self):
        return self.unit_size

    def st_visit(self, visitor):
        return visitor.visitArray(self)

    def ncg_visit(self, visitor):
        return visitor.visitArray(self)