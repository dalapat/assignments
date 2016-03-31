import sys

class Visitor:
    # text visitor pattern in python

    # initialize a text visitor with 0 left padding
    def __init__(self):
        self.indent = 0

    # output the names in a scope
    def visitScope(self, scope):
        self.write("SCOPE BEGIN\n")
        self.indent += 2
        for i in sorted(scope.symbol_table):
            self.write(i + " =>" + '\n')
            scope.symbol_table[i].visit(self)
        self.indent -= 2
        self.write("END SCOPE\n")

    def setIndent(self, indent):
        self.indent = indent

    # necessary empty function due to design flaw
    # between Visitor and DotVisitor
    def end(self):
        pass

    # format a string with proper padding
    def write(self, string):
        pad_string  = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + string)

    # output the fields of a record
    def visitRecord(self, record):
        self.indent += 2
        self.write("RECORD BEGIN\n")
        self.indent += 2
        # visit scope
        self.visitScope(record.scope)
        self.indent -= 2
        self.write("END RECORD\n")
        self.indent -= 2

    # output the length and type of an array
    def visitArray(self, array):
        self.indent += 2
        self.write("ARRAY BEGIN\n")
        self.indent += 2
        self.write("type:\n")
        array._type.visit(self)
        self.write("length:\n")
        self.indent += 2
        # self.write(str(array.length.value) + '\n')
        self.write(str(array.length) + '\n')
        self.indent -= 2
        self.indent -= 2
        self.write("END ARRAY\n")
        self.indent -= 2

    # output the type of a variable
    def visitVar(self, var):
        self.indent += 2
        self.write("VAR BEGIN\n")
        self.indent += 2
        self.write("type:\n")
        var._type.visit(self)
        self.indent -= 2
        self.write("END VAR\n")
        self.indent -= 2

    # output the value and type of a constant
    def visitConst(self, const):
        self.indent += 2
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
        self.indent -= 2

    # output I
    def visitInt(self):
        self.indent += 2
        self.write("INTEGER\n")
        self.indent -= 2