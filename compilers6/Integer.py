from Type import Type

class Integer(Type):
    # represent an integer in Simple

    # initialize an integer
    def __init__(self):
        pass

    # output "INTEGER"
    def visit(self, visitor):
        visitor.visitInt()

    def st_visit(self, visitor):
        return visitor.visitInt()

integerInstance = Integer()
