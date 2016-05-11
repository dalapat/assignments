from Type import Type

class Array(Type):
    # array type for simple

    # initialize an array with array length and type of array
    def __init__(self, length, _type):
        self.length = length
        self.unit_size = 0
        self._type = _type

    # output the length and type
    def visit(self, visitor):
        visitor.visitArray(self)

    def get_length(self):
        return self.length

    def get_type(self):
        return self._type