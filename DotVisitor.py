# Eric Calder
# ecalder6@jhu.edu

from Constant import Constant
from Variable import Variable
from Type import Type
from Integer import Integer
from Array import Array
from Record import Record
from Scope import Scope

# Visitor that produces a DOT representation of the symbol table.
class DotVisitor:
    def __init__(self):
        """Initializes the DOT visitor."""
        self.output = "strict digraph G {\n"
        self.id = 0
        self.stack = []
        self.scopes = set()
        self.outer = None

    def display(self):
        """Called by parser."""
        self.program_scope.accept(self)

        self.output += "}"
        print(self.output)

    def visit_scope(self, scope):
        """Print everything in a scope. Recurse using a stack."""
        self.output += (
            "subgraph cluster" + str(self.id)
            + "{\n"
        )
        self.scopes.add(scope)
        self.id += 1

        # Used for visually attaching the scope to a node (like record).
        empty_node = None
        self.output += (
            "n" + str(self.id) + " [label=\"\",style=invis]\n"
        )
        empty_node = str(self.id)
        self.id += 1

        s = []
        for name in sorted(scope.table.keys()):
            self.output += (
                "n" + str(self.id) + " [label=" + str(name) + ",color=white]\n"
            )
            s.append("n" + str(self.id))
            self.id += 1

        # Reserve the stack so that the first entry added is on top.
        s.reverse()
        self.stack.extend(s)

        self.output += "}\n"

        if self.outer != None:
            self.output += "n" + self.outer + " -> n" + empty_node + "\n"
            self.outer = None

        # Go through each entry in order and visit them.
        for name in sorted(scope.table.keys()):
            scope.table[name].accept(self)

    def visit_const(self, const):
        """Print const with type and value."""
        self.output += (
            "n" + str(self.id) + " [label=" + str(const.value)
            + ", shape=diamond]\n"
        )
        prev = self.stack.pop()
        self.output += prev + " -> n" + str(self.id) + "\n"
        self.stack.append("n" + str(self.id))
        self.id += 1
        const.type.accept(self)

    def visit_var(self, var):
        """Print var with type."""
        self.output += (
            "n" + str(self.id) + " [label=\"\", shape=circle]\n"
        )
        prev = self.stack.pop()
        self.output += prev + " -> n" + str(self.id) + "\n"
        self.stack.append("n" + str(self.id))
        self.id += 1
        var.type.accept(self)

    def visit_field(self, field):
        """Print field with type."""
        self.output += (
            "n" + str(self.id) + " [label=\"\", shape=circle]\n"
        )
        prev = self.stack.pop()
        self.output += prev + " -> n" + str(self.id) + "\n"
        self.stack.append("n" + str(self.id))
        self.id += 1
        field.type.accept(self)

    def visit_integer(self, integer):
        """Print the integer type."""
        self.output += str(integer) + " [shape=box, style=rounded]\n"
        prev = self.stack.pop()
        self.output += prev + " -> " + str(integer) + "\n"

    def visit_invalid(self, invalid):
        """Print the invalid type (for debugging purpose only)."""
        self.output += self.indentation + str(invalid) + "\n"

    def visit_array(self, array):
        """Print the array with length and element type."""

        # Use id of the object as node to ensure that multiple nodes can connect
        # to the same array object.
        self.output += (
            "n" + str(id(array)) + " [label=\"Array\nlength: "
            + str(array.length) + "\", shape=box, style=rounded]\n"
        )
        prev = self.stack.pop()
        self.output += prev + " -> n" + str(id(array)) + "\n"
        self.stack.append("n" + str(id(array)))
        array.element_type.accept(self)

    def visit_record(self, record):
        """Print the record and recurse on its scope."""

        # Use id of the object as node to ensure that multiple nodes can connect
        # to the same record object.
        self.output += (
            "n" + str(id(record))
            + " [label=Record, shape=box, style=rounded]\n"
        )
        prev = self.stack.pop()
        self.output += prev + " -> n" + str(id(record)) + "\n"

        # Avoid visiting the same scope more than once.
        if record.scope not in self.scopes:
            self.outer = str(id(record))
            record.scope.accept(self)