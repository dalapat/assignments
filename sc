#!/usr/bin/env python3

# Eric Calder
# ecalder6@jhu.edu

import sys
from Error import *
from Scanner import *
from Parser import Parser
from ParserObserver import *
from TextVisitor import TextVisitor
from DotVisitor import DotVisitor
from ASTTextVisitor import ASTTextVisitor
from ASTDotVisitor import ASTDotVisitor
from ASTInterpreterVisitor import ASTInterpreterVisitor

# This is the driver class of the compiler. It recieves input from the user and
# passes it to the scanner, which returns a set of tokens. It then print all
# of these tokens, one on each line. More functionalities will be added in the
# future.
def read_standard_input():
    """Read SIMPLE code from Standard Input."""

    # Read user input from standard input.
    code = sys.stdin.read()

    return code

def read_input_file(file):
    """Read SIMPLE code from a input file."""

    code = ""
    try:
        f = open(file, 'r')

        # Read user input from file
        code = f.read()

        f.close()
        return code

    except IOError:
        # Catch an exeption for invalid file.
        sys.stderr.write("error: file " + str(file) + " cannot be opened.\n")
        sys.exit(1)

def scan(code):
    """Get all tokens from scanner and print them out"""

    # Create a scanner.
    scanner = Scanner(code)

    # Get the tokens from scanner.
    tokens = scanner.all()

    # Print all tokens scanned.
    for token in tokens:
        # Do not print invalid token
        if (str(token) != ''):
            print(token)

def call_parser(code, parser_type, style):
    """Call parse in Parser with an initialized Scanner"""

    scanner = Scanner(code)
    if parser_type == "-c":
        # Print out the parse tree.
        output_object = ParserObserver(style, True)
    elif parser_type == "-t":
        # Print out the symbol table.

        # Do not display the observer output for parse tree.
        ParserObserver(style, False)
        if style == "text":
            output_object = TextVisitor()
        elif style == "graph":
            output_object = DotVisitor()
    elif parser_type == "-a":
        # Print out the AST.

        # Do not display the observer output for parse tree.
        ParserObserver(style, False)
        if style == "text":
            output_object = ASTTextVisitor()
        elif style == "graph":
            output_object = ASTDotVisitor()

    elif parser_type == "-i":
        # Interpret the program

        ParserObserver(style, False)
        output_object = ASTInterpreterVisitor()

    parser = Parser(scanner, output_object, parser_type, style)
    parser.parse()


# "Main Method"
arg_len = len(sys.argv)

try:
    # Get input from standard input for scanner.
    if arg_len == 2 and sys.argv[1] == "-s":

        # Create scanner and print tokens produced by scanner.
        scan(read_standard_input())

    # Get input from file for scanner.
    elif arg_len == 3 and sys.argv[1] == "-s":

        # Create scanner and print tokens produced by scanner.
        scan(read_input_file(sys.argv[2]))

    # Get input from standard input for parser.
    elif arg_len == 2 and sys.argv[1] == "-c":

        # Create parser and call parse with textual form tree.
        call_parser(read_standard_input(), sys.argv[1], "text")

    # Get input from standard input for parser.
    elif arg_len == 2 and sys.argv[1] == "-t":

        # Create parser and create symbol table with textual form tree.
        call_parser(read_standard_input(), sys.argv[1], "text")

    # Get input from standard input for parser.
    elif arg_len == 2 and sys.argv[1] == "-a":

        # Create parser and create AST in text.
        call_parser(read_standard_input(), sys.argv[1], "text")

        # Get input from standard input for parser.
    elif arg_len == 2 and sys.argv[1] == "-i":

        # Create parser and create AST in text.
        call_parser(read_standard_input(), sys.argv[1], "text")

    # Get input from standard input for parser.
    elif arg_len == 3 and sys.argv[1] == "-a" and sys.argv[2] == "-g":

        # Create parser and create AST in text.
        call_parser(read_standard_input(), sys.argv[1], "graph")

    # Get input from standard input for parser.
    elif arg_len == 4 and sys.argv[1] == "-a" and sys.argv[2] == "-g":

        # Create parser and create AST in graph.
        call_parser(read_input_file(sys.argv[3]), sys.argv[1], "graph")

    # Get input from standard input for parser.
    elif arg_len == 3 and sys.argv[1] == "-t" and sys.argv[2] == "-g":

        # Create parser and create symbol table with graphical form tree.
        call_parser(read_standard_input(), sys.argv[1], "graph")

    # Get input from standard input for parser.
    elif arg_len == 4 and sys.argv[1] == "-t" and sys.argv[2] == "-g":

        # Create parser and create symbol table with graphical form tree.
        call_parser(read_input_file(sys.argv[3]), sys.argv[1], "graph")

    # Get input from standard input for parser.
    elif arg_len == 3 and sys.argv[1] == "-c" and sys.argv[2] == "-g":

        # Create parser and call parse with graphical form tree.
        call_parser(read_standard_input(), sys.argv[1], "graph")

    # Get input from file for parser with graphical form tree.
    elif arg_len == 4 and sys.argv[1] == "-c" and sys.argv[2] == "-g":

        # Create parser and call parse
        call_parser(read_input_file(sys.argv[3]), sys.argv[1], "graph")

    # Get input from file for parser with textual form tree.
    elif arg_len == 3 and sys.argv[1] == "-c":

        # Create parser and call parse
        call_parser(read_input_file(sys.argv[2]), sys.argv[1], "text")

    # Get input from standard input for parser.
    elif arg_len == 3 and sys.argv[1] == "-t":

        # Create parser and create symbol table with textual form tree.
        call_parser(read_input_file(sys.argv[2]), sys.argv[1], "text")

    # Get input from standard input for parser.
    elif arg_len == 3 and sys.argv[1] == "-a":

        # Create parser and create AST in text.
        call_parser(read_input_file(sys.argv[2]), sys.argv[1], "text")

    # Get input from standard input for parser.
    elif arg_len == 3 and sys.argv[1] == "-i":

        # Create parser and create AST in text.
        call_parser(read_input_file(sys.argv[2]), sys.argv[1], "text")

    # Invalid arguments.
    else:
        raise ArgvError()

except ArgvError as e:
    # Catch an exception for invalid argument.
    sys.stderr.write(e.message + "\n")
    sys.exit(1)