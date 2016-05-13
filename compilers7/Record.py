from Type import Type

class Record(Type):
    # record type in Simple

    # initialize a record with a scope
    def __init__(self, scope):
        self.scope = scope
        self.size = 0

    # output the fields of a record
    def visit(self, visitor):
        visitor.visitRecord(self)

    def st_visit(self, visitor):
        return visitor.visitRecord(self)

    def ncg_visit(self, visitor):
        return visitor.visitRecord(self)


