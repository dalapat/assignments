from Entry import Entry

class Variable(Entry):
    # represent a variable in Simple

    # initialize a Variable with type
    def __init__(self, _type):
        self._type = _type
        self.offset = 0

    # output the type of a variable
    def visit(self, visitor):
        visitor.visitVar(self)

    def get_offset(self):
        return self.offset

    def set_offset(self, value):
        self.offset = value

    def st_visit(self, visitor):
        return visitor.visitVar(self)

    def cg_visit(self, visitor):
        pass

    def ncg_visit(self, visitor):
        return visitor.visitVar(self)
