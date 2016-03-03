from Type import Type

class Array(Type):

    def __init__(self, length, _type):
        self.length = length
        self._type = _type

    def visit(self, visitor):
        visitor.visitArray(self)