from Environment import Environment
from Variable import Variable
from IntegerBox import IntegerBox
from ArrayBox import ArrayBox
from RecordBox import RecordBox
import copy

class SymbolTableVisitor:

    def visitScope(self, scope):
        environment = Environment()
        for identifier in scope.symbol_table:
            val = scope.symbol_table[identifier]

            if isinstance(val, Variable):
                box = val.st_visit(self)
                environment.insert(identifier, box)
        return environment

    def visitVar(self, variable_obj):
        return variable_obj._type.st_visit(self)

    def visitInt(self):
        return IntegerBox()

    def visitArray(self, array):

        box = array._type.st_visit(self)

        box_list = []
        for i in range(array.length):
            if i == 0:
                box_list.append(box)
            else:
                box_list.append(copy.deepcopy(box))
        array_box = ArrayBox(box_list)
        return array_box

    def visitRecord(self, record):

        box = record.scope.st_visit(self)
        record_box = RecordBox(box)
        return record_box

