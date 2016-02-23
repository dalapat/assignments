import sys

class Observer:

    def __init__(self):
        self.indent = 0

    def print_token(self, token):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + str(token) + "\n")

    def begin_program(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Program" + '\n')
        self.indent += 2


    def end_program(self):
        self.indent -= 2

    def begin_declarations(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Declarations" + '\n')
        self.indent += 2

    def end_declarations(self):
        self.indent -= 2

    def begin_constdecl(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "ConstDecl" + '\n')
        self.indent += 2

    def end_constdecl(self):
        self.indent -= 2

    def begin_typedecl(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "TypeDecl" + '\n')
        self.indent += 2

    def end_typedecl(self):
        self.indent -= 2

    def begin_vardecl(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "VarDecl" + '\n')
        self.indent += 2

    def end_vardecl(self):
        self.indent -= 2

    def begin_type(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Type" + '\n')
        self.indent += 2

    def end_type(self):
        self.indent -= 2

    def begin_expression(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Expression" + '\n')
        self.indent += 2

    def end_expression(self):
        self.indent -= 2

    def begin_term(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Term" + '\n')
        self.indent += 2

    def end_term(self):
        self.indent -= 2

    def begin_factor(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Factor" + '\n')
        self.indent += 2

    def end_factor(self):
        self.indent -= 2

    def begin_instructions(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Instructions" + '\n')
        self.indent += 2

    def end_instructions(self):
        self.indent -= 2

    def begin_instruction(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Instruction" + '\n')
        self.indent += 2

    def end_instruction(self):
        self.indent -= 2

    def begin_assign(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Assign" + '\n')
        self.indent += 2

    def end_assign(self):
        self.indent -= 2

    def begin_if(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "If" + '\n')
        self.indent += 2

    def end_if(self):
        self.indent -= 2

    def begin_repeat(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Repeat" + '\n')
        self.indent += 2

    def end_repeat(self):
        self.indent -= 2

    def begin_while(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "While" + '\n')
        self.indent += 2

    def end_while(self):
        self.indent -= 2

    def begin_condition(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Condition" + '\n')
        self.indent += 2

    def end_condition(self):
        self.indent -= 2

    def begin_write(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Write" + '\n')
        self.indent += 2

    def end_write(self):
        self.indent -= 2

    def begin_read(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Read" + '\n')
        self.indent += 2

    def end_read(self):
        self.indent -= 2

    def begin_designator(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Designator" + '\n')
        self.indent += 2

    def end_designator(self):
        self.indent -= 2

    def begin_selector(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "Selector" + '\n')
        self.indent += 2

    def end_selector(self):
        self.indent -= 2

    def begin_identifier_list(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "IdentifierList" + '\n')
        self.indent += 2

    def end_identifier_list(self):
        self.indent -= 2

    def begin_expression_list(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        sys.stdout.write(pad_string + "ExpressionList" + '\n')
        self.indent += 2

    def end_expression_list(self):
        self.indent -= 2
