class Scope:

    # the symbol table would just be printing
    # out the scope, right?
    def __init__(self, outer_scope):
        self.outer_scope = outer_scope
        self.symbol_table = {}

    def insert(self, name, _type):
        self.symbol_table[name] = _type

    def find(self, name):
        curr_pointer = self #should this be self?
        returned_type = None
        while(curr_pointer is not None): # won't find integer in outer scope
            # also getting stuck in infinite loop b/c currpointer never = none
            if curr_pointer.local(name):
                returned_type = curr_pointer.symbol_table[name]
                break
            else:
                curr_pointer = curr_pointer.outer_scope
        return returned_type

    def local(self, name):
        if name in self.symbol_table:
            return True
        else:
            return False
