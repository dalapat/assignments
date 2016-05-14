from Environment import Environment
import copy
from Integer import Integer
from CGIntegerBox import CGIntegerBox
from CGArrayBox import CGArrayBox
from CGRecordBox import CGRecordBox
from Variable import Variable

class CGSymbolTableVisitor:

    def __init__(self):
        self.env_size = 0

    def visitScope(self, scope):
        offset = 0
        for identifier in scope.symbol_table:
            a = scope.symbol_table[identifier]
            if isinstance(a, Variable):
                a.offset = offset
                a.size = a._type.ncg_visit(self)
                offset += a.size
        scope.size = offset
        return scope.size

    '''
    def visitScope(self, scope):
        environment = Environment()
        offset = 0
        flag = 0
        for identifier in scope.symbol_table:
            val = scope.symbol_table[identifier]

            if isinstance(val, Variable):
                box = val.ncg_visit(self)
                box.offset = offset
                environment.insert(identifier, box)
                #size = box.size
                offset += box.size
        environment.env_size = offset
        return environment
    '''

    def visitVar(self, variable_obj):
        return variable_obj._type.ncg_visit(self)

    def visitInt(self):
        return Integer().size

    def visitArray(self, array):
        unit_size = array._type.ncg_visit(self)
        array.unit_size = unit_size
        array.size = array.unit_size * array.length
        return array.size

    '''
    def visitArray(self, array):

        #array.unit_size = array._type.ncg_visit(self)
        array_type_box = array._type.ncg_visit(self)
        unit_size = array_type_box.size
        box_list = []
        offset = 0
        for i in range(array.length):
            if i == 0:
                # array_type_box.offset = offset
                box_list.append(array_type_box)
            else:
                box_list.append(copy.deepcopy(array_type_box))
            offset += array_type_box.size
        cgbox = CGArrayBox(box_list)
        cgbox.unit_size = array_type_box.size
        cgbox.length = array.length
        cgbox.size = offset

        #array.size = array.unit_size * array.get_length()
        return cgbox
    '''

    def visitRecord(self, record):
        record.scope.ncg_visit(self)
        size = record.scope.size
        return size
    '''
    def visitRecord(self, record):

        environment = record.scope.ncg_visit(self)
        rec_box = CGRecordBox(environment)
        rec_box.size = environment.env_size
        return rec_box
    '''