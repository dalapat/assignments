from Type import Type

class Integer(Type):
    # represent an integer in Simple

    # initialize an integer
    def __init__(self):
        self.set_size(4)

    # output "INTEGER"
    def visit(self, visitor):
        visitor.visitInt()

integerInstance = Integer()
