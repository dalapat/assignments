# Eric Calder
# ecalder6@jhu.edu

import sys
from Token import *
from Error import *

# The scanner receives input from the user and produces Tokens that represent
# the input.
class Scanner:

    def __init__(self, code):
        """Initializes the scanner with a initial position (0) and a set of
        keywords.
        """

        self.i = 0

        self.code = code

        self.keywords = {"PROGRAM", "BEGIN", "END", "CONST", "TYPE", "VAR",
        "ARRAY", "OF", "RECORD", "DIV", "MOD", "IF", "THEN", "ELSE", "REPEAT",
        "UNTIL", "WHILE", "DO", "WRITE", "READ", ";", ".", ",", ":", "=", "+",
        "-", "*", "#", "<", ">", "<=", ">=", ":=", "(", ")", "[", "]"}

        self.tokens = []


    def next(self):
        """Return the next token in the code. Returns an eof token if there are
        no more tokens left in code. Returns an invalid token if there is an
        invalid character in the code.
        """

        try:
            while (self.i <= len(self.code)):
                if (self.i == len(self.code)):
                    # return an eof token.
                    return Token("eof", None, self.i, self.i)

                c = self.code[self.i]
                if str.isspace(c):
                    # skip the spaces.
                    self.i += 1
                elif str.isdigit(c):
                    # Constrcut a number token, which contains digits.
                    # This code is inspired by Peter's example compiler
                    start_pos = self.i
                    integer = 0
                    while (
                        self.i < len(self.code)
                        and str.isdigit(self.code[self.i])
                    ):
                        integer = 10 * integer + int(self.code[self.i])
                        self.i += 1
                    return Token(
                        "integer", integer, start_pos, self.i - 1
                    )
                elif str.isalpha(c):
                    # Construct an identifier token, which contains digits and
                    # letters
                    start_pos = self.i
                    identifier = c
                    self.i += 1

                    while (
                        self.i < len(self.code) and
                        (
                            str.isalpha(self.code[self.i]) or
                            str.isdigit(self.code[self.i])
                        )
                    ):
                        identifier += self.code[self.i]
                        self.i += 1

                    if identifier in self.keywords:
                        # If the identifier is a keyword, create a token for
                        # the keyword
                        return Token(identifier, None, start_pos, self.i - 1)
                    else:
                        return(
                            Token("identifier", identifier, start_pos,
                                self.i - 1)
                        )
                elif (
                    self.i + 1 < len(self.code)
                    and (c + self.code[self.i + 1]) == "(*"
                ):
                    # Skip the comment block, including any nested comments
                    start_pos = self.i
                    comment = 1
                    self.i += 2

                    # loop until the comment is not closed i.e. there are more
                    # opening comment symbols than closing comment symbols
                    while comment != 0:
                        if (self.i > len(self.code) - 2):
                            # The scanner reached the end of input while the
                            # comment is not closed. Throw an exception.
                            raise (
                                ScannerInvalidCommentNestingError(
                                    start_pos, self.i
                                )
                            )

                        elif (self.i + 1 < len(self.code) and (self.code[self.i]
                        + self.code[self.i + 1]) == "*)"):
                            # Encountered an end comment symbol.
                            comment -= 1
                            self.i += 2

                        elif (self.i + 1 < len(self.code) and (self.code[self.i]
                        + self.code[self.i + 1]) == "(*"):
                            # Encountered a start comment symbol.
                            comment += 1
                            self.i += 2

                        else:
                            # Skip anything inside a comment.
                            self.i += 1

                else:
                    # Symbol keywords that do not contain letters.
                    if (
                        self.i + 1 < len(self.code) and (self.code[self.i]
                            + self.code[self.i + 1]) in self.keywords
                    ):
                        # Check for symbol keyword with length 2.
                        self.i += 2
                        return (Token(c + self.code[self.i - 1], None,
                            self.i - 2, self.i - 1))

                    elif c in self.keywords:
                        # Check for symbol keyword with length 1.
                        self.i += 1
                        return (Token(c, None, self.i - 1, self.i - 1))
                    else:
                        # The input character is not valid. Throw an exception.
                        raise ScannerInvalidInputError(c, self.i)

        except (
            ScannerInvalidInputError, ScannerInvalidCommentNestingError
        ) as e:
            # Catch invalid comment and invalid input exception
            sys.stderr.write(e.message + "\n")

            # Return an invalid token
            self.i += 1
            return Token("INVALID", None, self.i, self.i)



    def all(self):
        """Return a list containing all tokens in the input. Note that
        this cannot be called if next has already been called."""
        try:
            if self.i != 0:
                # Throw an exception if next has already been called.
                raise ScannerAllError()
            while True:
                # Keep getting the next token.
                token = self.next()
                self.tokens.append(token)
                if (token.kind == "eof" or token.kind == "INVALID"):
                    # End loop if there are no more input (encountered eof) or
                    # there is an invalid token.
                    break
            return self.tokens
        except ScannerAllError as e:
            # Catch an exception in which next is called before all.
            sys.stderr.write(e.message + "\n")
            return self.tokens

