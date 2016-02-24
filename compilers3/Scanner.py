from Token import Token
import sys

class Scanner:
    """
    Reads an input string and creates tokens. Tokens can be generated one by one by
    calling next() or all()
    """

    # initializes a Scanner with the text to parse for tokens
    # as well as a pointer to the current character being parsed
    def __init__(self, input_text):
        self.input_text = input_text # text to parse for Tokens
        self.curr_position = 0 # current character in input_text

    # return all tokens found in input_text
    def all(self):
        token_list = [] # list of found tokens
        try:
            token = self.next() # first token
            while(not token.kind == Token.kind_map["EOF"]): # while we haven't reached the end of file
                token_list.append(token) # add it to found tokens
                token = self.next() # iterate
            token = self.next() # include eof token
            token_list.append(token)
        except Exception as e:
            sys.stderr.write(str(e))
        finally:
            return token_list

    # get the next token from the current position in the line
    def next(self):
        input_text_length = len(self.input_text)
        token = Token()
        error_flag = 0 # alert if error occurred
        while(self.curr_position < input_text_length):
            # check if the current character whitespace or string formatting
            if self.is_whitespace(self.input_text[self.curr_position]):
                self.curr_position += 1

            # check if the current character the beginning to a comment
            elif not self.curr_position+1 >= input_text_length and \
                    self.is_open_comment(self.input_text[self.curr_position], self.curr_position):
                open_comment_count = 1 # keeps track of currently unclosed comments
                closed_comment_count = 0 # keeps track of closed comments
                comment_list = [] # keeps track of currently unclosed comment position
                comment_list.append((self.curr_position, self.curr_position+1))
                self.curr_position += 2
                while(self.curr_position < input_text_length and not open_comment_count == closed_comment_count
                      and not self.curr_position+1 >= input_text_length):
                    if self.is_open_comment(self.input_text[self.curr_position], self.curr_position):
                        open_comment_count += 1
                        comment_list.append((self.curr_position, self.curr_position+1))
                        self.curr_position += 2
                    elif self.is_closed_comment(self.input_text[self.curr_position], self.curr_position):
                        closed_comment_count += 1
                        # inner most comment has been closed
                        comment_list = comment_list[:-1]
                        self.curr_position += 2
                    else:
                        self.curr_position += 1
                if not open_comment_count == closed_comment_count:
                    # check if there is an unclosed comment
                    start_position, end_position = comment_list[len(comment_list)-1]
                    sys.stderr.write("\nerror: unclosed comment at position ({0}, {1})\n".format(start_position, end_position))
                    error_flag = 1
                    break

            # check if the current character is a letter
            elif self.is_letter(self.input_text[self.curr_position]):
                v = []
                # if its a letter, it could be a identifier or a keyword
                start = self.curr_position # start position of token
                while(self.curr_position < input_text_length and (self.is_letter(self.input_text[self.curr_position])
                                                 or self.is_digit(self.input_text[self.curr_position]))):
                    v.append(self.input_text[self.curr_position])
                    self.curr_position += 1
                end = self.curr_position-1 # end position of token
                v_string = ''.join(v)
                try:
                    token_string = Token.keyword_map[v_string] # check if the token is a keyword
                    token = Token(kind=Token.kind_map[token_string], keyword_value=token_string,
                                  start_position=start, end_position=end)
                    return token
                except:
                    token = Token(kind=Token.kind_map["IDENTIFIER"], identifier_value=v_string, # KeyError caught so it must be an identifier
                                  start_position=start, end_position=end)
                    return token

            # check if current character is a digit
            elif self.is_digit(self.input_text[self.curr_position]):
                v = 0
                start = self.curr_position
                while(self.curr_position < input_text_length and self.is_digit(self.input_text[self.curr_position])):
                    # find an integer token
                    v = (10*v) + int(self.input_text[self.curr_position])
                    self.curr_position += 1
                end = self.curr_position-1
                token = Token(kind=Token.kind_map["INTEGER"], int_value=v, start_position=start, end_position=end)
                return token

            # check if current character is a symbol
            elif self.is_symbol(self.input_text[self.curr_position]):
                symbol = self.input_text[self.curr_position]
                if(not self.curr_position == input_text_length-1 and
                           (self.input_text[self.curr_position]+self.input_text[self.curr_position+1]) in Token.symbol_map):
                    # symbol is a multi-character token (i.e "<=", ">=", ":=")
                    symbol = self.input_text[self.curr_position] + self.input_text[self.curr_position+1]
                    token = Token(kind=Token.kind_map[symbol], symbol_value=symbol,
                                  start_position=self.curr_position, end_position=self.curr_position+1)
                    self.curr_position+=2
                    return token
                else:
                    # symbol is a single-character token
                    token = Token(kind=Token.kind_map[symbol], symbol_value=symbol,
                                  start_position=self.curr_position, end_position=self.curr_position)
                    self.curr_position+=1
                    return token

            # illegal character
            else:
                sys.stderr.write("\nerror: illegal character \'{0}\' found " \
                      "at position @({1}, {2})\n".format(self.input_text[self.curr_position],
                                                       self.curr_position, self.curr_position))
                error_flag = 1
                break
        # if no errors were found, return eof token
        if error_flag == 0:
            token = Token(kind=Token.kind_map["EOF"], eof_value="eof", start_position=self.curr_position, end_position=self.curr_position)
            return token
        else:
            # error, exit the program
            exit()

    # check if a character is a whitespace or string formatting character
    def is_whitespace(self, c):
        return c == ' ' or c == '\t' or c == '\n' or c == '\r' or c == '\f'

    # check if a character is a beginning to a comment
    def is_open_comment(self, c, i):
        return (c+self.input_text[i+1]) == "(*"

    # check if a character is a closing comment
    def is_closed_comment(self, c, i):
        return (c+self.input_text[i+1]) == "*)"

    # check if a character is a letter
    def is_letter(self, c):
        # if scanner reads a letter, it could be a keyword or an identifier
        letter_alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if c in letter_alphabet:
            return True
        return False

    # check if a character is in the symbol map defined in Token
    def is_symbol(self, c):
        single_char_symbol_alphabet = list("+-*:;=<>#:()[],.")
        if c in single_char_symbol_alphabet:
            return True
        return False

    # check if a character is a digit
    def is_digit(self, c):
        number_alphabet = list("0123456789")
        if c in number_alphabet:
            return True
        return False