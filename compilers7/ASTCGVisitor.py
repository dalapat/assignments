import sys
from Array import Array
from Record import Record
from Integer import Integer
class ASTCGVisitor:

    #

    def __init__(self, environment, ast):
        self.ast = ast
        self.environment = environment
        self.numif = 0
        self.output_string = ""
        self.stack = []
        self.index_node_flag = 0
        self.num_loop = 0
        self.wordcopy = 0
        self.recordcopy = 0

    def cgwrite(self, string):
        self.output_string += "\t\t{0}\n".format(string)

    def start(self):
        self.cgwrite(".arch armv6")
        self.cgwrite(".fpu vfp")
        self.cgwrite(".align 2")
        self.cgwrite(".global main")
        self.cgwrite(".data")
        self.output_string += "vars:\t\t.space {0}\n".format(self.environment.size)
        #self.cgwrite(".space {0}".format(self.scope.stsize))
        self.output_string += "format:\t\t.asciz \"%d\\n\"\n" # does a dot need to be here
        self.output_string += "scan_format:\t\t.asciz\"%d\"\n"
        #self.cgwrite(".asciz \"%d\\n\"")
        self.cgwrite(".text")
        #self.cgwrite(".align 4")
        #self.cgwrite(".text")
        #self.cgwrite(".globl main")
        #self.cgwrite(".type main @fcn")
        self.output_string += "main:\n"
        self.cgwrite("ldr r11, =vars")
        self.visitInstructions(self.ast)
        self.cgwrite("bl exit")

    def cgoutput(self):
        f = open("test2.s", "w")
        f.write(self.output_string)
        f.close()

    def visitInstructions(self, head):
        while head is not None:
            head.ncg_visit(self)
            head = head._next

    def visitVariableNode(self, variable_node):
        self.cgwrite("@Variable")
        self.cgwrite("add r2, r11, #{0}".format(variable_node.variable.offset))
        self.cgwrite("push {r2}")
        return "location"

    def visitAssignNode(self, assign_node):
        self.cgwrite("@Assign")
        assign_node.location.ncg_visit(self)
        s = assign_node.expression.ncg_visit(self)
        if isinstance(assign_node.location.type, Integer) and \
                isinstance(assign_node.expression.type, Integer):

            if s == "location":
                self.cgwrite("pop {r3}")
                self.cgwrite("ldr r3, [r3]")
                self.cgwrite("pop {r2}")
                self.cgwrite("str r3, [r2]")
            elif s == "number":
                self.cgwrite("pop {r3}")
                self.cgwrite("pop {r2}")
                self.cgwrite("str r3, [r2]")
        elif isinstance(assign_node.location.type, Array) and \
                isinstance(assign_node.expression.type, Array):
            self.cgwrite("pop {r0}")
            self.cgwrite("pop {r1}")
            '''self.cgwrite("ldr r0, r2")
            self.cgwrite("ldr r1, r3")'''
            self.cgwrite("mov r2, #{0}".format(assign_node.expression.type.size))
            self.output_string += "wordcopy{0}:\n".format(self.wordcopy)
            #self.cgwrite("ldr r3, [r0], #{0}".format(assign_node.expression.type.unit_size))
            #self.cgwrite("str r3, [r1], #{0}".format(assign_node.expression.type.unit_size))
            self.cgwrite("ldr r3, [r0], #4")
            self.cgwrite("str r3, [r1], #4")
            self.cgwrite("subs r2, r2, #4")
            self.cgwrite("bne wordcopy{0}".format(self.wordcopy))
            self.wordcopy += 1
        elif isinstance(assign_node.location.type, Record) and \
            isinstance(assign_node.expression.type, Record):
            '''
            self.cgwrite("pop {r0}")
            self.cgwrite("pop {r1}")
            self.cgwrite("mov r2, #{0}".format(assign_node.expression.type.size))
            #self.output_string += "recordcopy{0}:\n".format(self.recordcopy)
            st = assign_node.expression.type.scope.symbol_table
            for field_identifier in st:
                fsize = st[field_identifier].size
                self.cgwrite("ldr r3, [r0], #{0}".format(fsize))
                self.cgwrite("str r3, [r1], #{0}".format(fsize))
                self.cgwrite("subs r2, r2, #{0}".format(fsize))
            '''

            self.cgwrite("pop {r0}")
            self.cgwrite("pop {r1}")
            self.cgwrite("mov r2, #{0}".format(assign_node.expression.type.scope.size))
            self.output_string += "recordcopy{0}:\n".format(self.recordcopy)
            self.cgwrite("ldr r3, [r0], #4")
            self.cgwrite("str r3, [r1], #4")
            self.cgwrite("subs r2, r2, #4")
            self.cgwrite("bne recordcopy{0}".format(self.recordcopy))
            self.recordcopy += 1


    def visitIfNode(self, if_node):
        self.cgwrite("@If")
        if_node.condition.ncg_visit(self)
        self.numif += 1
        local_numif = self.numif
        self.cgwrite("pop {r2}")
        self.cgwrite("cmp r2, #1")
        self.cgwrite("beq itrue{0}".format(local_numif))
        self.cgwrite("bne ifalse{0}".format(local_numif))
        ###
        self.output_string += "itrue{0}:\n".format(local_numif)
        self.visitInstructions(if_node.instructions_true)
        self.cgwrite("bl endif{0}".format(local_numif))
        self.output_string += "ifalse{0}:\n".format(local_numif)
        #if if_node.instructions_false is not None:
        self.visitInstructions(if_node.instructions_false)
        self.cgwrite("bl endif{0}".format(local_numif))
        self.output_string += "endif{0}:\n".format(local_numif)

    def visitConditionNode(self, condition_node):
        self.cgwrite("@Condition")
        s1 = condition_node.exp_left.ncg_visit(self)
        if s1 == "location":
            self.cgwrite("pop {r2}")
            self.cgwrite("ldr r2, [r2]")
            self.cgwrite("push {r2}")
        s2 = condition_node.exp_right.ncg_visit(self)
        if s2 == "location":
            self.cgwrite("pop {r2}")
            self.cgwrite("ldr r2, [r2]")
            self.cgwrite("push {r2}")
        self.cgwrite("pop {r2}")
        self.cgwrite("pop {r3}")
        self.cgwrite("cmp r3, r2")
        if condition_node.relation == "<":
            self.cgwrite("movlt r2, #1")
            self.cgwrite("movge r2, #0")
        elif condition_node.relation == ">":
            self.cgwrite("movgt r2, #1")
            self.cgwrite("movle r2, #0")
        elif condition_node.relation == "<=":
            self.cgwrite("movle r2, #1")
            self.cgwrite("movgt r2, #0")
        elif condition_node.relation == ">=":
            self.cgwrite("movge r2, #1")
            self.cgwrite("movlt r2, #0")
        elif condition_node.relation == "=":
            self.cgwrite("moveq r2, #1")
            self.cgwrite("movne r2, #0")
        elif condition_node.relation == "#":
            self.cgwrite("movne r2, #1")
            self.cgwrite("moveq r2, #0")
        else:
            sys.stderr.write("error: invalid condition")
            exit(1)
        self.cgwrite("push {r2}")

    def visitReadNode(self, read_node):
        self.cgwrite("@Read")
        read_node.location.ncg_visit(self)
        self.cgwrite("pop {r1}")
        self.cgwrite("ldr r0, =scan_format")
        #self.cgwrite("mov r1, r2")
        self.cgwrite("bl scanf")

    def visitWriteNode(self, write_node):
        self.cgwrite("@Write")
        s1 = write_node.expression.ncg_visit(self)
        if s1 == "location":
            self.cgwrite("pop {r2}")
            self.cgwrite("ldr r2, [r2]")
            self.cgwrite("push {r2}")
        self.cgwrite("pop {r1}")
        self.cgwrite("ldr r0, =format")
            #self.cgwrite("mov r1, r2")
        self.cgwrite("bl printf")

    def visitRepeatNode(self, repeat_node):
        self.cgwrite("@Repeat")
        self.num_loop += 1
        local_num_loop = self.num_loop
        self.output_string += "loop{0}:\n".format(local_num_loop)
        self.visitInstructions(repeat_node.instructions)
        repeat_node.condition.ncg_visit(self)
        self.cgwrite("pop {r2}")
        self.cgwrite("cmp r2, #0")
        self.cgwrite("beq loop{0}".format(local_num_loop))
        self.cgwrite("bne endloop{0}".format(local_num_loop))
        self.output_string += "endloop{0}:\n".format(local_num_loop)

    def visitIndexNode(self, index_node):
        self.cgwrite("@Index")
        index_node.location.ncg_visit(self)
        s = index_node.expression.ncg_visit(self)
        if s == "location":
            self.cgwrite("pop {r2}")
            self.cgwrite("ldr r2, [r2]")
            self.cgwrite("push {r2}")
        if isinstance(index_node.location.type, Array):
            self.cgwrite("ldr r3, ={0}".format(index_node.location.type.unit_size))
        elif isinstance(index_node.location.type, Record):
            self.cgwrite("ldr r3, ={0}".format(index_node.location.type.size))
        elif isinstance(index_node.location.type, Integer):
            self.cgwrite("ldr r3, ={0}".format(index_node.location.type.size))
        else:
            sys.stderr.write("error: type")
            exit(1)
        self.cgwrite("pop {r2}")
        self.cgwrite("mul r2, r2, r3")
        self.cgwrite("push {r2}")
        self.cgwrite("pop {r2}")
        self.cgwrite("pop {r3}")
        self.cgwrite("add r2, r3, r2")
        self.cgwrite("push {r2}")
        return "location"

    def visitNumberNode(self, number_node):
        self.cgwrite("@number")
        self.cgwrite("ldr r2, ={0}".format(number_node.constant.value))
        self.cgwrite("push {r2}")
        return "number"

    def visitFieldNode(self, field_node):
        self.cgwrite("@Field")
        field_node.location.ncg_visit(self)
        #field_node.variable.ncg_visit(self)
        self.cgwrite("ldr r2, ={0}".format(field_node.variable.variable.offset))
        self.cgwrite("push {r2}")
        self.cgwrite("pop {r2}")
        #self.cgwrite("ldr r2, [r2]")
        #self.cgwrite("push {r2}")
        #self.cgwrite("pop {r2}")
        self.cgwrite("pop {r3}")
        self.cgwrite("add r2, r3, r2")
        self.cgwrite("push {r2}")
        return "location"

    def visitBinaryNode(self, binary_node):
        self.cgwrite("@ binary")
        re = binary_node.exp_left.ncg_visit(self)
        if re == "location":
            self.cgwrite("pop {r2}")
            self.cgwrite("ldr r2, [r2]")
            self.cgwrite("push {r2}")
        le = binary_node.exp_right.ncg_visit(self)
        if le == "location":
            self.cgwrite("pop {r2}")
            self.cgwrite("ldr r2, [r2]")
            self.cgwrite("push {r2}")
        self.cgwrite("pop {r1}")
        self.cgwrite("pop {r0}")
        if binary_node.operator == "+":
            self.cgwrite("add r2, r0, r1")
            self.cgwrite("push {r2}")
        elif binary_node.operator == "-":
            self.cgwrite("sub r2, r0, r1")
            self.cgwrite("push {r2}")
        elif binary_node.operator == "*":
            self.cgwrite("mul r2, r0, r1")
            self.cgwrite("push {r2}")
        elif binary_node.operator == "DIV":
            self.cgwrite("bl __aeabi_idiv")
            self.cgwrite("push {r0}")
        elif binary_node.operator == "MOD":
            self.cgwrite("bl __aeabi_idivmod")
            self.cgwrite("push {r1}")
        else:
            pass
        return "number"









