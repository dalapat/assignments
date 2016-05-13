import sys
import copy
from Box import Box
from ArrayBox import ArrayBox
from RecordBox import RecordBox
from IntegerBox import IntegerBox

class ASTInterpreterVisitor:

    def __init__(self, environment, ast):
        self.ast = ast
        self.environment = environment
        self.stack = []

    def start(self):
        self.visitInstructions(self.ast)

    def visitInstructions(self, head):
        while head is not None:
            head.int_visit(self)
            head = head._next

    def get_box(self):
        box = self.stack.pop()
        return_val = box
        if isinstance(box, int):
            return return_val
        if not isinstance(box, Box):
            return_val = self.environment.find(box)
        return return_val

    def visitIf(self, if_node):
        if_node.condition.int_visit(self)
        result = self.stack.pop()

        if result == 1:
            self.visitInstructions(if_node.instructions_true)
        else:
            self.visitInstructions(if_node.instructions_false)

    def visitAssignNode(self, assign_node):
        assign_node.location.int_visit(self)
        assign_node.expression.int_visit(self)
        exp = self.get_box()
        loc = self.get_box()
        if isinstance(exp, IntegerBox):
            store_val = exp.value
        elif isinstance(exp, int):
            store_val = exp
        elif isinstance(exp, ArrayBox):
            store_val = copy.deepcopy(exp.value)
        elif isinstance(exp, RecordBox):
            store_val = copy.deepcopy(exp.value)
        loc.value = store_val

    def visitRepeatNode(self, repeat_node):
        flag = 0
        while not flag:
            self.visitInstructions(repeat_node.instructions)
            repeat_node.condition.int_visit(self)
            flag = self.stack.pop()

    def visitConditionNode(self, condition_node):

        #relation_map = {"=":"==", "#":"!=", ">":">", "<":"<",
        #                ">=":">=", "<=":"<="}

        #relation = relation_map[condition_node.relation]

        condition_node.exp_left.int_visit(self)
        condition_node.exp_right.int_visit(self)

        right = self.get_box()
        if isinstance(right, IntegerBox):
            right = right.get()
        left = self.get_box()
        if isinstance(left, IntegerBox):
            left = left.get()
        #self.stack.append(eval(str(left) + str(relation) + str(right)))
        if condition_node.relation == "=":
            if left == right:
                self.stack.append(1)
            else:
                self.stack.append(0)
        elif condition_node.relation == "#":
            if not (left == right):
                self.stack.append(1)
            else:
                self.stack.append(0)
        elif condition_node.relation == ">":
            if left > right:
                self.stack.append(1)
            else:
                self.stack.append(0)
        elif condition_node.relation == "<":
            if left < right:
                self.stack.append(1)
            else:
                self.stack.append(0)
        elif condition_node.relation == ">=":
            if left >= right:
                self.stack.append(1)
            else:
                self.stack.append(0)
        elif condition_node.relation == "<=":
            if left <= right:
                self.stack.append(1)
            else:
                self.stack.append(0)
        else:
            pass

    def visitVariableNode(self, var_node):
        self.stack.append(var_node.variable_name)

    def visitNumberNode(self, num_node):
        self.stack.append(num_node.constant.value)

    def visitReadNode(self, read_node):
        read_node.location.int_visit(self)
        box = self.get_box()
        string = sys.stdin.readline()
        try:
            number = int(string)
        except ValueError:
            sys.stderr.write("error: not a number")
            sys.exit(1)
        box.value = number

    def visitWriteNode(self, write_node):
        write_node.expression.int_visit(self)
        box = self.get_box()
        if isinstance(box, IntegerBox):
            value = box.get()
        else:
            value = box
        sys.stdout.write(str(value) + "\n")

    def visitIndexNode(self, index_node):
        index_node.location.int_visit(self)
        index_node.expression.int_visit(self)
        index = self.get_box()
        if isinstance(index, IntegerBox):
            index = index.get()
        array = self.get_box()
        try:
            if index < 0:
                raise IndexError
            val = array.value[index]
        except IndexError:
            sys.stderr.write("error: invalid index")
            sys.exit(1)
        self.stack.append(val)

    def visitBinaryNode(self, binary_node):
        """Interpret a binary tree."""
        operator_map = {"*":"*", "DIV":"/", "MOD":"%", "+":"+", "-":"-"}
        operator = operator_map[binary_node.operator]

        binary_node.exp_left.int_visit(self)
        binary_node.exp_right.int_visit(self)

        right = self.get_box()
        if isinstance(right, IntegerBox):
            right = right.get()
        left = self.get_box()
        if isinstance(left, IntegerBox):
            left = left.get()

        try:
            self.stack.append(int(eval(str(left) + str(operator) + str(right))))
        except ZeroDivisionError:
            sys.stderr.write("error: dividing by 0")
            sys.exit(1)

    def visitFieldNode(self, field_node):
        field_node.location.int_visit(self)
        field_node.variable.int_visit(self)
        name = self.stack.pop()
        record = self.get_box()
        self.stack.append(record.value.find(name))