# Eric Calder
# ecalder6@jhu.edu

import copy
from Constant import Constant
from Variable import Variable
from Type import Type
from Array import Array
from Record import Record
from Scope import Scope
from Integer import Integer
from Environment import Environment
from ArrayBox import ArrayBox
from RecordBox import RecordBox
from IntegerBox import IntegerBox

# Visitor that creates boxes for entries in symbol table
class SymbolTableVisitor:
    def visit_var(self, var):
        """Create box for varialbe."""
        return var.type.accept(self)

    def visit_field(self, field):
        """Create box for field."""
        return field.type.accept(self)

    def visit_integer(self, field):
        """Create box for field."""
        return IntegerBox()

    def visit_array(self, array):
        """Create box for array."""
        box = array.element_type.accept(self)

        boxes = []
        for i in range(array.length):
            if i == 0:
                boxes.append(box)
            else:
                boxes.append(copy.deepcopy(box))

        array_box = ArrayBox(boxes)
        return array_box

    def visit_record(self, record):
        """Create box for record."""
        box = record.scope.accept(self)

        record_box = RecordBox(box)

        return record_box

    def visit_scope(self, scope):
        """Create box for scope."""
        env = Environment()
        for key in scope.table:
            val = scope.table[key]

            if not isinstance(val, Variable):
                # Do not store constants or types in env
                continue
            else:
                box = val.accept(self)
                env.insert(key, box)

        return env