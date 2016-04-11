from Integer import Integer
from Array import Array
from Record import Record
from Variable import Variable
from IntegerBox import IntegerBox
from ArrayBox import ArrayBox
from RecordBox import RecordBox

import sys
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

    def make_code_generator_environment(self):
        environment = {}
        offset = 0
        for identifier in self.symbol_table:
            if isinstance(self.symbol_table[identifier], Variable):
                self.symbol_table[identifier].set_offset(offset)
                size = self.make_offset(self.symbol_table[identifier]._type)
                offset += size

    def test(self):
        for identifier in self.symbol_table:
            if isinstance(self.symbol_table[identifier], Variable):
                self.symbol_table[identifier].set_offset(self.make_offset(self.symbol_table[identifier]._type))

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

    def make_offset(self, type):
        if isinstance(type, Integer):
            return type.get_size()
        elif isinstance(type, Array):
            array_type_size = self.make_offset(type._type)
            type.unit_size = array_type_size
            return type.length * array_type_size
        elif isinstance(type, Record):
            size_counter = 0
            offset = 0
            for field in type.scope.symbol_table:
                type.scope.symbol_table[field].set_offset(offset)
                size = self.make_offset(type.scope.symbol_table[field]._type)
                offset += size
            return offset
        else:
            sys.stderr.write("error: invalid type\n")
            exit(1)

