class Scope:

    # the symbol table would just be printing
    # out the scope, right?
    def __init__(self, outer_scope):
        self.outer_scope = outer_scope
        self.symbol_table = {}

    def insert(self, name, type):
        self.symbol_table[name] = type

    def find(self, name):
        curr_pointer = -1
        returned_type = None
        while(curr_pointer is not None):
            if self.local(name):
                returned_type = self.symbol_table[name]
                break
            else:
                curr_pointer = self.outer_scope
        return returned_type

    def local(self, name):
        if name in self.symbol_table:
            return True
        else:
            return False
