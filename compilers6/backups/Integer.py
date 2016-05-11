from Type import Type

class Integer(Type):
    # represent an integer in Simple

    # initialize an integer
    def __init__(self):
        pass

    # output "INTEGER"
    def visit(self, visitor):
        visitor.visitInt()

integerInstance = Integer()
