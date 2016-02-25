from UnexpectedTokenException import UnexpectedTokenException
from Scanner import Scanner
from Token import Token
from Observer import Observer
from DotObserver import DotObserver
import sys


class Parser:

    # how to suppress output if error occurs
    # switching output on and off?
    # graph
    # when errors occur, should we break or continue parsing?

    def __init__(self, observer = Observer(), token_list=[]):
        self.current = 0
        self.token_list = token_list
        self.kind_map = Token.kind_map
        # self.observer = observer
        self.observer = observer
        self.total_error_flag = 0

    def parse(self):
        self._program()
        if self.total_error_flag == 0:
            self.observer.print_output()

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
            # raise UnexpectedTokenException

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

    def _declarations(self):
        # print "Declarations"
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
                # what should happen here?
                # self.total_error_flag = 1
                # sys.stderr.write("error: expecting \'CONST\', \'TYPE\', or \'VAR\'" + '\n')
                # should I break here?
        # else:
        #    self.total_error_flag = 1
        #    sys.stderr.write("error: expecting \'CONST\', \'TYPE\', or \'VAR\'" + '\n')
        # what should happen here? it says 0 or more
        self.observer.end_declarations()

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

    def _term(self):
        # print "Term"
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

    def _factor(self):
        # print "Factor"
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

    def _instructions(self):
        # print "Instructions"
        self.observer.begin_instructions()
        self._instruction()
        while self.token_list[self.current].kind == self.kind_map[";"]:
            self.match(";")
            self._instruction()
        self.observer.end_instructions()

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

    def _assign(self):
        # print "Assign"
        self.observer.begin_assign()
        self._designator()
        self.match(":=")
        self._expression()
        self.observer.end_assign()

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

    def _repeat(self):
        # print "Repeat"
        self.observer.begin_repeat()
        self.match("REPEAT")
        self._instructions()
        self.match("UNTIL")
        self._condition()
        self.match("END")
        self.observer.end_repeat()

    def _while(self):
        # print "While"
        self.observer.begin_while()
        self.match("WHILE")
        self._condition()
        self.match("DO")
        self._instructions()
        self.match("END")
        self.observer.end_while()

    def _condition(self):
        # print "Condition"
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

    def _write(self):
        # print "Write"
        self.observer.begin_write()
        self.match("WRITE")
        self._expression()
        self.observer.end_write()

    def _read(self):
        # print "Read"
        self.observer.begin_read()
        self.match("READ")
        self._designator()
        self.observer.end_read()

    def _designator(self):
        # print "Designator"
        self.observer.begin_designator()
        self.match("IDENTIFIER")
        self._selector()
        self.observer.end_designator()


    def _selector(self):
        # print "Selector"
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


    def _identifier_list(self):
        # print "IdentifierList"
        self.observer.begin_identifier_list()
        self.match("IDENTIFIER")
        while self.token_list[self.current].kind == self.kind_map[","]:
            self.match(",")
            self.match("IDENTIFIER")
        self.observer.end_identifier_list()

    def _expression_list(self):
        # print "ExpressionList"
        self.observer.begin_expression_list()
        self._expression()
        while self.token_list[self.current].kind == self.kind_map[","]:
            self.match(",")
            self._expression()
        self.observer.end_expression_list()

'''
def main():
    # if there is an error in scanner, how do i stop the program?
    # how many errors should show up?
    # strong and weak?
    try:

        f = open("test.txt", 'r')
        input_line = ""
        for line in f:
            input_line += line
        s = Scanner(input_line)
        token_list = s.all()
        #for token in token_list:
        #    sys.stdout.write(str(token) + '\n')
        f.close()
        # token_list = s.all()
        p = Parser(token_list)
        p.parse()
    except:
        pass
main()
'''