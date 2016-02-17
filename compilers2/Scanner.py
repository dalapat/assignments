from Token import Token

class Scanner:

    def __init__(self, input_text):
        self.input_text = input_text
        self.tokenlist = self.form_tokens()

    def form_tokens(self):
        i = 0
        input_text_length = len(self.input_text)
        tokenlist = []
        while(i < input_text_length):
            if self.is_whitespace(self.input_text[i]):
                i += 1
            elif self.is_letter(self.input_text[i]):
                v = []
                start = i
                while(i < input_text_length and (self.is_letter(self.input_text[i])
                                                 or self.is_digit(self.input_text[i]))):
                    v.append(self.input_text[i])
                    i += 1
                end = i
                v_string = ''.join(v)
                try:
                    token_string = Token.keyword_map[v_string]
                    token = Token(kind=2, keyword_value=token_string,
                                  start_position=start, end_position=end)
                    tokenlist.append(token)
                except:
                    token = Token(kind=1, identifier_value=v_string,
                                  start_position=start, end_position=end)
                    tokenlist.append(token)
            elif self.is_digit(self.input_text[i]):
                v = 0
                start = i
                while(i < input_text_length and self.is_digit(self.input_text[i])):
                    v = (10*v) + int(self.input_text[i])
                    i += 1
                end = i
                token = Token(kind=0, int_value=v, start_position=start, end_position=end)
                tokenlist.append(token)
            elif self.is_symbol(self.input_text[i]):
                symbol = self.input_text[i]
                if(not i == input_text_length-1 and (self.input_text[i]+self.input_text[i+1]) in Token.symbol_map):
                    symbol = self.input_text[i] + self.input_text[i+1]
                    token = Token(kind=3, symbol_value=symbol, start_position=i, end_position=i+1)
                    tokenlist.append(token)
                    i+=2
                else:
                    token = Token(kind=3, symbol_value=symbol, start_position=i, end_position=i)
                    tokenlist.append(token)
                    i+=1
            else:
                print "error"
        tokenlist.append(Token(kind=4, eof_value="eof", start_position=i, end_position=i))
        return tokenlist

    def is_whitespace(self, c):
        return c == ' ' or c == '\t' or c == '\n' or c == '\r'

    def is_letter(self, c):
        # if scanner reads a letter, it could be a keyword or an identifier
        letter_alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if c in letter_alphabet:
            return True
        return False

    def is_symbol(self, c):
        single_char_symbol_alphabet = list("+-*:;=<>#:()[],.")
        if c in single_char_symbol_alphabet:
            return True
        return False

    def is_digit(self, c):
        number_alphabet = list("0123456789")
        if c in number_alphabet:
            return True
        return False

    def next(self):
        pass

    def all(self):
        pass

def main():
    s = Scanner("VAR ics142: ARRAY 5 OF INTEGER;")
    for elem in s.tokenlist:
        print elem

main()
