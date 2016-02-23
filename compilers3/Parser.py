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
        

    def _term(self):
        pass

    def _factor(self):
        pass

    def _instructions(self):
        pass

    def _instruction(self):
        pass

    def _assign(self):
        pass

    def _if(self):
        pass

    def _repeat(self):
        pass

    def _while(self):
        pass

    def _condition(self):
        pass

    def _write(self):
        pass

    def _read(self):
        pass

    def _designator(self):
        pass

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