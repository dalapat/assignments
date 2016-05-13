from Entry import Entry

class Variable(Entry):
    # represent a variable in Simple

    # initialize a Variable with type
    def __init__(self, _type):
        self._type = _type

    # output the type of a variable
    def visit(self, visitor):
        visitor.visitVar(self)

    def st_visit(self, visitor):
        return visitor.visitVar(self)
