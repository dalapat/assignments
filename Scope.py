# Eric Calder
# ecalder6@jhu.edu

# Contains the symbol table for a scope.
class Scope:
    def __init__(self, outer):
        """Initializes the scope."""
        self.outer = outer
        self.table = {}

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_scope(self)

    def insert(self, name, value):
        """Insert a string, entry pair into the symbol table."""
        self.table[name] = value

    def local(self, name):
        """Whether the symbol table contains a name, entry pair."""
        if name in self.table:
            return True
        return False

    def find(self, name):
        """Get the entry with the specified name."""
        if self.local(name):
            return self.table[name]
        
        # Check outer scopes if entry doesn't exist in the current scope.
        if self.outer != None:
            return self.outer.find(name)
        else:
            return None

    def __str__(self):
        return "Scope"