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
        self.indent -= 2

    def visitRepeatNode(self, repeat_node):
        self.indent += 2
        self.write("Repeat:")
        self.write("condition =>")
        repeat_node.condition.visit(self)
        self.write("instructions =>")
        repeat_node.instructions.visit(self)
        self.indent -= 2

    def visitConditionNode(self, condition_node):
        self.indent += 2
        self.write("Condition ({0}):".format(condition_node.relation))
        self.write("left =>")
        condition_node.exp_left.visit(self)
        self.write("right =>")
        condition_node.exp_right.visit(self)
        self.indent -= 2

    def visitReadNode(self, read_node):
        self.indent += 2
        self.write("Read:")
        self.write("location =>")
        read_node.location.visit(self)
        self.indent -= 2

    def visitWriteNode(self, write_node):
        self.indent += 2
        self.write("Write:")
        self.write("expression =>")
        write_node.expression.visit(self)
        self.indent -= 2

    def visitWhile(self):
        pass

    def visitIfNode(self, if_node):
        self.indent += 2
        self.write("If:")
        self.write("condition =>")
        if_node.condition.visit(self)
        self.write("true =>")
        if_node.instructions_true.visit(self)
        if if_node.instructions_false is not None:
            self.write("false =>")
            if_node.instructions_false.visit(self)
        self.indent -= 2

    def visitBinaryNode(self, binary_node):
        self.indent += 2
        self.write("Binary ({0}):".format(binary_node.operator))
        self.write("left =>")
        binary_node.exp_left.visit(self)
        self.write("right =>")
        binary_node.exp_right.visit(self)
        self.indent -= 2

    def visitNumberNode(self, number_node):
        self.indent += 2
        self.write("Number:")
        self.write("value =>")
        self.stvisitor.setIndent(self.indent)
        number_node.constant.visit(self.stvisitor)
        self.indent -= 2

    def visitVariableNode(self, variable_node):
        self.indent += 2
        self.write("Variable:")
        self.write("variable =>")
        self.stvisitor.setIndent(self.indent)
        variable_node.variable.visit(self.stvisitor)
        self.indent -= 2

    def visitIndexNode(self, index_node):
        self.indent += 2
        self.write("Index:")
        self.write("location =>")
        index_node.location.visit(self)
        self.write("expression =>")
        index_node.expression.visit(self)
        self.indent -= 2

    def visitFieldNode(self, field_node):
        self.indent += 2
        self.write("Field:")
        self.write("location =>")
        field_node.location.visit(self)
        self.write("variable =>")
        field_node.variable.visit(self)
        self.indent -= 2

    def start(self):
        self.write("instructions =>")

