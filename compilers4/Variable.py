from Entry import Entry

class Variable(Entry):

    def __init__(self, _type):
        self._type = _type

    def visit(self, visitor):
        visitor.visitVar(self)
