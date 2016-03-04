from Entry import Entry

class Constant(Entry):

    def __init__(self, _type, value):
        # what's the point of Entry?
        self._type = _type
        self.value = value #make this 5 for now

    def visit(self, visitor):
        visitor.visitConst(self)


