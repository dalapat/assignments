from Integer import Integer
from Array import Array
from Record import Record
from Variable import Variable
from IntegerBox import IntegerBox
from ArrayBox import ArrayBox
from RecordBox import RecordBox
class Scope:
    # represent a symbol table

    # initialize a symbol table with an outer symbol table
    def __init__(self, outer_scope):
        self.outer_scope = outer_scope
        self.symbol_table = {}

    # insert a name and associated type into the symbol table
    def insert(self, name, _type):
        self.symbol_table[name] = _type

    # search in the local scope as well as outer scope
    def find(self, name):
        curr_pointer = self # traversal pointer for find
        returned_type = None
        while(curr_pointer is not None):
            if curr_pointer.local(name):
                returned_type = curr_pointer.symbol_table[name]
                break
            else:
                curr_pointer = curr_pointer.outer_scope
        return returned_type

    # search only in local scope
    def local(self, name):
        if name in self.symbol_table:
            return True
        else:
            return False

    def make_environment(self):
        environment = {}
        for identifier in self.symbol_table:
            if isinstance(self.symbol_table[identifier], Variable):
                environment[identifier] = self.make_box(self.symbol_table[identifier]._type)
        return environment

    def make_box(self, type):
        if isinstance(type, Integer):
            return IntegerBox()
        elif isinstance(type, Array):
            list = []
            for i in range(type.length):
                list.append(self.make_box(type._type))
            return ArrayBox(list)
        elif isinstance(type, Record):
            fields = {}
            for field in type.scope.symbol_table:
                fields[field] = self.make_box(type.scope.symbol_table[field]._type)
            return RecordBox(fields)

    def st_visit(self, visitor):
        return visitor.visitScope(self)


