# Eric Calder
# ecalder6@jhu.edu

import copy
import sys
from TextVisitor import TextVisitor
from Constant import Constant
from Integer import Integer
from Array import Array
from Record import Record
from Location import Location
from IntegerBox import IntegerBox
from ArrayBox import ArrayBox
from RecordBox import RecordBox
from Box import Box
from Error import *

# Visitor that creates the text output for AST.
class ASTInterpreterVisitor:
    def __init__(self):
        self.stack = []
        self.env = None
        self.tree = None

    def display(self):
        """Called by the parser."""
        self.visit_instructions(self.tree)

    def pop_box(self):
        """Pop a box from stack."""
        box = self.stack.pop()

        if isinstance(box, int):
            # Return all integers popped.
            return box
        if not isinstance(box, Box):
            # Find the box in the environment and return the box.
            box = self.env.find(box)
        return box

    def runtime_error(self, error):
        """Print the error message and stop the interpreter."""
        sys.stderr.write(error.message + "\n")
        sys.exit(1)

    def visit_instructions(self, instruction):
        """Interpret a list of instructions."""
        while instruction != None:
            instruction.accept(self)
            instruction = instruction.next

    def visit_assign(self, assign):
        """Interpret an assign tree."""
        assign.location.accept(self)
        assign.expression.accept(self)

        value_box = self.pop_box()
        box = self.pop_box()

        if isinstance(value_box, ArrayBox) or isinstance(value_box, RecordBox):
            value = copy.deepcopy(value_box.value)
        elif isinstance(value_box, IntegerBox):
            value = value_box.value
        else:
            # value is an integer
            value = value_box

        box.value = value

    def visit_if(self, if_ins):
        """Interpret an if tree."""
        if_ins.condition.accept(self)
        condition = self.stack.pop()

        if condition:
            self.visit_instructions(if_ins.instructions_true)
        else:
            self.visit_instructions(if_ins.instructions_false)

    def visit_repeat(self, repeat):
        """Interpret a repeat tree."""
        while True:
            self.visit_instructions(repeat.instructions)
            repeat.condition.accept(self)
            condition = self.stack.pop()

            if condition:
                break

    def visit_read(self, read):
        """Interpret a read tree."""
        read.location.accept(self)
        box = self.pop_box()
        string = sys.stdin.readline()
        try:
            number = int(string)
        except ValueError:
            # Invalid input error.
            error = InvalidInputForRead(string, read.token)
            self.runtime_error(error)

        box.value = number

    def visit_write(self, write):
        """Interpret a write tree."""
        write.expression.accept(self)
        box = self.pop_box()
        if isinstance(box, IntegerBox):
            value = box.value
        else:
            value = box
        print(str(value))

    def visit_number(self, number):
        """Push the number onto the stack."""
        self.stack.append(number.entry.value)

    def visit_binary(self, binary):
        """Interpret a binary tree."""
        operator_map = {"*":"*", "DIV":"/", "MOD":"%", "+":"+", "-":"-"}
        operator = operator_map[binary.operator]

        binary.left.accept(self)
        binary.right.accept(self)

        right = self.pop_box()
        if isinstance(right, IntegerBox):
            right = right.value
        left = self.pop_box()
        if isinstance(left, IntegerBox):
            left = left.value

        try:
            # Evaluate the operation.
            self.stack.append(int(eval(str(left) + str(operator) + str(right))))
        except ZeroDivisionError:
            # Divide by 0 error.
            error = DivideByZero(binary.token)
            self.runtime_error(error)

    def visit_variableAST(self, variableAST):
        """Push a varialbe onto the stack."""
        self.stack.append(variableAST.name)

    def visit_index(self, index):
        """Interpret an index tree."""
        index.location.accept(self)
        index.expression.accept(self)

        i = self.pop_box()
        if isinstance(i, IntegerBox):
            i = i.value
        array = self.pop_box()

        try:
            if i < 0:
                raise IndexError
            val = array.value[i]
        except IndexError:
            # Invalid array index.
            error = InvalidArrayIndex(i, len(array.value), index.token)
            self.runtime_error(error)

        self.stack.append(val)

    def visit_fieldAST(self, fieldAST):
        """Interpret a field tree."""
        fieldAST.location.accept(self)
        fieldAST.variable.accept(self)

        # Use the name string (not a box) to find the desired field.
        name = self.stack.pop()
        record = self.pop_box()

        self.stack.append(record.value.find(name))

    def visit_condition(self, condition):
        """Interpret a condition tree."""
        relation_map = {"=":"==", "#":"!=", ">":">", "<":"<",
                        ">=":">=", "<=":"<="}

        relation = relation_map[condition.relation]

        condition.left.accept(self)
        condition.right.accept(self)

        right = self.pop_box()
        if isinstance(right, IntegerBox):
            right = right.value
        left = self.pop_box()
        if isinstance(left, IntegerBox):
            left = left.value

        # Evaluate the condition.
        self.stack.append(eval(str(left) + str(relation) + str(right)))