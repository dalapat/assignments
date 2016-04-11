import sys
class DotObserver:

    """
        Graphical output to represent parsed token list
        using Observer pattern
    """

    # initializes an observer with empty node stack
    def __init__(self):
        self.stack = [] # node stack to assist with connecting subtrees
        self.output_string = "" # stores dot language cmds to create graph
        self.node_count = 0 # keeps track of names of nodes in tree

    # prints dot language cmds for creating terminal token node within the context of currently parsed tokens
    def print_token(self, token):
        self.output_string += "L{0} [label=\"{1}\", " \
                              "shape=diamond]\n".format(self.node_count,
                                                        str(token.get_token_name()))
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.node_count += 1

    # prints dot language cmds for Program node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_program(self):
        self.output_string += "strict digraph CST {"
        self.output_string += "L{0} [label=\"Program\", " \
                              "shape=box]\n".format(self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack and closes graph function in dot langauge
    def end_program(self):
        self.stack = self.stack[:-1]
        self.output_string += "}\n"

    # prints dot language cmds for Declarations node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_declarations(self):
        self.output_string += "L{0} [label=\"Declarations\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_declarations(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for ConstDecl node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_constdecl(self):
        self.output_string += "L{0} [label=\"ConstDecl\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_constdecl(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for TypeDecl node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_typedecl(self):
        self.output_string += "L{0} [label=\"TypeDecl\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_typedecl(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for VarDecl node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_vardecl(self):
        self.output_string += "L{0} [label=\"VarDecl\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_vardecl(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Type node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_type(self):
        self.output_string += "L{0} [label=\"Type\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    def end_type(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Expression node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_expression(self):
        self.output_string += "L{0} [label=\"Expression\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_expression(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Term node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_term(self):
        self.output_string += "L{0} [label=\"Term\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_term(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Factor node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_factor(self):
        self.output_string += "L{0} [label=\"Factor\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_factor(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Instructions node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_instructions(self):
        self.output_string += "L{0} [label=\"Instructions\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_instructions(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Instruction node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_instruction(self):
        self.output_string += "L{0} [label=\"Instruction\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_instruction(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Assign node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_assign(self):
        self.output_string += "L{0} [label=\"Assign\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_assign(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for If node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_if(self):
        self.output_string += "L{0} [label=\"If\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_if(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Repeat node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_repeat(self):
        self.output_string += "L{0} [label=\"Repeat\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_repeat(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for While node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_while(self):
        self.output_string += "L{0} [label=\"While\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_while(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Condition node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_condition(self):
        self.output_string += "L{0} [label=\"Condition\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_condition(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Write node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_write(self):
        self.output_string += "L{0} [label=\"Write\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_write(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Read node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_read(self):
        self.output_string += "L{0} [label=\"Read\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_read(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Designator node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_designator(self):
        self.output_string += "L{0} [label=\"Designator\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_designator(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for Selector node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_selector(self):
        self.output_string += "L{0} [label=\"Selector\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_selector(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for IdentifierList node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_identifier_list(self):
        self.output_string += "L{0} [label=\"IdentifierList\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # pops node from node stack
    def end_identifier_list(self):
        self.stack = self.stack[:-1]

    # prints dot language cmds for ExpressionList node within the context of currently parsed tokens
    # indents node count by 1 to keep track of nodes added to graph
    def begin_expression_list(self):
        self.output_string += "L{0} [label=\"ExpressionList\", " \
                              "shape=box]\n".format(self.node_count)
        self.output_string += "{0} -> L{1}\n".format(self.stack[len(self.stack)-1], self.node_count)
        self.stack.append("L{0}".format(self.node_count))
        self.node_count += 1

    # print dot cmds for forming graph
    def print_output(self):
        sys.stdout.write(self.output_string)

    # pops node from node stack
    def end_expression_list(self):
        self.stack = self.stack[:-1]