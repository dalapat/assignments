class Token():

    keyword_list = ["CONST", "PROGRAM", "BEGIN", "END", "TYPE", "VAR",
                    "ARRAY", "IF", "DIV", "ELSE", "REPEAT", "WHILE", "WRITE", "READ",
                    "THEN", "END", "MOD", "DO", "UNTIL"]
    symbol_list = ["+", "-", "*", ":", ";", "=", "<", ">", "<=",
                   ">=", "#", ":=", "(", ")", "[", "]", ",", "."]
    # peek symbols, : -> := | < -> <= | > -> >= | ( -> (*
    keyword_map = {i:i for i in keyword_list}
    symbol_list = {k:k for k in symbol_list}

    def __init__(self, kind=0, int_value=0, identifier_value="", keyword_value="",
                 symbol="", start_position=0, end_position=0):
        self.kind = kind #integer=0, identifier=1, keyword=2, symbol=3, eof=4
        self.int_value = int_value
        self.identifier_value = identifier_value
        self.keyword_value = keyword_value
        self.symbol = symbol
        self.start_position = start_position
        self.end_position = end_position

    def __str__(self):
        output_string = ""
        if self.kind == 0:
            # integer
            output_string = "integer<{0}>@({1}, {2})".format(self.int_value, self.start_position, self.end_position)
        elif self.kind == 1:
            # identifier
            output_string = "identifier<{0}>@({1}, {2})".format(self.identifier_value, self.start_position, self.end_position)
        elif self.kind == 2:
            # keyword
            output_string = "{0}@({1}, {2})".format(self.keyword_value, self.start_position, self.end_position)
        elif self.kind == 3:
            # symbol
            output_string = "{0}@({1}, {2})".format(self.symbol, self.start_position, self.end_position)
        elif self.kind == 4:
            # eof
            output_stirng = "eof@{0}, {1}".format(self.start_position, self.end_position)
        else:
            output_string = "error: not a valid token"
        print output_string