# from UnexpectedTokenException import UnexpectedTokenException
from Scanner import Scanner
from Token import Token
from Observer import Observer
###
from Scope import Scope
from Constant import Constant
from Integer import Integer
from Array import Array
from Record import Record
from Variable import Variable
from Type import Type

from Visitor import Visitor
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
        self.universe.insert("INTEGER", Integer()) # universe scope only holds integer
        self.program_scope = Scope(self.universe) # program scope to hold program names
        self.current_scope = self.program_scope # current scope for switching between scopes
        self.print_symbol_table = print_symbol_table # determines whether to print cst or st
        self.visitor = visitor

    # parse the token list
    def parse(self):
        self._program()
        # do not print any output if error occurs
        if self.total_error_flag == 0:
            if self.print_symbol_table == 0:
                self.observer.print_output()
            elif self.print_symbol_table == 1:
                self.visitor.visitScope(self.program_scope)
                self.visitor.end()

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
        if self.token_list[self.current].kind == self.kind_map["BEGIN"]:
            self.match("BEGIN")
            self._instructions()
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
        while self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            name = self.match("IDENTIFIER")
            # check if const name in local scope
            if self.program_scope.local(name):
                self.total_error_flag = 1
                sys.stderr.write("error: attempted to redefine identifier\n")
            self.match("=")
            e = self._expression()
            self.match(";")
            # add it we formed a constant
            if isinstance(e, Constant): # is it constant object or constant name
                self.program_scope.insert(name, e)
            else:
                self.total_error_flag = 1
                sys.stderr.write("error: attempted to define const with nonconst object\n")
        self.observer.end_constdecl()

    # set expectation of creating a TypeDecl
    # by following the TypeDecl production
    def _typedecl(self):
        # print "TypeDecl"
        self.observer.begin_typedecl()
        self.match("TYPE")
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
            if isinstance(e, Constant):
                length = e
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
        if self.token_list[self.current].kind == self.kind_map["+"]:
            self.match("+")
        elif self.token_list[self.current].kind == self.kind_map["-"]:
            self.match("-")
        self._term()
        while (self.token_list[self.current].kind == self.kind_map["+"]) or \
                (self.token_list[self.current].kind == self.kind_map["-"]):
            if self.token_list[self.current].kind == self.kind_map["+"]:
                self.match("+")
            elif self.token_list[self.current].kind == self.kind_map["-"]:
                self.match("-")
            else:
                self.total_error_flag = 1
                sys.stderr.write("error: expecting \'+\' or \'-\'\n")
            self._term()
        self.observer.end_expression()
        e = Constant(self.universe.find("INTEGER"), 5)
        return e

    # set expectation of creating a Term
    # by following the Term production
    def _term(self):
        self.observer.begin_term()
        self._factor()
        while (self.token_list[self.current].kind == self.kind_map["*"])or \
            (self.token_list[self.current].kind == self.kind_map["DIV"]) or \
            (self.token_list[self.current].kind == self.kind_map["MOD"]):
            if self.token_list[self.current].kind == self.kind_map["*"]:
                self.match("*")
            elif self.token_list[self.current].kind == self.kind_map["DIV"]:
                self.match("DIV")
            elif self.token_list[self.current].kind == self.kind_map["MOD"]:
                self.match("MOD")
            else:
                self.total_error_flag = 1
                sys.stderr.out("error: expecting \'*\', \'DIV\', or \'MOD\'\n")
            self._factor()
        self.observer.end_term()

    # set expectation of creating a Factor
    # by following the Factor production
    def _factor(self):
        self.observer.begin_factor()
        if self.token_list[self.current].kind == self.kind_map["INTEGER"]:
            self.match("INTEGER")
        elif self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            self._designator()
        elif self.token_list[self.current].kind == self.kind_map["("]:
            self.match("(")
            self._expression()
            self.match(")")
        else:
            self.total_error_flag = 1
            sys.stdout.error("error: expecting integer, identifier or \'(\'\n")
        self.observer.end_factor()

    # set expectation of creating a Instructions
    # by following the Instructions production
    def _instructions(self):
        self.observer.begin_instructions()
        self._instruction()
        while self.token_list[self.current].kind == self.kind_map[";"]:
            self.match(";")
            self._instruction()
        self.observer.end_instructions()

    # set expectation of creating a Instruction
    # by following the Instruction production
    def _instruction(self):
        # print "Instruction"
        self.observer.begin_instruction()
        if self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            self._assign()
        elif self.token_list[self.current].kind == self.kind_map["IF"]:
            self._if()
        elif self.token_list[self.current].kind == self.kind_map["REPEAT"]:
            self._repeat()
        elif self.token_list[self.current].kind == self.kind_map["WHILE"]:
            self._while()
        elif self.token_list[self.current].kind == self.kind_map["READ"]:
            self._read()
        elif self.token_list[self.current].kind == self.kind_map["WRITE"]:
            self._write()
        else:
            self.total_error_flag = 1
            sys.stderr.write("error: not a valid instruction\n"
                             "@({0}, {1})".format(self.token_list[self.current].start_position,
                                                  self.token_list[self.current].end_position))
        self.observer.end_instruction()

    # set expectation of creating a Assign
    # by following the Assign production
    def _assign(self):
        # print "Assign"
        self.observer.begin_assign()
        self._designator()
        self.match(":=")
        self._expression()
        self.observer.end_assign()

    # set expectation of creating a If
    # by following the If production
    def _if(self):
        # print "If"
        self.observer.begin_if()
        self.match("IF")
        self._condition()
        self.match("THEN")
        self._instructions()
        if self.token_list[self.current].kind == self.kind_map["ELSE"]:
            self.match("ELSE")
            self._instructions()
        self.match("END")
        self.observer.end_if()

    # set expectation of creating a Repeat
    # by following the Repeat production
    def _repeat(self):
        self.observer.begin_repeat()
        self.match("REPEAT")
        self._instructions()
        self.match("UNTIL")
        self._condition()
        self.match("END")
        self.observer.end_repeat()

    # set expectation of creating a While
    # by following the While production
    def _while(self):
        self.observer.begin_while()
        self.match("WHILE")
        self._condition()
        self.match("DO")
        self._instructions()
        self.match("END")
        self.observer.end_while()

    # set expectation of creating a Condition
    # by following the Condition production
    def _condition(self):
        self.observer.begin_condition()
        self._expression()
        if self.token_list[self.current].kind == self.kind_map["="]:
            self.match("=")
        elif self.token_list[self.current].kind == self.kind_map["#"]:
            self.match("#")
        elif self.token_list[self.current].kind == self.kind_map["<"]:
            self.match("<")
        elif self.token_list[self.current].kind == self.kind_map[">"]:
            self.match(">")
        elif self.token_list[self.current].kind == self.kind_map["<="]:
            self.match("<=")
        elif self.token_list[self.current].kind == self.kind_map[">="]:
            self.match(">=")
        else:
            self.total_error_flag = 1
            sys.stderr.write("error: not a valid condition\n"
                             "@({0}, {1})".format(self.token_list[self.current].start_position,
                                                  self.token_list[self.current].end_position))
        self._expression()
        self.observer.end_condition()

    # set expectation of creating a Write
    # by following the Write production
    def _write(self):
        self.observer.begin_write()
        self.match("WRITE")
        self._expression()
        self.observer.end_write()

    # set expectation of creating a Read
    # by following the Read production
    def _read(self):
        self.observer.begin_read()
        self.match("READ")
        self._designator()
        self.observer.end_read()

    # set expectation of creating a Designator
    # by following the Designator production
    def _designator(self):
        self.observer.begin_designator()
        self.match("IDENTIFIER")
        self._selector()
        self.observer.end_designator()

    # set expectation of creating a Selector
    # by following the Selector production
    def _selector(self):
        self.observer.begin_selector()
        while (self.token_list[self.current].kind == self.kind_map["["]) \
                or (self.token_list[self.current].kind == self.kind_map["."]):
            if self.token_list[self.current].kind == self.kind_map["["]:
                self.match("[")
                self._expression_list()
                self.match("]")
            elif self.token_list[self.current].kind == self.kind_map["."]:
                self.match(".")
                self.match("IDENTIFIER")
            else:
                self.total_error_flag = 1
                sys.stderr.write("error: not a valid selector\n"
                             "@({0}, {1})".format(self.token_list[self.current].start_position,
                                                  self.token_list[self.current].end_position))
        self.observer.end_selector()

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
        self.observer.begin_expression_list()
        self._expression()
        while self.token_list[self.current].kind == self.kind_map[","]:
            self.match(",")
            self._expression()
        self.observer.end_expression_list()

'''
def main():
    f = open("test2.txt")
    input_string = ""
    for line in f:
        input_string += line
    # print input_string
    f.close()
    s = Scanner(input_string)
    token_list = s.all()
    p = Parser(token_list=token_list, print_symbol_table=1)
    p.parse()

main()
'''