from UnexpectedTokenException import UnexpectedTokenException
from Scanner import Scanner
from Token import Token

import sys

class Parser:

    def __init__(self, token_list):
        self.current = 0
        self.token_list = token_list
        # fix this
        t = Token()
        self.kind_map = t.kind_map

    def parse(self):
        self._program()

    def match(self, kind):
        if self.token_list[self.current].kind == self.kind_map[kind]:
            sys.stdout.write(self.token_list[self.current])
            self.current += 1
        else:
            sys.stderr.write("error: expected token kind {0}, "
                             "received unexpected token {1}".format(kind, self.token_list[self.current]))

    def _program(self):
        print "Program"
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

    def _declarations(self):
        print "Declarations"
        while (self.token_list[self.current].kind == self.kind_map["CONST"] or
            self.token_list[self.current].kind == self.kind_map["TYPE"] or
            self.token_list[self.current].kind == self.kind_map["VAR"]):
            if self.token_list[self.current].kind == self.kind_map["CONST"]:
                self._constdecl()
            elif self.token_list[self.current].kind == self.kind_map["TYPE"]:
                self._typedecl()
            elif self.token_list[self.current].kind == self.kind_map["VAR"]:
                self._vardecl()
            else:
                pass

    def _constdecl(self):
        print "ConstDecl"
        self.match("CONST")
        while self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            self.match("IDENTIFIER")
            self.match("=")
            self._expression()
            self.match(";")

    def _typedecl(self):
        print "TypeDecl"
        self.match("TYPE")
        while self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            self.match("IDENTIFIER")
            self.match("=")
            self._expression()
            self.match(";")

    def _vardecl(self):
        print "VarDecl"
        self.match("VAR")
        while self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            self._identifier_list()
            self.match(":")
            self._type()
            self.match(";")

    def _type(self):
        print "Type"
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
            pass

    def _expression(self):
        print "Expression"
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
                sys.stderr.write("error: expected {0}, received unexpected "
                                 "token {1}".format("+ or -", self.token_list[self.current]))
            self._term()

    def _term(self):
        print "Term"
        self._factor()
        while (self.token_list[self.current].kind == self.kind_map["*"])or \
            (self.token_list[self.current].kind == self.kind_map["DIV"]) or \
            (self.token_list[self.current].kind == self.kind_map["MOD"]):
            self._factor()

    def _factor(self):
        print "Factor"
        if self.token_list[self.current].kind == self.kind_map["INTEGER"]:
            self.match("INTEGER")
        elif self.token_list[self.current].kind == self.kind_map["IDENTIFIER"]:
            self._designator()
        elif self.token_list[self.current].kind == self.kind_map["("]:
            self.match("(")
            self._expression()
            self.match(")")
        else:
            sys.stdout.error("error: idk man something's wrong in factor")

    def _instructions(self):
        print "Instructions"
        self._instruction()
        while self.token_list[self.current].kind == self.kind_map[";"]:
            self.match(";")
            self._instruction()

    def _instruction(self):
        print "Instruction"
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
            sys.stderr.write("error: instruction method")

    def _assign(self):
        print "Assign"
        self._designator()
        self.match(":=")
        self._expression()

    def _if(self):
        print "If"
        self.match("IF")
        self._condition()
        self.match("THEN")
        self._instructions()
        if self.token_list[self.current].kind == self.kind_map["ELSE"]:
            self.match("ELSE")
            self._instructions()
        self.match("END")

    def _repeat(self):
        print "Repeat"
        self.match("REPEAT")
        self._instructions()
        self.match("UNTIL")
        self._condition()
        self.match("END")

    def _while(self):
        print "While"
        self.match("WHILE")
        self._condition()
        self.match("DO")
        self._instructions()
        self.match("END")

    def _condition(self):
        print "Condition"
        self._expression()
        ("="|"#"|"<"|">"|"<="|">=")
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
            sys.stderr.write("error: condition method")

    def _write(self):
        print "Write"
        self.match("WRITE")
        self._expression()

    def _read(self):
        print "Read"
        self.match("READ")
        self._designator()

    def _designator(self):
        

    def _selector(self):
        pass

    def _identifier_list(self):
        pass

    def _expression_list(self):
        pass

    def _identifier(self):
        pass

    def _integer(self):
        pass


def main():
    s = Scanner("")

    token_list = s.all()
    p = Parser(token_list)

main()