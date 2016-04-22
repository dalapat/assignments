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
        self.num_loops = 1
        self.num_if = 1

    # ARM headers, unfinished
    def start(self):
        '''self.output_string += "\t\t.text\n"
        self.output_string += ".Ltext0:\n"
        self.make_format()
        self.output_string += "\t\t.globl main\n"
        self.output_string += "\t\t.type main, @function\n"
        self.output_string += "main:\n"
        self.code_generator(self.ast)'''
        self.cgwrite(".arch armv6")
        self.cgwrite(".fpu vfp")
        self.cgwrite(".align 2")
        self.cgwrite(".global main")
        self.cgwrite(".data")
        self.output_string += "vars:\t\t.space {0}\n".format(self.scope.stsize)
        #self.cgwrite(".space {0}".format(self.scope.stsize))
        self.output_string += "format:\t\t.asciz \"%d\\n\"\n" # does a dot need to be here
        #self.cgwrite(".asciz \"%d\\n\"")
        self.cgwrite(".text")
        #self.cgwrite(".align 4")
        #self.cgwrite(".text")
        #self.cgwrite(".globl main")
        #self.cgwrite(".type main @fcn")
        self.output_string += "main:\n"
        self.cgwrite("ldr r11, =vars")
        self.code_generator(self.ast)
        self.cgwrite("bl exit\n")

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
            self.output_string += "\t\tpush {r2}\n"
            return "number"
        elif isinstance(ast, BinaryNode):
            s1 = self.code_generator(ast.exp_left)
            if s1 == "location":
                self.cgwrite("pop {r2}")
                self.cgwrite("ldr r2, [r2]")
                self.cgwrite("push {r2}")
            s2 = self.code_generator(ast.exp_right)
            if s2 == "location":
                self.cgwrite("pop {r2}")
                self.cgwrite("ldr r2, [r2]")
                self.cgwrite("push {r2}")
            self.output_string += "\t\tpop {r2}\n"
            self.output_string += "\t\tpop {r3}\n"
            if ast.operator == "+":
                self.cgwrite("@plus")
                self.output_string += "\t\tadd r2, r2, r3\n"
                self.output_string += "\t\tpush {r2}\n"
            elif ast.operator == "-":
                self.output_string += "\t\tsub r2, r2, r3\n"
                self.output_string += "\t\tpush {r2}\n"
            elif ast.operator == "*":
                self.output_string += "\t\tmul r2, r2, r3\n"
                self.output_string += "\t\tpush {r2}\n"
            elif ast.operator == "DIV":
                self.output_string += "\t\tsdiv r2, r2, r3\n"
                self.output_string += "\t\tpush {r2}\n"
            elif ast.operator == "MOD":
                self.output_string += "\t\tmod r2, r2, r3\n"
                self.output_string += "\t\tpush {r2}\n"
            else:
                sys.stderr.write("error: invalid operator")
            return "number"
        elif isinstance(ast, VariableNode):
            self.cgwrite("add r2, r11, #{0}".format(ast.variable.get_offset()))
            self.cgwrite("push {r2}")
            return "location"
        elif isinstance(ast, AssignNode):
            '''self.interpret(ast.location, environment)
            self.interpret(ast.expression, environment)
            exp = self.stack.pop()
            loc = self.stack.pop()
            loc.set(exp)'''
            self.code_generator(ast.location)
            s = self.code_generator(ast.expression)
            if s == "location":
                self.cgwrite("pop {r3}")
                self.cgwrite("ldr r3, [r3]")
                self.cgwrite("pop {r2}")
                self.cgwrite("str r3, [r2]")
            elif s == "number":
                self.cgwrite("pop {r3}")
                self.cgwrite("pop {r2}")
                self.cgwrite("str r3, [r2]")
            #self.cgwrite("push {r2}")
            '''self.cgwrite("pop {r2}")
            self.cgwrite("pop {r3}")
            self.cgwrite("pop {r2}")
            self.cgwrite("ldr r2, [r2]")
            self.cgwrite("str r2, [r3]")'''
            if ast._next is not None:
                ast._next.cg_visit(self)
            return "t"
        elif isinstance(ast, IfNode):
            self.output_string += "itrue{0}:\n".format(self.num_if)
            self.code_generator(ast.instructions_true)
            self.output_string += "ifalse{0}:\n".format(self.num_if)
            self.code_generator(ast.instructions_false)
            self.num_if += 1
            self.code_generator(ast.condition)
            self.cgwrite("pop {r2}")
            self.cgwrite("cmp r2, #1")
            self.cgwrite("beq itrue{0}".format(self.num_if - 1))
            self.cgwrite("bne ifalse{0}".format(self.num_if - 1))
            # self.code_generator(ast.instructions_true)
            if ast._next is not None:
                ast._next.cg_visit(self)
            return "t"
        elif isinstance(ast, ReadNode):
            # unfinished
            self.code_generator(ast.location)
            self.cgwrite("pop {r2}")
            self.cgwrite("ldr r0, =format")
            self.cgwrite("mov r1, r2")
            self.cgwrite("bl scanf")
            if ast._next is not None:
                ast._next.cg_visit(self)
            return "t"
        elif isinstance(ast, WriteNode):
            #self.cgwrite("@write")
            self.code_generator(ast.expression)
            self.cgwrite("pop {r2}")
            self.cgwrite("ldr r2, [r2]")
            self.cgwrite("push {r2}")
            self.cgwrite("pop {r2}")
            self.cgwrite("ldr r0, =format")
            self.cgwrite("mov r1, r2")
            self.cgwrite("bl printf")
            if ast._next is not None:
                ast._next.cg_visit(self)
        elif isinstance(ast, RepeatNode):
            # unfinished
            self.output_string += "loop{0}:\n".format(self.num_loops)
            self.num_loops += 1
            self.code_generator(ast.instructions)
            self.code_generator(ast.condition)
            self.cgwrite("pop {r2}")
            self.cgwrite("cmp r2, #0")
            self.cgwrite("beq loop{0}".format(self.num_loops-1))
            if ast._next is not None:
                ast._next.cg_visit(self)
            return "t"
        elif isinstance(ast, ConditionNode):
            # unfinished
            s1 = self.code_generator(ast.exp_left)
            if s1 == "location":
                self.cgwrite("pop {r2}")
                self.cgwrite("ldr r2, [r2]")
                self.cgwrite("push {r2}")
            s2 = self.code_generator(ast.exp_right)
            if s2 == "location":
                self.cgwrite("pop {r2}")
                self.cgwrite("ldr r2, [r2]")
                self.cgwrite("push {r2}")
            self.cgwrite("pop {r2}")
            self.cgwrite("pop {r3}")
            self.cgwrite("cmp r3, r2")
            if ast.relation == "<":
                self.cgwrite("movlt r2, #1")
                self.cgwrite("movge r2, #0")
            elif ast.relation == ">":
                self.cgwrite("movgt r2, #1")
                self.cgwrite("movle r2, #0")
            elif ast.relation == "<=":
                self.cgwrite("movle r2, #1")
                self.cgwrite("movgt r2, #0")
            elif ast.relation == ">=":
                self.cgwrite("movge r2, #1")
                self.cgwrite("movlt r2, #0")
            elif ast.relation == "=":
                self.cgwrite("moveq r2, #1")
                self.cgwrite("movne r2, #0")
            elif ast.relation == "#":
                self.cgwrite("movne r2, #1")
                self.cgwrite("moveq r2, #0")
            else:
                sys.stderr.write("error: invalid condition")
            self.cgwrite("push {r2}")
            return "t"
        elif isinstance(ast, FieldNode):
            # unfinished
            pass
        elif isinstance(ast, IndexNode):
            self.code_generator(ast.location)
            s = self.code_generator(ast.expression)
            if s == "location":
                self.cgwrite("pop {r2}")
                self.cgwrite("ldr r2, [r2]")
                self.cgwrite("push {r2}") #index in simple
            self.cgwrite("ldr r3, ={0}".format(
                    self.scope.find(ast.location.variable_name)._type.unit_size))
            #self.cgwrite("@{0}".format(
            #       self.scope.find(ast.location.variable_name)._type.unit_size))
            self.cgwrite("pop {r2}")
            self.cgwrite("mul r2, r2, r3")
            self.cgwrite("push {r2}")
            self.cgwrite("pop {r3}")
            self.cgwrite("pop {r2}")
            self.cgwrite("add r2, r2, r3")
            self.cgwrite("push {r2}")
            return "location"
        else:
            pass