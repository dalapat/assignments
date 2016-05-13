import sys
class ASTCGVisitor:

    def __init__(self, environment, ast):
        self.ast = ast
        self.environment = environment
        self.numif = 0
        self.output_string = ""
        self.num_loop = 0

    def cgwrite(self, string):
        self.output_string += "\t\t{0}\n".format(string)

    def start(self):
        self.cgwrite(".arch armv6")
        self.cgwrite(".fpu vfp")
        self.cgwrite(".align 2")
        self.cgwrite(".global main")
        self.cgwrite(".data")
        self.output_string += "vars:\t\t.space {0}\n".format(self.environment.env_size)
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

    def visitInstructions(self, head):
        while head is not None:
            head.ncg_visit(self)
            head = head._next

    def visitVariableNode(self, variable_node):
        self.cgwrite("add r2, r11, #{0}".format(self.environment.find(variable_node.variable_name).offset))
        self.cgwrite("push {r2}")
        return "location"

    def visitAssignNode(self, assign_node):
        assign_node.location.ncg_visit(self)
        s = assign_node.expression.ncg_visit(self)
        if s == "location":
            self.cgwrite("pop {r3}")
            self.cgwrite("ldr r3, [r3]")
            self.cgwrite("pop {r2}")
            self.cgwrite("str r3, [r2]")
        elif s == "number":
            self.cgwrite("pop {r3}")
            self.cgwrite("pop {r2}")
            self.cgwrite("str r3, [r2]")

    def visitIfNode(self, if_node):
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
        read_node.location.ncg_visit(self)
        self.cgwrite("pop {r1}")
        self.cgwrite("ldr r0, =scan_format")
        #self.cgwrite("mov r1, r2")
        self.cgwrite("bl scanf")

    def visitWriteNode(self, write_node):
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
        index_node.location.ncg_visit(self)
        s = index_node.expression.ncg_visit(self)
        if s == "location":
            self.cgwrite("pop {r2}")
            self.cgwrite("ldr r2, [r2]")
            self.cgwrite("push {r2}")
        self.cgwrite("ldr r3, ={0}".format(self.environment.
                                           find(index_node.location.variable_name).unit_size))
        self.cgwrite("pop {r2}")
        self.cgwrite("mul r2, r2, r3")
        self.cgwrite("push {r2}")
        self.cgwrite("pop {r2}")
        self.cgwrite("pop {r3}")
        self.cgwrite("add r2, r3, r2")
        self.cgwrite("push {r2}")
        return "location"

    def visitFieldNode(self, field_node):
        field_node.location.ncg_visit(self)
        field_node.variable.ncg_visit(self)
        self.cgwrite("pop {r2}")
        self.cgwrite("pop {r3}")
        self.cgwrite("add r2, r3, r2")
        self.cgwrite("push {r2}")
        return "location"

    def visitBinaryNode(self, binary_node):
        








