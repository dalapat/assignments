from UnexpectedTokenException import UnexpectedTokenException
from Scanner import Scanner
from Token import Token
from Observer import Observer
import sys


class Parser:

    """Takes a list of tokens and performs semantic analysis
       to check if input adheres to grammar. Outputs to stdout
       a textual representation of the CST via the call stack.
       Parser is also capable of outputting graphical output
    """

    # initializes Parser instance and parses a list of tokens
    # cmd line arguments determine output type
    def __init__(self, observer = Observer(), token_list=[]):
        self.current = 0 # current position in token list
        self.token_list = token_list # token list received from scanner
        self.kind_map = Token.kind_map # dictionary of token kinds
        self.observer = observer # output class determined by cmd line arguments
        self.total_error_flag = 0 # detects if an error occurs anywhere in the program

    # parse the token list
    def parse(self):
        self._program()
        # do not print any output if error occurs
        if self.total_error_flag == 0:
            self.observer.print_output()

    # check if the currently parsed token is a token we are
    # expecting to find
    # kind = expected kind of token
    def match(self, kind):
        if self.token_list[self.current].kind == self.kind_map[kind]:
            # sys.stdout.write(str(self.token_list[self.current]) + "\n")
            self.observer.print_token(self.token_list[self.current])
            self.current += 1
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
        self.match("IDENTIFIER")
        self.match(";")
        self._declarations()
        if self.token_list[self.current].kind == self.kind_map["BEGIN"]:
            self.match("BEGIN")
            self._instructions()
        self.match("END")
        self.match("IDENTIFIER")
        self.match(".")
        self.observer.end_program()
        # should an error go here to detect trash?
        if not self.token_list[self.current].kind == self.kind_map["EOF"]:
            self.total_error_flag = 1
            sys.stderr.write("error: trash detected after program end: "
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
            self.match("IDENTIFIER")
            self.match("=")
            self._expression()
            self.match(";")
        self.observer.end_constdecl()

    # set expectation of creating a TypeDecl
    # by following the TypeDecl production
    def _typedecl(self):
        # print "TypeDecl"
        self.observer.begin_typedecl()
        self.match("TYPE")
        while self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            self.match("IDENTIFIER")
            self.match("=")
            self._type()
            self.match(";")
        self.observer.end_typedecl()

    # set expectation of creating a VarDecl
    # by following the VarDecl production
    def _vardecl(self):
        # print "VarDecl"
        self.observer.begin_vardecl()
        self.match("VAR")
        while self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            self._identifier_list()
            self.match(":")
            self._type()
            self.match(";")
        self.observer.end_vardecl()

    # set expectation of creating a Type
    # by following the Type production
    def _type(self):
        # print "Type"
        self.observer.begin_type()
        if self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            self.match("IDENTIFIER")
        elif self.token_list[self.current].kind == self.kind_map["ARRAY"]:
            self.match("ARRAY")
            self._expression()
            self.match("OF")
            self._type()
        elif self.token_list[self.current].kind == self.kind_map["RECORD"]:
            self.match("RECORD")
            while self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
                self._identifier_list()
                self.match(":")
                self._type()
                self.match(";")
            self.match("END")
        else:
            self.total_error_flag = 1
            sys.stderr.out("error: expecting Identifier, ARRAY, or RECORD")
        self.observer.end_type()

    # set expectation of creating a Expression
    # by following the Expression production
    def _expression(self):
        # print "Expression"
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
                sys.stderr.write("error: expecting \'+\' or \'-\'")
            self._term()
        self.observer.end_expression()

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
                sys.stderr.out("error: expecting \'*\', \'DIV\', or \'MOD\'")
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
            sys.stdout.error("error: expecting integer, identifier or \'(\'")
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
        # is this bad that i check directly for identifier?
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
            sys.stderr.write("error: not a valid instruction "
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
            sys.stderr.write("error: not a valid condition "
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
                sys.stderr.write("error: not a valid selector "
                             "@({0}, {1})".format(self.token_list[self.current].start_position,
                                                  self.token_list[self.current].end_position))
        self.observer.end_selector()

    # set expectation of creating a IdentifierList
    # by following the IdentifierList production
    def _identifier_list(self):
        self.observer.begin_identifier_list()
        self.match("IDENTIFIER")
        while self.token_list[self.current].kind == self.kind_map[","]:
            self.match(",")
            self.match("IDENTIFIER")
        self.observer.end_identifier_list()

    # set expectation of creating a ExpressionList
    # by following the ExpressionList production
    def _expression_list(self):
        self.observer.begin_expression_list()
        self._expression()
        while self.token_list[self.current].kind == self.kind_map[","]:
            self.match(",")
            self._expression()
        self.observer.end_expression_list()