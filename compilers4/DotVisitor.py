import sys

class DotVisitor:

    def __init__(self):
        self.stack = [] # node stack to assist with constructing subtrees
        self.node_count = 0
        self.cluster_count = 1
        self.start_flag = 0

    def visitScope(self, scope):
        if self.start_flag == 0:
            self.start_flag = 1
            sys.stdout.write("digraph X {\n")

        sys.stdout.write("subgraph cluster_" + str(self.cluster_count) + " {\n")
        for i in sorted(scope.symbol_table):
            sys.stdout.write("i_{0} [label=\"Z\",shape=box,color=white,"
                                                      "fontcolor=black]\n".format(self.node_count))
            self.node_count += 1
            self.stack.append("i_{0}".format(self.node_count))
            scope.symbol_table[i].visit(self)
        sys.stdout.write("}\n")
        sys.stdout.write("}\n")

        # output the fields of a record
    def visitRecord(self, record):
        '''self.indent += 2
        self.write("RECORD BEGIN\n")
        self.indent += 2
        # visit scope
        self.visitScope(record.scope)
        self.indent -= 2
        self.write("END RECORD\n")
        self.indent -= 2'''

    # output the length and type of an array
    def visitArray(self, array):
        '''self.indent += 2
        self.write("ARRAY BEGIN\n")
        self.indent += 2
        self.write("type:\n")
        array._type.visit(self)
        self.write("length:\n")
        self.indent += 2
        self.write(str(array.length.value) + '\n')
        self.indent -= 2
        self.indent -= 2
        self.write("END ARRAY\n")
        self.indent -= 2'''

    # output the type of a variable
    def visitVar(self, var):
        '''self.indent += 2
        self.write("VAR BEGIN\n")
        self.indent += 2
        self.write("type:\n")
        var._type.visit(self)
        self.indent -= 2
        self.write("END VAR\n")
        self.indent -= 2'''

    # output the value and type of a constant
    def visitConst(self, const):
        '''self.indent += 2
        self.write("CONST BEGIN\n")
        self.indent += 2
        self.write("type:\n")
        const._type.visit(self)
        self.write("value:\n")
        self.indent += 2
        self.write(str(const.value) + '\n')
        self.indent -= 2
        self.indent -= 2
        self.write("END CONST\n")
        self.indent -= 2'''

    # output I
    def visitInt(self):
        '''self.indent += 2
        self.write("INTEGER\n")
        self.indent -= 2'''