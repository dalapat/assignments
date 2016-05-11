import sys

class Observer:

    """
        Textual output to represent parsed token list
        using Observer pattern
    """

    # initializes an Observer with 0 space padding
    def __init__(self):
        self.indent = 0 # padding from left
        self.output_string = "" # textual output of parsed tokens

    # prints a token within the context of currently parsed tokens
    def print_token(self, token):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + str(token) + '\n'

    # prints Program within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_program(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Program" + '\n'
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_program(self):
        self.indent -= 2
        # print output string after checking error flag

    # prints Declarations within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_declarations(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Declarations" + '\n'
        # sys.stdout.write(pad_string + "Declarations" + '\n')
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_declarations(self):
        self.indent -= 2

    # prints ConstDecl within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_constdecl(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "ConstDecl" + '\n'
        # sys.stdout.write(pad_string + "ConstDecl" + '\n')
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_constdecl(self):
        self.indent -= 2

    # prints TypeDecl within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_typedecl(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "TypeDecl" + '\n'
        # sys.stdout.write(pad_string + "TypeDecl" + '\n')
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_typedecl(self):
        self.indent -= 2

    # prints VarDecl within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_vardecl(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "VarDecl" + '\n'
        # sys.stdout.write(pad_string + "VarDecl" + '\n')
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_vardecl(self):
        self.indent -= 2

    # prints BeginType within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_type(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Type" + '\n'
        # sys.stdout.write(pad_string + "Type" + '\n')
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_type(self):
        self.indent -= 2

    # prints Expression within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_expression(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Expression" + '\n'
        # sys.stdout.write(pad_string + "Expression" + '\n')
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_expression(self):
        self.indent -= 2

    # prints Term within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_term(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Term" + '\n'
        # sys.stdout.write(pad_string + "Term" + '\n')
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_term(self):
        self.indent -= 2

    # prints Factor within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_factor(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Factor" + '\n'
        # sys.stdout.write(pad_string + "Factor" + '\n')
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_factor(self):
        self.indent -= 2

    # prints Instructions within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_instructions(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Instructions" + '\n'
        # sys.stdout.write(pad_string + "Instructions" + '\n')
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_instructions(self):
        self.indent -= 2

    # prints Instruction within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_instruction(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Instruction" + '\n'
        # sys.stdout.write(pad_string + "Instruction" + '\n')
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_instruction(self):
        self.indent -= 2

    # prints Assign within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_assign(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Assign" + '\n'
        # sys.stdout.write(pad_string + "Assign" + '\n')
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_assign(self):
        self.indent -= 2

    # prints If within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_if(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "If" + '\n'
        # sys.stdout.write(pad_string + "If" + '\n')
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_if(self):
        self.indent -= 2

    # prints Repeat within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_repeat(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Repeat" + '\n'
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_repeat(self):
        self.indent -= 2

    # prints While within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_while(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "While" + '\n'
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_while(self):
        self.indent -= 2

    # prints Condition within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_condition(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Condition" + '\n'
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_condition(self):
        self.indent -= 2

    # prints Write within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_write(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Write" + '\n'
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_write(self):
        self.indent -= 2

    # prints Read within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_read(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Read" + '\n'
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_read(self):
        self.indent -= 2

    # prints Designator within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_designator(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Designator" + '\n'
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_designator(self):
        self.indent -= 2

    # prints Selector within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_selector(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "Selector" + '\n'
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_selector(self):
        self.indent -= 2

    # prints IdentifierList within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_identifier_list(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "IdentifierList" + '\n'
        self.indent += 2

    # decrements the indent by 2 to represent popping from call stack
    def end_identifier_list(self):
        self.indent -= 2

    # prints ExpressionList within the context of currently parsed tokens
    # indents padding by 2 to represent adding to call stack
    def begin_expression_list(self):
        pad_string = ""
        for _ in range(self.indent):
            pad_string += " "
        self.output_string += pad_string + "ExpressionList" + '\n'
        self.indent += 2

    # prints textual representation of parsed tokens
    def print_output(self):
        sys.stdout.write('\n' + self.output_string)

    # decrements the indent by 2 to represent popping from call stack
    def end_expression_list(self):
        self.indent -= 2
