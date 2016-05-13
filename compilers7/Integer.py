from Type import Type

class Integer(Type):
    # represent an integer in Simple

    # initialize an integer
    def __init__(self):
        self.size = 4

    # output "INTEGER"
    def visit(self, visitor):
        visitor.visitInt()

    def get_size(self):
        return self.size

    def st_visit(self, visitor):
        return visitor.visitInt()

    def ncg_visit(self, visitor):
        return visitor.visitInt()

integerInstance = Integer()
