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

'''
Runs over AST and interprets Simple Programs
'''
class Interpreter:

    # initializes an interpreter
    def __init__(self, ast, environment):
        self.stack = [] # explicit stack for interpreter
        self.ast = ast # ast to be traversed
        self.environment = environment # maps variables to storage space

    # method to start parsing ast
    def start(self):
        self.interpret(self.ast, self.environment)

    # follows visitor pattern to interpret AST
    def interpret(self, ast, environment):
        if isinstance(ast, NumberNode):
            self.stack.append(ast.constant.value)
        elif isinstance(ast, BinaryNode):
            self.interpret(ast.exp_left, environment)
            self.interpret(ast.exp_right, environment)
            second = self.stack.pop()
            first = self.stack.pop()
            first_val = first
            second_val = second
            if isinstance(first, IntegerBox):
                first_val = first.get()
            if isinstance(second, IntegerBox):
                second_val = second.get()
            if ast.operator == "+":
                self.stack.append(first_val + second_val)
            elif ast.operator == "-":
                self.stack.append(first_val - second_val)
            elif ast.operator == "*":
                self.stack.append(first_val - second_val)
            elif ast.operator == "DIV":
                if second == 0:
                    sys.stderr.write("error: division by 0")
                    exit(1)
                self.stack.append(first_val / second_val)
            elif ast.operator == "MOD":
                if second == 0:
                    sys.stderr.write("error: division by 0")
                    exit(1)
                self.stack.append(first_val % second_val)
            else:
                sys.stderr.write("error: invalid operator")
        elif isinstance(ast, VariableNode):
            try:
                self.stack.append(environment[ast.variable_name])
            except:
                sys.stderr.write("error: did not find var name: " + ast.variable_name)
                exit(1)
        elif isinstance(ast, AssignNode):
            self.interpret(ast.location, environment)
            self.interpret(ast.expression, environment)
            exp = self.stack.pop()
            loc = self.stack.pop()
            loc.set(exp)
            if ast._next is not None:
                ast._next.int_visit(self, self.environment)
        elif isinstance(ast, IfNode):
            self.interpret(ast.condition, environment)
            condition_result = self.stack.pop()
            if condition_result == 1:
                self.interpret(ast.instructions_true, environment)
            elif condition_result == 0:
                self.interpret(ast.instructions_false, environment)
            if ast._next is not None:
                ast._next.int_visit(self, self.environment)
        elif isinstance(ast, ReadNode):
            self.interpret(ast.location, environment)
            loc = self.stack.pop()
            input = sys.stdin.read()
            #input = "16"
            try:
                num = int(input)
            except:
                sys.stderr.write("error: not an integer")
            loc.set(num)
            if ast._next is not None:
                ast._next.int_visit(self, self.environment)
            #stack.append(loc)
        elif isinstance(ast, WriteNode):
            self.interpret(ast.expression, environment)
            exp = self.stack.pop()
            output = ""
            if isinstance(exp, IntegerBox):
                output = str(exp.get())
            elif isinstance(exp, int):
                output = str(exp)
            sys.stdout.write(output + '\n')
            if ast._next is not None:
                ast._next.int_visit(self, self.environment)
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
