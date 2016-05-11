# Eric Calder
# ecalder6@jhu.edu

from TextVisitor import TextVisitor
from Constant import Constant
from Integer import Integer

# Visitor that creates the text output for AST.
class ASTTextVisitor:
    def __init__(self):
        """Initializes the text visitor"""
        self.indentation = ""
        self.tree = None
        self.program_scope = None

    def display(self):
        """Called by the Parser."""

        self.st_visitor = TextVisitor()
        self.st_visitor.program_scope = self.program_scope

        output = self.indentation + "instructions =>\n"
        self.indentation += "  "

        output += self.visit_instructions(self.tree)

        print(output)

    def visit_instructions(self, instruction):
        output = ""

        while instruction != None:
            output += instruction.accept(self)
            instruction = instruction.next

        return output

    def visit_assign(self, assign):
        """Print everything in an assign tree."""
        output = self.indentation + "Assign:\n"

        output += self.indentation + "location =>\n"
        self.indentation += "  "
        output += assign.location.accept(self)
        self.indentation = self.indentation[:-2]

        output += self.indentation + "expression =>\n"
        self.indentation += "  "
        output += assign.expression.accept(self)
        self.indentation = self.indentation[:-2]

        return output

    def visit_if(self, if_ins):
        """Print everything in an if tree."""
        output = self.indentation + "If:\n"

        output += self.indentation + "condition =>\n"
        self.indentation += "  "
        output += if_ins.condition.accept(self)
        self.indentation = self.indentation[:-2]

        output += self.indentation + "true =>\n"
        self.indentation += "  "
        output += self.visit_instructions(if_ins.instructions_true)
        self.indentation = self.indentation[:-2]

        if if_ins.instructions_false != None:
            output += self.indentation + "false =>\n"
            self.indentation += "  "
            output += self.visit_instructions(if_ins.instructions_false)
            self.indentation = self.indentation[:-2]

        return output

    def visit_repeat(self, repeat):
        """Print everything in a repeat tree."""
        output = self.indentation + "Repeat:\n"

        output += self.indentation + "condition =>\n"
        self.indentation += "  "
        output += repeat.condition.accept(self)
        self.indentation = self.indentation[:-2]

        output += self.indentation + "instructions =>\n"
        self.indentation += "  "

        output += self.visit_instructions(repeat.instructions)

        self.indentation = self.indentation[:-2]

        return output

    def visit_read(self, read):
        """Print everything in a read tree."""
        output = self.indentation + "Read:\n"
        output += self.indentation + "location =>\n"
        self.indentation += "  "
        output += read.location.accept(self)
        self.indentation = self.indentation[:-2]
        return output

    def visit_write(self, write):
        """Print everything in a write tree."""
        output = self.indentation + "Write:\n"
        output += self.indentation + "expression =>\n"
        self.indentation += "  "
        output += write.expression.accept(self)
        self.indentation = self.indentation[:-2]
        return output

    def visit_number(self, number):
        """Print everything in a write tree."""
        output = self.indentation + "Number:\n"
        output += self.indentation + "value =>\n"
        self.indentation += "  "
        self.st_visitor.indentation = self.indentation
        output += number.entry.accept(self.st_visitor)
        self.indentation = self.indentation[:-2]
        return output

    def visit_binary(self, binary):
        """Print everything in a binary tree."""
        output = (
            self.indentation + "Binary (" + str(binary.operator) + "):\n"
        )

        output += self.indentation + "left =>\n"
        self.indentation += "  "
        output += binary.left.accept(self)
        self.indentation = self.indentation[:-2]

        output += self.indentation + "right =>\n"
        self.indentation += "  "
        output += binary.right.accept(self)
        self.indentation = self.indentation[:-2]

        return output

    def visit_variableAST(self, variableAST):
        """Print everything in a variable tree."""
        output = self.indentation + "Variable:\n"
        output += self.indentation + "variable =>\n"
        self.indentation += "  "
        self.st_visitor.indentation = self.indentation
        output += variableAST.variable.accept(self.st_visitor)
        self.indentation = self.indentation[:-2]
        return output

    def visit_index(self, index):
        """Print everything in an index tree."""
        output = self.indentation + "Index:\n"
        output += self.indentation + "location =>\n"
        self.indentation += "  "
        output += index.location.accept(self)
        self.indentation = self.indentation[:-2]
        output += self.indentation + "expression =>\n"
        self.indentation += "  "
        output += index.expression.accept(self)
        self.indentation = self.indentation[:-2]
        return output

    def visit_fieldAST(self, fieldAST):
        """Print everything in a field tree."""
        output = self.indentation + "Field:\n"
        output += self.indentation + "location =>\n"
        self.indentation += "  "
        output += fieldAST.location.accept(self)
        self.indentation = self.indentation[:-2]

        output += self.indentation + "variable =>\n"
        self.indentation += "  "   
        output += fieldAST.variable.accept(self)
        self.indentation = self.indentation[:-2]
        return output

    def visit_condition(self, condition):
        """Print everything in a field tree."""
        output = (
            self.indentation + "Condition (" + str(condition.relation) + "):\n"
        )

        output += self.indentation + "left =>\n"
        self.indentation += "  "
        output += condition.left.accept(self)
        self.indentation = self.indentation[:-2]

        output += self.indentation + "right =>\n"
        self.indentation += "  "
        output += condition.right.accept(self)
        self.indentation = self.indentation[:-2]

        return output