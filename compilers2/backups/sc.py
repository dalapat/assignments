#!/usr/bin/python
from Scanner import Scanner
import sys

def main():
    num_args = len(sys.argv)-1
    try:
        if num_args == 0:
            sys.stderr.write("Error: not enough arguments\n")
        if num_args > 2:
            sys.stderr.write("Error: too many arguments\n")

        if sys.argv[1][1] == 's':
            if num_args == 1:
                # read from stdin
                print "hello"
            elif num_args == 2:
                # read from file
                f = open(sys.argv[2], 'r')
                input_line = ""
                for line in f:
                    input_line += line
                s = Scanner(input_line)
                s.all()
                f.close()
        elif sys.argv[1][1] == 'c':
            sys.stderr.write("Error: invalid option\n")
        elif sys.argv[1][1] == 't':
            sys.stderr.write("Error: invalid option\n")
        elif sys.argv[1][1] == 'a':
            sys.stderr.write("Error: invalid option\n")
        elif sys.argv[1][1] == 'i':
            sys.stderr.write("Error: invalid option\n")
        else:
            sys.stderr.write("Error: invalid option\n")

    except Exception as e:
        pass
main()