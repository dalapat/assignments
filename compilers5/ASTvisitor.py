import sys
from Visitor import Visitor

class ASTvisitor:

    def __init__(self):
        self.indent = 0
        self.stvisitor = Visitor()

    def write(self, string):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + string + "\n")

    def visitAssignNode(self, assign_node):
        self.indent += 2
        self.write("Assign:")
        self.write("location =>")
        assign_node.location.visit(self)
        self.write("expression =>")
        assign_node.expression.visit(self)

    def visitRepeatNode(self):
        pass

    def visitConditionNode(self):
        pass

    def visitReadNode(self):
        pass

    def visitWriteNode(self):
        pass

    def visitWhile(self):
        pass

    def visitIfNode(self):
        pass

    def visitBinaryNode(self):
        pass

    def visitNumberNode(self, number_node):
        self.indent += 2
        self.write("Number:")
        number_node.constant.visit(self.stvisitor)

    def visitVariableNode(self, variable_node):
        self.indent += 2
        self.write("Variable:")
        variable_node.variable.visit(self.stvisitor)
        self.indent -= 2

    def visitIndexNode(self):
        pass

    def visitFieldNode(self):
        pass

