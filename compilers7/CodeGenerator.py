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

class CodeGenerator:

    def __init__(self, scope):
        self.scope = scope

    def start(self):
        sys.stdout.write("\t\t.text\n")
        sys.stdout.write(".Ltext0:\n")
        sys.stdout.write("\t\t.globl main\n")
        sys.stdout.write("\t\t.type main, @function\n")
        sys.stdout.write("main:\n")

    def cgwrite(self, string):
        sys.stdout.write("\t\t{0}\n".format(string))

    def code_generator(self, ast):
        if isinstance(ast, NumberNode):
            sys.stdout.write("\t\tldr r2, ={0}\n".format(ast.constant.value))
            sys.stdout.write("\t\tpush r2\n")
        elif isinstance(ast, BinaryNode):
            self.code_generator(ast.exp_left)
            self.code_generator(ast.exp_right)
            sys.stdout.write("\t\tpop r2\n")
            sys.stdout.write("\t\tpop r3\n")
            if ast.operator == "+":
                sys.stdout.write("\t\tadd r2, r2, r3\n")
                sys.stdout.write("\t\tpush r2\n")
            elif ast.operator == "-":
                sys.stdout.write("\t\tsub r2, r2, r3\n")
                sys.stdout.write("\t\tpush r2\n")
            elif ast.operator == "*":
                sys.stdout.write("\t\tmul r2, r2, r3\n")
                sys.stdout.write("\t\tpush r2\n")
            elif ast.operator == "DIV":
                sys.stdout.write("\t\tsdiv r2, r2, r3\n")
                sys.stdout.write("\t\tpush r2\n")
            elif ast.operator == "MOD":
                sys.stdout.write("\t\tmod r2, r2, r3\n")
                sys.stdout.write("\t\tpush r2\n")
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
            self.code_generator()
            if ast._next is not None:
                ast._next.cg_visit(self)
        elif isinstance(ast, RepeatNode):
            flag = 0
            while not flag:
                self.interpret(ast.instructions, environment)
                self.interpret(ast.condition, environment)
                flag = self.stack.pop()
                if ast._next is not None:
                    ast._next.int_visit(self, self.environment)
        elif isinstance(ast, ConditionNode):
            self.interpret(ast.exp_left, environment)
            self.interpret(ast.exp_right, environment)
            relation = ast.relation
            left = self.stack.pop()
            right = self.stack.pop()
            if relation == "<":
                if left < right:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            elif relation == ">":
                if left > right:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            elif relation == "<=":
                if left <= right:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            elif relation == ">=":
                if left >= right:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            elif relation == "=":
                if left == right:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            elif relation == "#":
                if not left == right:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            else:
                sys.stderr.write("error: invalid condition\n")
                exit(1)
        elif isinstance(ast, FieldNode):
            self.interpret(ast.location, environment)
            #self.interpret(ast.variable, environment)
            #field = self.stack.pop()
            record = self.stack.pop()
            val = record.get_field(ast.variable.variable_name)
            self.stack.append(val)
        elif isinstance(ast, IndexNode):
            self.interpret(ast.location, environment)
            self.interpret(ast.expression, environment)
            index = self.stack.pop()
            #print type(index)
            #if not isinstance(index, IntegerBox):
            #    sys.stderr.write("error: accessing array with noninteger index")
            arr = self.stack.pop()
            self.stack.append(arr.index(index))
        else:
            pass