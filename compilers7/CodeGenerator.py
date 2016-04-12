import sys
from NumberNode import NumberNode
from BinaryNode import BinaryNode
import sys
from VariableNode import VariableNode
from AssignNode import AssignNode
from IfNode import IfNode
from ReadNode import ReadNode
from WriteNode import WriteNode
from RepeatNode import RepeatNode
from ConditionNode import ConditionNode
from FieldNode import FieldNode
from IndexNode import IndexNode
from IntegerBox import IntegerBox

# class to generate ARM assembly code from SIMPLE program
class CodeGenerator:

    # initialize code generator
    def __init__(self, scope, flag, ast, filename=""):
        self.scope = scope # scope to reference during traversal
        self.flag = flag # print to stdout or file
        self.output_string = "" # assembly code
        self.ast = ast # ast to parse
        self.filename = filename # filename to write to

    # ARM headers, unfinished
    def start(self):
        self.output_string += "\t\t.text\n"
        self.output_string += ".Ltext0:\n"
        self.make_format()
        self.output_string += "\t\t.globl main\n"
        self.output_string += "\t\t.type main, @function\n"
        self.output_string += "main:\n"
        self.code_generator(self.ast)

    # ARM printing
    def make_format(self):
        self.output_string += ".LCO:\n"
        self.cgwrite(".string \"%d\\n\"")
        self.cgwrite(".data")
        self.cgwrite(".align 4")
        self.cgwrite(".type   format, @object")
        self.cgwrite(".size   format, 4")
        self.output_string += "format:\n"
        self.cgwrite(".long   .LC0")
        self.cgwrite(".align 4")
        self.cgwrite(".type   data, @object")
        self.cgwrite(".size   data, 4")

    # format ARM assembly
    def cgwrite(self, string):
        self.output_string += "\t\t{0}\n".format(string)

    # write to stdout or file
    def cgoutput(self):
        if self.flag == 0:
            sys.stdout.write(self.output_string)
        elif self.flag == 1:
            f = open(self.filename, "w")
            f.write(self.output_string)
            f.close()

    # perform left to right post order traversal on ast
    def code_generator(self, ast):
        if isinstance(ast, NumberNode):
            self.output_string += "\t\tldr r2, ={0}\n".format(ast.constant.value)
            self.output_string += "\t\tpush r2\n"
        elif isinstance(ast, BinaryNode):
            self.code_generator(ast.exp_left)
            self.code_generator(ast.exp_right)
            self.output_string += "\t\tpop r2\n"
            self.output_string += "\t\tpop r3\n"
            if ast.operator == "+":
                self.output_string += "\t\tadd r2, r2, r3\n"
                self.output_string += "\t\tpush r2\n"
            elif ast.operator == "-":
                self.output_string += "\t\tsub r2, r2, r3\n"
                self.output_string += "\t\tpush r2\n"
            elif ast.operator == "*":
                self.output_string += "\t\tmul r2, r2, r3\n"
                self.output_string += "\t\tpush r2\n"
            elif ast.operator == "DIV":
                self.output_string += "\t\tsdiv r2, r2, r3\n"
                self.output_string += "\t\tpush r2\n"
            elif ast.operator == "MOD":
                self.output_string += "\t\tmod r2, r2, r3\n"
                self.output_string += "\t\tpush r2\n"
            else:
                sys.stderr.write("error: invalid operator")
        elif isinstance(ast, VariableNode):
            self.cgwrite("sub r2, r11, ={0}".format(ast.variable.get_offset()))
            self.cgwrite("push r2")
        elif isinstance(ast, AssignNode):
            '''self.interpret(ast.location, environment)
            self.interpret(ast.expression, environment)
            exp = self.stack.pop()
            loc = self.stack.pop()
            loc.set(exp)'''
            self.code_generator(ast.location)
            self.code_generator(ast.expression)
            self.cgwrite("pop r2")
            self.cgwrite("ldr r2, [r2]")
            self.cgwrite("push r2")
            self.cgwrite("pop r2")
            self.cgwrite("pop r3")
            self.cgwrite("str r2, [r3]")
            if ast._next is not None:
                ast._next.cg_visit(self)
        elif isinstance(ast, IfNode):
            # unfinished
            if ast._next is not None:
                ast._next.cg_visit(self)
        elif isinstance(ast, ReadNode):
            # unfinished
            if ast._next is not None:
                ast._next.cg_visit(self)
        elif isinstance(ast, WriteNode):
            self.code_generator(ast.expression)
            self.cgwrite("pop r2")
            self.cgwrite("ldr r2, [r2]")
            self.cgwrite("push r2")
            self.cgwrite("pop r2")
            self.cgwrite("ldr r0, format")
            self.cgwrite("mov r1, r2")
            self.cgwrite("bl printf")
            if ast._next is not None:
                ast._next.cg_visit(self)
        elif isinstance(ast, RepeatNode):
            # unfinished
            if ast._next is not None:
                ast._next.cg_visit(self)
        elif isinstance(ast, ConditionNode):
            # unfinished
            pass
        elif isinstance(ast, FieldNode):
            # unfinished
            pass
        elif isinstance(ast, IndexNode):
            # unfinished
            pass
        else:
            pass