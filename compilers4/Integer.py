from Type import Type

class Integer(Type):

    def __init__(self):
        pass

    def visit(self, visitor):
        visitor.visitInt()

