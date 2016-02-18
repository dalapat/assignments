from Token import Token
import sys

class Scanner:
    """
    Reads an input string and creates tokens. Tokens can be generated one by one by
    calling next() or a
    """

    # initializes a Scanner with the text to parse for tokens
    # as well as a pointer to the current character being parsed
    def __init__(self, input_text):
        self.input_text = input_text # text to parse for Tokens
        self.curr_position = 0 # current character in input_text

    # return all tokens found in input_text
    def all(self):
        token_list = []
        try:
            token = self.next()
            while(not token.kind == 4):
                sys.stdout.write(str(token) + '\n')
                token_list.append(token)
                token = self.next()
            token = self.next()
            sys.stdout.write(str(token) + '\n')
            token_list.append(token)
        except Exception as e:
            sys.stdout.write(str(e))
        return token_list
    def next(self):
        input_text_length = len(self.input_text)
        token = Token()
        error_flag = 0
        while(self.curr_position < input_text_length):
            if self.is_whitespace(self.input_text[self.curr_position]):
                self.curr_position += 1
            elif not self.curr_position+1 >= input_text_length and \
                    self.is_open_comment(self.input_text[self.curr_position], self.curr_position):
                open_comment_count = 1
                closed_comment_count = 0
                comment_list = []
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
                        comment_list = comment_list[:-1]
                        self.curr_position += 2
                    else:
                        self.curr_position += 1
                if not open_comment_count == closed_comment_count:
                    start_position, end_position = comment_list[len(comment_list)-1]
                    sys.stderr.write("\nerror: unclosed comment at position ({0}, {1})\n".format(start_position, end_position))
                    error_flag = 1
                    break

            elif self.is_letter(self.input_text[self.curr_position]):
                v = []
                start = self.curr_position
                while(self.curr_position < input_text_length and (self.is_letter(self.input_text[self.curr_position])
                                                 or self.is_digit(self.input_text[self.curr_position]))):
                    v.append(self.input_text[self.curr_position])
                    self.curr_position += 1
                end = self.curr_position-1
                v_string = ''.join(v)
                try:
                    token_string = Token.keyword_map[v_string]
                    token = Token(kind=2, keyword_value=token_string,
                                  start_position=start, end_position=end)
                    return token
                except:
                    token = Token(kind=1, identifier_value=v_string,
                                  start_position=start, end_position=end)
                    return token
            elif self.is_digit(self.input_text[self.curr_position]):
                v = 0
                start = self.curr_position
                while(self.curr_position < input_text_length and self.is_digit(self.input_text[self.curr_position])):
                    v = (10*v) + int(self.input_text[self.curr_position])
                    self.curr_position += 1
                end = self.curr_position-1
                token = Token(kind=0, int_value=v, start_position=start, end_position=end)
                return token
            elif self.is_symbol(self.input_text[self.curr_position]):
                symbol = self.input_text[self.curr_position]
                if(not self.curr_position == input_text_length-1 and
                           (self.input_text[self.curr_position]+self.input_text[self.curr_position+1]) in Token.symbol_map):
                    symbol = self.input_text[self.curr_position] + self.input_text[self.curr_position+1]
                    token = Token(kind=3, symbol_value=symbol,
                                  start_position=self.curr_position, end_position=self.curr_position+1)
                    self.curr_position+=2
                    return token
                else:
                    token = Token(kind=3, symbol_value=symbol,
                                  start_position=self.curr_position, end_position=self.curr_position)
                    self.curr_position+=1
                    return token
            else:
                sys.stderr.write("\nerror: illegal character \'{0}\' found " \
                      "at position @({1}, {2})\n".format(self.input_text[self.curr_position],
                                                       self.curr_position, self.curr_position))
                error_flag = 1
                break
        if error_flag == 0:
            token = Token(kind=4, eof_value="eof", start_position=self.curr_position, end_position=self.curr_position)
            return token
        else:
            exit()

    # check if a character is a whitespace or string formatting character
    def is_whitespace(self, c):
        return c == ' ' or c == '\t' or c == '\n' or c == '\r'

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

'''
def main():
    # s = Scanner("VAR ics142: ARRAY 5 OF INTEGER;")
    # s = Scanner("asdf 8_9 * ()^D")
    # s = Scanner("")
    # s = Scanner("VAR (*(*hello*)*) ics142: ARRAY 5 OF INTEGER; (*final*)")
    s = Scanner("PROGRAM As3;\nCONST x = -47;TYPE T = RECO$RD f: INTEGER; END; VAR a: 123ARRAY123 12 OF T; BEGINa[7].f := -x/END As3.")
    while True:
        try:
            x = raw_input()
            print s.next()
        except Exception as e:
            pass

main()
'''


