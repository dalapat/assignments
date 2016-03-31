# from UnexpectedTokenException import UnexpectedTokenException
from Scanner import Scanner
from Token import Token
from Observer import Observer
###
from Scope import Scope
from Constant import Constant
from Integer import Integer, integerInstance
from Array import Array
from Record import Record
from Variable import Variable
from Type import Type
from ConditionNode import ConditionNode
from VariableNode import VariableNode
from IndexNode import IndexNode
from NumberNode import NumberNode
from BinaryNode import BinaryNode
from FieldNode import FieldNode
from AssignNode import AssignNode
from IfNode import IfNode
from RepeatNode import RepeatNode
from WriteNode import WriteNode
from ReadNode import ReadNode

from Visitor import Visitor
from ASTvisitor import ASTvisitor
import sys


class Parser:

    """Takes a list of tokens and performs semantic analysis
       to check if input adheres to grammar. Outputs to stdout
       a textual representation of the CST via the call stack.
       Parser is also capable of outputting graphical output
    """

    # initializes Parser instance and parses a list of tokens
    # cmd line arguments determine output type
    def __init__(self, observer = Observer(), token_list=[], print_symbol_table = 0, visitor = Visitor()):
        self.current = 0 # current position in token list
        self.token_list = token_list # token list received from scanner
        self.kind_map = Token.kind_map # dictionary of token kinds
        self.observer = observer # output class determined by cmd line arguments
        self.total_error_flag = 0 # detects if an error occurs anywhere in the program
        self.universe = Scope(None) # universe scope
        self.universe.insert("INTEGER", integerInstance) # universe scope only holds integer
        self.program_scope = Scope(self.universe) # program scope to hold program names
        self.current_scope = self.program_scope # current scope for switching between scopes
        self.print_symbol_table = print_symbol_table # determines whether to print cst or st
        self.visitor = visitor

    # parse the token list
    def parse(self):
        instructions = self._program()
        # do not print any output if error occurs
        if self.total_error_flag == 0:
            if self.print_symbol_table == 0:
                self.observer.print_output()
            elif self.print_symbol_table == 1:
                self.visitor.visitScope(self.program_scope)
                self.visitor.end()
            elif self.print_symbol_table == 2:
                currinstruction = instructions
                self.visitor.start()
                while(currinstruction is not None):
                    currinstruction.visit(self.visitor)
                    currinstruction = currinstruction._next

    # check if the currently parsed token is a token we are
    # expecting to find
    # kind = expected kind of token
    def match(self, kind):
        if self.token_list[self.current].kind == self.kind_map[kind]:
            self.observer.print_token(self.token_list[self.current])
            self.current += 1
            ### for returning identifier names
            return self.token_list[self.current-1].get_token_name()
        else:
            self.total_error_flag = 1
            sys.stderr.write("error: expected token kind \'{0}\', "
                             "received unexpected token \'{1}\'"
                             " @({2}, {3})".format(kind, self.token_list[self.current],
                                                   self.token_list[self.current].start_position,
                                                   self.token_list[self.current].end_position) + '\n')

    # set expectation of creating a program
    # by following the program production
    def _program(self):
        # print "Program"
        self.observer.begin_program()
        self.match("PROGRAM")
        name = self.match("IDENTIFIER")
        self.match(";")
        self._declarations()
        instructions = None
        if self.token_list[self.current].kind == self.kind_map["BEGIN"]:
            self.match("BEGIN")
            instructions = self._instructions()
        self.match("END")
        end_name = self.match("IDENTIFIER")
        self.match(".")
        self.observer.end_program()
        if not name == end_name:
            self.total_error_flag = 1
            sys.stderr.write("error: program identifier does not match end identifier\n")
        if not self.token_list[self.current].kind == self.kind_map["EOF"]:
            self.total_error_flag = 1
            sys.stderr.write("error: trash detected after program end:\n"
                             "Token \'{0}\'".format(self.token_list[self.current]) + '\n')
        return instructions

    # set expectation of creating a declaration
    # by following the declaration production
    def _declarations(self):
        self.observer.begin_declarations()
        while (self.token_list[self.current].kind == self.kind_map["CONST"]) or \
            (self.token_list[self.current].kind == self.kind_map["TYPE"]) or \
            (self.token_list[self.current].kind == self.kind_map["VAR"]):
            if self.token_list[self.current].kind == self.kind_map["CONST"]:
                self._constdecl()
            elif self.token_list[self.current].kind == self.kind_map["TYPE"]:
                self._typedecl()
            elif self.token_list[self.current].kind == self.kind_map["VAR"]:
                self._vardecl()
            else:
                pass
        self.observer.end_declarations()

    # set expectation of creating a ConstDecl
    # by following the ConstDecl production
    def _constdecl(self):
        # print "ConstDecl"
        self.observer.begin_constdecl()
        self.match("CONST")
        # return_obj = None
        while self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            name = self.match("IDENTIFIER")
            # check if const name in local scope
            if self.program_scope.local(name):
                self.total_error_flag = 1
                sys.stderr.write("error: attempted to redefine identifier\n")
            self.match("=")
            e = self._expression()
            if not isinstance(e, NumberNode):
                self.total_error_flag = 1
                sys.stderr.write("error: constdecl received nonconst exp\n")
                # exit(1)
            self.match(";")
            #return_obj = e
            # add it we formed a constant
            if isinstance(e.constant, Constant): # is it constant object or constant name
                self.program_scope.insert(name, e.constant)
            else:
                self.total_error_flag = 1
                sys.stderr.write("error: attempted to define const with nonconst object\n")
        self.observer.end_constdecl()
        # return return_obj

    # set expectation of creating a TypeDecl
    # by following the TypeDecl production
    def _typedecl(self):
        # print "TypeDecl"
        self.observer.begin_typedecl()
        self.match("TYPE")
        #return_type = None
        while self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            name = self.match("IDENTIFIER")
            self.match("=")
            # type of current Type
            return_type = self._type()
            self.match(";")
            if return_type is None:
                self.total_error_flag = 1
                sys.stderr.write("error: type not found\n")
                return None
            if not self.current_scope.local(name):
                self.current_scope.insert(name, return_type)
            else:
                self.total_error_flag = 1
                sys.stderr.write("error: attempting to redefine variable\n")
        self.observer.end_typedecl()
        # return return_type

    # set expectation of creating a VarDecl
    # by following the VarDecl production
    def _vardecl(self):
        # print "VarDecl"
        self.observer.begin_vardecl()
        self.match("VAR")
        id_list = []
        return_type = None
        while self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            id_list = self._identifier_list()
            self.match(":")
            return_type = self._type()
            # type of current identifier
            if return_type is None:
                self.total_error_flag = 1
                sys.stderr.write("error: type not found\n")
                return None
            self.match(";")
            for name in id_list:
                if not self.current_scope.local(name):
                    self.current_scope.insert(name, Variable(return_type))
                else:
                    self.total_error_flag = 1
                    sys.stderr.write("error: attempting to redefine var\n")
        self.observer.end_vardecl()
        return return_type

    # set expectation of creating a Type
    # by following the Type production
    def _type(self):
        # print "Type"
        self.observer.begin_type()
        return_type = None
        if self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            name = self.match("IDENTIFIER")
            # get the name of an identifier
            return_type = self.current_scope.find(name)
            if return_type is None:
                self.total_error_flag = 1
                sys.stderr.write("error: indentifier not found. attempting to assign "
                                 "uncreated type\n")
                self.observer.end_type()
                return None
            if isinstance(return_type, Type):
                self.observer.end_type()
                return return_type
            else:
                self.total_error_flag = 1
                sys.stderr.write("error: found not Type object\n")
                return None
        elif self.token_list[self.current].kind == self.kind_map["ARRAY"]:
            self.match("ARRAY")
            length = None
            e = self._expression()
            # get length of array
            # print "TYPE",
            if isinstance(e, NumberNode):
                # should it be assigned to actual value or number node?
                length = e.constant.value
            else:
                self.total_error_flag = 1
                sys.stderr.write("error: not a valid type for array length\n")
            self.match("OF")
            array_type = self._type()
            # check if array_type is already defined
            if array_type is None:
                self.total_error_flag = 1
                sys.stderr.write("error: array type not found\n")
                return None
            return_type = Array(length, array_type)
            self.observer.end_type()
            return return_type
        elif self.token_list[self.current].kind == self.kind_map["RECORD"]:
            self.match("RECORD")
            id_list = []
            outer_scope = self.current_scope
            self.current_scope = Scope(outer_scope)
            while self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
                id_list = self._identifier_list()
                self.match(":")
                # type of current identifier(s)
                record_field_type = self._type()
                if record_field_type is None:
                    self.total_error_flag = 1
                    sys.stderr.write("error: record field type nonexistent\n")
                self.match(";")
                for name in id_list:
                    if not self.current_scope.local(name):
                        self.current_scope.insert(name, Variable(record_field_type))
                    else:
                        self.total_error_flag = 1
                        sys.stderr.write("error: attempting to redefine field\n")
                        return None
            self.match("END")
            return_type = Record(self.current_scope)
            outer_scope = self.current_scope.outer_scope
            self.current_scope.outer_scope = None
            self.current_scope = outer_scope
            self.observer.end_type()
            return return_type
        else:
            self.total_error_flag = 1
            sys.stderr.out("error: expecting Identifier, ARRAY, or RECORD\n")
        self.observer.end_type()

    # set expectation of creating a Expression
    # by following the Expression production
    def _expression(self):
        self.observer.begin_expression()
        '''operation = -1
        if self.token_list[self.current].kind == self.kind_map["+"]:
            operation = self.match("+")
        elif self.token_list[self.current].kind == self.kind_map["-"]:
            operation = self.match("-")
        subtree = self._term()

        while (self.token_list[self.current].kind == self.kind_map["+"]) or \
                (self.token_list[self.current].kind == self.kind_map["-"]):
            if self.token_list[self.current].kind == self.kind_map["+"]:
                self.match("+")
            elif self.token_list[self.current].kind == self.kind_map["-"]:
                self.match("-")
            else:
                self.total_error_flag = 1
                sys.stderr.write("error: expecting \'+\' or \'-\'\n")
            self._term()'''
        node = self.nexpression()
        # node.to_string()
        self.observer.end_expression()
        # e = Constant(self.universe.find("INTEGER"), 5)
        # print "e", type(node)
        return node

    def nexpression(self):
        outer_operation = -1
        if self.token_list[self.current].kind == self.kind_map["+"]:
            outer_operation = self.match("+")
        elif self.token_list[self.current].kind == self.kind_map["-"]:
            outer_operation = self.match("-")
        subtree = self._term()
        node = subtree
        # if operation == '-':
        #    bn = BinaryNode(operation, NumberNode(Constant(integerInstance, 0)), subtree)
        if (self.token_list[self.current].kind == self.kind_map["+"]) or \
                (self.token_list[self.current].kind == self.kind_map["-"]):
            inner_operation = ""
            if self.token_list[self.current].kind == self.kind_map["+"]:
                inner_operation = self.match("+")
            elif self.token_list[self.current].kind == self.kind_map["-"]:
                inner_operation = self.match("-")
            else:
                self.total_error_flag = 1
                sys.stderr.write("error: expecting \'+\' or \'-\'\n")
            subtree_right = self._term()
            if isinstance(subtree, NumberNode) and isinstance(subtree_right, NumberNode):
                result = 0
                if inner_operation == "+":
                    result = int(subtree.type.value) + int(subtree_right.type.value)
                elif inner_operation == "-":
                    result = int(subtree.type.value) + int(subtree_right.type.value)
                else:
                    pass
                c = Constant(integerInstance, result)
                num_node = NumberNode(c)
                node = num_node
            else:
                bn = BinaryNode(inner_operation, subtree, subtree_right)
                node = bn
        else:
            node = subtree
        if outer_operation == "-":
            # how to do negative numbers?
            if isinstance(node, BinaryNode):
                if isinstance(node.exp_left, NumberNode) and isinstance(node.exp_right, NumberNode):
                    op = node.operator
                    left_value = node.exp_left.value
                    right_value = node.exp_right.value
                    op_result = 0
                    if op == "+":
                        op_result = left_value + right_value
                    elif op == "-":
                        op_result = left_value - right_value
                    elif op == "*":
                        op_result = left_value * right_value
                    elif op == "DIV":
                        op_result = left_value / right_value
                    elif op == "MOD":
                        op_result = left_value % right_value
                    else:
                        sys.stderr.write("error: invalid op")
                    result = -1*op_result
                    c = Constant(integerInstance, result)
                    num_node = NumberNode(c)
                    node = num_node
            elif isinstance(node, NumberNode):
                # node.constant.value = -1*node.constant.value
                c = Constant(integerInstance, 0 - node.constant.value)
                num_node = NumberNode(c)
                node = num_node
            # bn = BinaryNode(outer_operation,
                            #NumberNode(Constant(integerInstance, 0)), node)
            # node = bn
        return node

    # set expectation of creating a Term
    # by following the Term production
    def _term(self):
        self.observer.begin_term()
        '''operation = None
        subtree_left = self._factor()
        node = subtree_left
        while (self.token_list[self.current].kind == self.kind_map["*"])or \
            (self.token_list[self.current].kind == self.kind_map["DIV"]) or \
            (self.token_list[self.current].kind == self.kind_map["MOD"]):
            if self.token_list[self.current].kind == self.kind_map["*"]:
                 operation = self.match("*")
            elif self.token_list[self.current].kind == self.kind_map["DIV"]:
                 operation = self.match("DIV")
            elif self.token_list[self.current].kind == self.kind_map["MOD"]:
                 operation = self.match("MOD")
            else:
                self.total_error_flag = 1
                sys.stderr.out("error: expecting \'*\', \'DIV\', or \'MOD\'\n")
            subtree_right =  self._factor()
            temp = BinaryNode(operation, subtree_left, subtree_right)'''
        node = self.nterm()
        #return singular factor or binary node
        self.observer.end_term()
        return node

    def nterm(self):
        sub_left = self._factor()
        node = sub_left
        operation = 0
        if (self.token_list[self.current].kind == self.kind_map["*"])or \
            (self.token_list[self.current].kind == self.kind_map["DIV"]) or \
            (self.token_list[self.current].kind == self.kind_map["MOD"]):
            if self.token_list[self.current].kind == self.kind_map["*"]:
                 operation = self.match("*")
            elif self.token_list[self.current].kind == self.kind_map["DIV"]:
                 operation = self.match("DIV")
            elif self.token_list[self.current].kind == self.kind_map["MOD"]:
                 operation = self.match("MOD")
            else:
                self.total_error_flag = 1
                sys.stderr.out("error: expecting \'*\', \'DIV\', or \'MOD\'\n")
            sub_right = self.nterm()
            # originally had constant, changed it to integer
            if isinstance(sub_left, NumberNode) and isinstance(sub_right, NumberNode):
                result = 0
                if operation == "*":
                    result = int(sub_left.constant.value) * int(sub_right.constant.value)
                elif operation == "DIV":
                    result = int(sub_left.constant.value) / int(sub_right.constant.value)
                elif operation == "MOD":
                    result = int(sub_left.constant.value) % int(sub_right.constant.value)
                c = Constant(integerInstance, result)
                num_node = NumberNode(c)
                return num_node
            else:
                bn = BinaryNode(operation, sub_left, sub_right)
                return bn
        else:
            return sub_left

    # set expectation of creating a Factor
    # by following the Factor production
    def _factor(self):
        self.observer.begin_factor()
        node = None
        if self.token_list[self.current].kind == self.kind_map["INTEGER"]:
            int_value = self.match("INTEGER")
            c = Constant(integerInstance, int_value)
            node = NumberNode(c)
            # make a number node of out of the constant
            # return number node
        elif self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            sub_tree = self._designator()
            node = sub_tree
            #if not (isinstance(node, VariableNode) or isinstance(node, NumberNode)):
            #    sys.stderr.write("error: designator in factor")
        elif self.token_list[self.current].kind == self.kind_map["("]:
            self.match("(")
            sub_tree = self._expression()
            self.match(")")
            node = sub_tree
        else:
            self.total_error_flag = 1
            sys.stdout.error("error: expecting integer, identifier or \'(\'\n")
        self.observer.end_factor()
        return node

    # set expectation of creating a Instructions
    # by following the Instructions production
    def _instructions(self):
        self.observer.begin_instructions()
        head = self._instruction()
        curr = head
        while self.token_list[self.current].kind == self.kind_map[";"]:
            self.match(";")
            temp = self._instruction()
            curr._next = temp
            curr = temp
        self.observer.end_instructions()
        return head

    # set expectation of creating a Instruction
    # by following the Instruction production
    def _instruction(self):
        # print "Instruction"
        self.observer.begin_instruction()
        node = None
        if self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            node = self._assign()
        elif self.token_list[self.current].kind == self.kind_map["IF"]:
            node = self._if()
        elif self.token_list[self.current].kind == self.kind_map["REPEAT"]:
            node = self._repeat()
        elif self.token_list[self.current].kind == self.kind_map["WHILE"]:
            node = self._while()
        elif self.token_list[self.current].kind == self.kind_map["READ"]:
            node = self._read()
        elif self.token_list[self.current].kind == self.kind_map["WRITE"]:
            node = self._write()
        else:
            self.total_error_flag = 1
            sys.stderr.write("error: not a valid instruction\n"
                             "@({0}, {1})".format(self.token_list[self.current].start_position,
                                                  self.token_list[self.current].end_position))
        self.observer.end_instruction()
        return node

    # set expectation of creating a Assign
    # by following the Assign production
    def _assign(self):
        # print "Assign"
        self.observer.begin_assign()
        subtree_left = self._designator()
        # how do we check if its a variable?
        # it could be a field
        if not (isinstance(subtree_left, VariableNode) or isinstance(subtree_left, FieldNode)
                or isinstance(subtree_left, IndexNode)):
            print type(subtree_left)
            sys.stderr.write("error: assign")
        stl_type = subtree_left.type
        self.match(":=")
        subtree_right = self._expression()
        str_type = subtree_right.type
        if not type(stl_type) == type(str_type):
            sys.stderr.write("error: assigning things that don't have the same type")
        assign_node = AssignNode(None, subtree_left, subtree_right)
        self.observer.end_assign()
        return assign_node

    # set expectation of creating a If
    # by following the If production
    def _if(self):
        # print "If"
        self.observer.begin_if()
        self.match("IF")
        condition = self._condition()
        self.match("THEN")
        instructions_true = self._instructions()
        instructions_false = None
        if self.token_list[self.current].kind == self.kind_map["ELSE"]:
            self.match("ELSE")
            instructions_false = self._instructions()
        self.match("END")
        self.observer.end_if()
        if_node = IfNode(None, condition, instructions_true, instructions_false)
        return if_node

    # set expectation of creating a Repeat
    # by following the Repeat production
    def _repeat(self):
        self.observer.begin_repeat()
        self.match("REPEAT")
        instructions = self._instructions()
        self.match("UNTIL")
        condition = self._condition()
        self.match("END")
        self.observer.end_repeat()
        repeat_node = RepeatNode(None, condition, instructions)
        return repeat_node


    # set expectation of creating a While
    # by following the While production
    def _while(self):
        self.observer.begin_while()
        self.match("WHILE")
        condition = self._condition()
        self.match("DO")
        instructions = self._instructions()
        self.match("END")
        self.observer.end_while()
        negation_condition_node = self.get_negation(condition)
        repeat_node = RepeatNode(None, negation_condition_node, instructions)
        if_node = IfNode(None, condition, repeat_node, None)
        return if_node

    def get_negation(self, condition_node):
        relation_negation = {"=":"#",
                             "#":"=",
                             "<":">",
                             ">":"<",
                             "<=":">=",
                             ">=":"<="}
        negation_condition_node = ConditionNode(condition_node.exp_left, condition_node.exp_right,
                                                relation_negation[condition_node.relation])
        return negation_condition_node

    # set expectation of creating a Condition
    # by following the Condition production
    def _condition(self):
        self.observer.begin_condition()
        left = self._expression()
        relation = ""
        if self.token_list[self.current].kind == self.kind_map["="]:
             # self.match("=")
             relation = self.match("=")
        elif self.token_list[self.current].kind == self.kind_map["#"]:
             # self.match("#")
             relation = self.match("#")
        elif self.token_list[self.current].kind == self.kind_map["<"]:
             # self.match("<")
             relation = self.match("<")
        elif self.token_list[self.current].kind == self.kind_map[">"]:
            # self.match(">")
            relation = self.match(">")
        elif self.token_list[self.current].kind == self.kind_map["<="]:
            # self.match("<=")
            relation = self.match("<=")
        elif self.token_list[self.current].kind == self.kind_map[">="]:
            # self.match(">=")
            relation = self.match(">=")
        else:
            self.total_error_flag = 1
            sys.stderr.write("error: not a valid condition\n"
                             "@({0}, {1})".format(self.token_list[self.current].start_position,
                                                  self.token_list[self.current].end_position))
        right = self._expression()
        self.observer.end_condition()
        condition_subtree = ConditionNode(left, right, relation)
        return condition_subtree

    # set expectation of creating a Write
    # by following the Write production
    def _write(self):
        self.observer.begin_write()
        self.match("WRITE")
        expression = self._expression()
        if not isinstance(expression.type, Integer):
            self.total_error_flag = 1
            sys.stderr.write("error: expression in write not of type integer")
            #exit(1)
        self.observer.end_write()
        write_node = WriteNode(None, expression)
        return write_node

    # set expectation of creating a Read
    # by following the Read production
    def _read(self):
        self.observer.begin_read()
        self.match("READ")
        designator = self._designator()
        if not isinstance(designator.type, Integer):
            self.total_error_flag = 1
            sys.stderr.write("error: designator in read not an integer")
            #exit(1)
        self.observer.end_read()
        read_node = ReadNode(None, designator)
        return read_node

    # set expectation of creating a Designator
    # by following the Designator production
    def _designator(self):
        self.observer.begin_designator()
        var_name = self.match("IDENTIFIER")
        var_obj = self.program_scope.find(var_name)
        if not (isinstance(var_obj, Variable) or isinstance(var_obj, Constant)):
            # print "v", type(var_obj)
            sys.stderr.write("error: variable name not pointing var or const\n")
            # exit(1)
        if isinstance(var_obj, Constant):
            num_node = NumberNode(var_obj)
            # var_type = var_obj._type
            subtree = self._selector(num_node)
            self.observer.end_designator()
            return subtree
        if isinstance(var_obj._type, Integer):
            var_type = var_obj._type
        elif isinstance(var_obj._type, Array):
            var_type = var_obj._type._type
        elif isinstance(var_obj._type, Record):
            var_type = var_obj._type
        else:
            sys.stderr.write("error: designator\n")
        # var_type = var_obj._type
        # what type should go here? should i distinguish by possible types?
        # var_type = var_obj._type._type
        # print "vt", type(var_type)
        #print "vo", type(var_obj)
        var_node = VariableNode(var_type, var_obj, var_name)
        subtree = self._selector(var_node)
        self.observer.end_designator()
        return subtree

    # set expectation of creating a Selector
    # by following the Selector production
    def _selector(self, variable_node):
        self.observer.begin_selector()
        return_object = variable_node
        while (self.token_list[self.current].kind == self.kind_map["["]) \
                or (self.token_list[self.current].kind == self.kind_map["."]):
            if self.token_list[self.current].kind == self.kind_map["["]:
                self.match("[")
                exp_list = self._expression_list()
                self.match("]")
                # check if it's an array
                if not isinstance(return_object.variable._type, Array):
                    sys.stderr.write("error: not an array")
                node = return_object
                for e in exp_list:
                    #if not isinstance(e, NumberNode):
                    if not isinstance(e.type, Integer):
                        sys.stderr.write("error: nonconstant found in selector\n")
                # type refers to the type of the variable node
                # what should the type be here??
                index_type = return_object.type
                # print "it", type(index_type)
                # print "index type: ", type(index_type)
                index_node = IndexNode(index_type, node, exp_list[0])
                for i in range(1, len(exp_list)):
                    node = index_node
                    index_type = node.type
                    index_node = IndexNode(index_type, node, exp_list[i])
                return_object = index_node
            elif self.token_list[self.current].kind == self.kind_map["."]:
                # how to make field
                self.match(".")
                field_var_name = self.match("IDENTIFIER")
                # throws an error on field_var because it gets an index node
                # and can't find variable attribute
                if not isinstance(return_object.type, Record):
                    # sys.stdout.write("TYPE1: " + str(type(return_object)) + "\n")
                    # sys.stdout.write("return_object.type: " + str(type(return_object.type)) + "\n")
                    sys.stderr.write("error: attempting to select field from non-record type\n")
                if isinstance(return_object, VariableNode):
                    if(return_object.variable.type.scope.local(field_var_name)):
                        # local doesn't return, should it?
                        field_var_obj = return_object.variable.type.scope.find(field_var_name)
                elif isinstance(return_object, IndexNode) or isinstance(return_object, FieldNode):
                    if(return_object.location.type.scope.local(field_var_name)):
                        field_var_obj = return_object.location.type.scope.find(field_var_name)
                else:
                    sys.stderr.write("error: selector\n")
                # field_var_obj = return_object.variable._type.local(field_var_name)
                field_type = field_var_obj._type
                field_right_var_obj = VariableNode(field_type, field_var_obj, field_var_name)
                node = FieldNode(field_type, return_object, field_right_var_obj)
                return_object = node
            else:
                self.total_error_flag = 1
                sys.stderr.write("error: not a valid selector\n"
                             "@({0}, {1})".format(self.token_list[self.current].start_position,
                                                  self.token_list[self.current].end_position))
        self.observer.end_selector()
        return return_object

    # set expectation of creating a IdentifierList
    # by following the IdentifierList production
    def _identifier_list(self):
        self.observer.begin_identifier_list()
        name = self.match("IDENTIFIER")
        id_list = []
        id_list.append(name)
        while self.token_list[self.current].kind == self.kind_map[","]:
            self.match(",")
            name = self.match("IDENTIFIER")
            id_list.append(name)
        self.observer.end_identifier_list()
        return id_list

    # set expectation of creating a ExpressionList
    # by following the ExpressionList production
    def _expression_list(self):
        # return list of expressions - added return in assignment 5
        self.observer.begin_expression_list()
        exp_list = []
        name = self._expression()
        exp_list.append(name)
        while self.token_list[self.current].kind == self.kind_map[","]:
            self.match(",")
            name = self._expression()
            exp_list.append(name)
        self.observer.end_expression_list()
        return exp_list

'''
def main():
    f = open("../compilers4/test2.txt")
    input_string = ""
    for line in f:
        input_string += line
    # print input_string
    f.close()
    s = Scanner(input_string)
    token_list = s.all()
    p = Parser(token_list=token_list, print_symbol_table=2, visitor=ASTvisitor())
    p.parse()

main()
'''