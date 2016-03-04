from Entry import Entry

class Constant(Entry):
    # represent a constant in Simple

    # initialize a Constant with type and value
    def __init__(self, _type, value):
        self._type = _type
        self.value = value

    # output the type and value
    def visit(self, visitor):
        visitor.visitConst(self)


