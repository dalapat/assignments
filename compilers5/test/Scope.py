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
