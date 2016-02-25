import sys
class DotObserver:

    def __init__(self):
        self.stack = []
        self.output_string = ""
        self.node_count = 0

    def print_token(self, token):
        self.output_string += "L{0} [label=\"{1}\", " \
                              "shape=diamond]\n".format(self.node_count,
                                                        str(token.get_token_name()))
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.node_count += 1

    def begin_program(self):
        self.output_string += "strict digraph CST {"
        self.output_string += "L{0} [label=\"Program\", " \
                              "shape=box]\n".format(self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_program(self):
        self.stack = self.stack[:-1]
        self.output_string += "}\n"

    def begin_declarations(self):
        self.output_string += "L{0} [label=\"Declarations\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_declarations(self):
        self.stack = self.stack[:-1]

    def begin_constdecl(self):
        self.output_string += "L{0} [label=\"ConstDecl\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_constdecl(self):
        self.stack = self.stack[:-1]

    def begin_typedecl(self):
        self.output_string += "L{0} [label=\"TypeDecl\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_typedecl(self):
        self.stack = self.stack[:-1]

    def begin_vardecl(self):
        self.output_string += "L{0} [label=\"VarDecl\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_vardecl(self):
        self.stack = self.stack[:-1]

    def begin_type(self):
        self.output_string += "L{0} [label=\"Type\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_type(self):
        self.stack = self.stack[:-1]

    def begin_expression(self):
        self.output_string += "L{0} [label=\"Expression\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_expression(self):
        self.stack = self.stack[:-1]

    def begin_term(self):
        self.output_string += "L{0} [label=\"Term\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_term(self):
        self.stack = self.stack[:-1]

    def begin_factor(self):
        self.output_string += "L{0} [label=\"Factor\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_factor(self):
        self.stack = self.stack[:-1]

    def begin_instructions(self):
        self.output_string += "L{0} [label=\"Instructions\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_instructions(self):
        self.stack = self.stack[:-1]

    def begin_instruction(self):
        self.output_string += "L{0} [label=\"Instruction\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_instruction(self):
        self.stack = self.stack[:-1]

    def begin_assign(self):
        self.output_string += "L{0} [label=\"Assign\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_assign(self):
        self.stack = self.stack[:-1]

    def begin_if(self):
        self.output_string += "L{0} [label=\"If\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_if(self):
        self.stack = self.stack[:-1]

    def begin_repeat(self):
        self.output_string += "L{0} [label=\"Repeat\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_repeat(self):
        self.stack = self.stack[:-1]

    def begin_while(self):
        self.output_string += "L{0} [label=\"While\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_while(self):
        self.stack = self.stack[:-1]

    def begin_condition(self):
        self.output_string += "L{0} [label=\"Condition\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_condition(self):
        self.stack = self.stack[:-1]

    def begin_write(self):
        self.output_string += "L{0} [label=\"Write\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_write(self):
        self.stack = self.stack[:-1]

    def begin_read(self):
        self.output_string += "L{0} [label=\"Read\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_read(self):
        self.stack = self.stack[:-1]

    def begin_designator(self):
        self.output_string += "L{0} [label=\"Designator\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_designator(self):
        self.stack = self.stack[:-1]

    def begin_selector(self):
        self.output_string += "L{0} [label=\"Selector\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_selector(self):
        self.stack = self.stack[:-1]

    def begin_identifier_list(self):
        self.output_string += "L{0} [label=\"IdentifierList\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_identifier_list(self):
        self.stack = self.stack[:-1]

    def begin_expression_list(self):
        self.output_string += "L{0} [label=\"ExpressionList\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def print_output(self):
        sys.stdout.write(self.output_string)

    def end_expression_list(self):
        self.stack = self.stack[:-1]