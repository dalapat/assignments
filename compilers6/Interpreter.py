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

class Interpreter:

    def __init__(self):
        pass

    def interpret(self, ast, environment, stack):
        if isinstance(ast, NumberNode):
            stack.append(ast.constant.value)
        elif isinstance(ast, BinaryNode):
            self.interpret(ast.exp_left, environment, stack)
            self.interpret(ast.exp_right, environment, stack)
            first = stack.pop()
            second = stack.pop()
            if ast.operator == "+":
                stack.append(first + second)
            elif ast.operator == "-":
                stack.append(first - second)
            elif ast.operator == "*":
                stack.append(first - second)
            elif ast.operator == "DIV":
                if second == 0:
                    sys.stderr.write("error: division by 0")
                    exit(1)
                stack.append(first / second)
            elif ast.operator == "MOD":
                if second == 0:
                    sys.stderr.write("error: division by 0")
                    exit(1)
                stack.append(first % second)
            else:
                sys.stderr.write("error: invalid operator")
        elif isinstance(ast, VariableNode):
            stack.append(environment[ast.variable_name])
        elif isinstance(ast, AssignNode):
            self.interpret(ast.location, environment, stack)
            self.interpret(ast.expression, environment, stack)
            exp = stack.pop()
            loc = stack.pop()
            loc.set(exp)
        elif isinstance(ast, IfNode):
            self.interpret(ast.condition, environment, stack)
            condition_result = stack.pop()
            if condition_result == "TRUE":
                self.interpret(ast.instructions_true, environment, stack)
            elif condition_result == "FALSE":
                self.interpret(ast.instructions_false, environment, stack)
        elif isinstance(ast, ReadNode):
            self.interpret(ast.location, environment, stack)
            loc = stack.pop()
            #input = sys.stdin.read()
            input = "16"
            try:
                num = int(input)
            except:
                sys.stderr.write("error: not an integer")
            loc.set(num)
            #stack.append(loc)
        elif isinstance(ast, WriteNode):
            self.interpret(ast.expression, environment, stack)
            exp = stack.pop()
            sys.stdout.write(str(exp) + '\n')
        elif isinstance(ast, RepeatNode):
            flag = "FALSE"
            while not flag:
                self.interpret(ast.instructions, environment, stack)
                self.interpret(ast.condition, environment, stack)
                flag = stack.pop()
        elif isinstance(ast, ConditionNode):
            self.interpret(ast.exp_left, environment, stack)
            self.interpret(ast.exp_right, environment, stack)
            relation = ast.relation
            left = stack.pop()
            right = stack.pop()
            if relation == "<":
                if left < right:
                    stack.append("TRUE")
                else:
                    stack.append("FALSE")
            elif relation == ">":
                if left > right:
                    stack.append("TRUE")
                else:
                    stack.append("FALSE")
            elif relation == "<=":
                if left <= right:
                    stack.append("TRUE")
                else:
                    stack.append("FALSE")
            elif relation == ">=":
                if left >= right:
                    stack.append("TRUE")
                else:
                    stack.append("FALSE")
            elif relation == "=":
                if left == right:
                    stack.append("TRUE")
                else:
                    stack.append("FALSE")
            elif relation == "#":
                if not left == right:
                    stack.append("TRUE")
                else:
                    stack.append("FALSE")
            else:
                sys.stderr.write("error: invalid condition")
        elif isinstance(ast, FieldNode):
            self.interpret(ast.location, environment, stack)
            self.interpret(ast.variable, environment, stack)
            field = stack.pop()
            record = stack.pop()
            stack.append(record.get_field(field))
        elif isinstance(ast, IndexNode):
            self.interpret(ast.location, environment, stack)
            self.interpret(ast.expression, environment, stack)
            index = stack.pop()
            #print type(index)
            #if not isinstance(index, IntegerBox):
            #    sys.stderr.write("error: accessing array with noninteger index")
            arr = stack.pop()
            stack.append(arr.index(index))
        else:
            pass