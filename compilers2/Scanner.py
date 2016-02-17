from Token import Token

class Scanner:

    def __init__(self, input_text):
        self.input_text = input_text

    def form_tokens(self):
        tokenlist = []
        i = 0
        input_text_length = len(self.input_text)
        while(i < input_text_length):
            if self.is_whitespace(self.input_text[i]):
                i += 1
            elif self.is_letter(self.input_text[i]):
                pass
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
                pass
            else:
                print "error"

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

