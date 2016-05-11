class Token():

    """
    This class represents a single token. A token contains a "kind" field to represent
    whether its an integer, an identifier, a keyword, a symbol, or an EOF.
    This class also contains a list of all valid keywords and symbols, though
    the actual error checking is done in Scanner.
    """
    # list of all valid keywords
    keyword_list = ["CONST", "PROGRAM", "BEGIN", "END", "TYPE", "VAR",
                    "ARRAY", "IF", "OF", "DIV", "ELSE", "REPEAT", "WHILE", "WRITE", "READ",
                    "THEN", "END", "MOD", "DO", "RECORD", "UNTIL"] #21

    # list of all valid symbols
    symbol_list = ["+", "-", "*", ":", ";", "=", "<", ">", "<=",
                   ">=", "#", ":=", "(", ")", "[", "]", ",", "."]

    # maps are formed from the above lists for constant time access
    # to check if a token is a keyword or symbol.
    keyword_map = {i:i for i in keyword_list}
    symbol_map = {k:k for k in symbol_list}

    kind_map = {"INTEGER":0, "IDENTIFIER":1}
    map_count = 2
    for keyword in keyword_list:
        kind_map[keyword] = map_count
        map_count += 1

    for operator in symbol_list:
        kind_map[operator] = map_count
        map_count += 1

    kind_map["EOF"] = map_count

    # initialize a generic token
    def __init__(self, kind=0, int_value=0, identifier_value="", keyword_value="",
                 symbol_value="", eof_value = "eof", start_position=0, end_position=0):
        self.kind = kind # INTEGER, IDENTIFIER, <keyword>, <symbol>, EOF
        self.int_value = int_value # actual integer value if integer
        self.identifier_value = identifier_value # actual identifier value if identifier
        self.keyword_value = keyword_value # actual keyword value if keyword
        self.symbol_value = symbol_value # actual symbol value if symbol
        self.eof_value = eof_value # token returned to represent eof
        self.start_position = start_position # position where current token was found
        self.end_position = end_position # position where current token ends

    # print custom attributes of token
    def __str__(self):
        output_string = ""
        if self.kind == 0:
            # integer
            output_string = "integer<{0}>@({1}, {2})".format(self.int_value, self.start_position, self.end_position)
        elif self.kind == 1:
            # identifier
            output_string = "identifier<{0}>@({1}, {2})".format(self.identifier_value, self.start_position, self.end_position)
        # elif self.kind == 2:
        elif 2 <= self.kind <= len(self.keyword_list) + 1:
            # keyword
            output_string = "{0}@({1}, {2})".format(self.keyword_value, self.start_position, self.end_position)
        # elif self.kind == 3:
        elif len(self.keyword_list) + 2 <= self.kind <= len(self.symbol_list) + len(self.keyword_list) + 1:
            # symbol
            output_string = "{0}@({1}, {2})".format(self.symbol_value, self.start_position, self.end_position)
        elif self.kind == 41:
            # eof
            output_string = "{0}@({1}, {1})".format(self.eof_value, self.start_position, self.end_position)
        else:
            output_string = "error: not a valid token"
        return output_string

    # parse the value stored in the token
    def get_token_name(self):
        output_string = ""
        if self.kind == 0:
            # integer
            output_string = str(self.int_value)
        elif self.kind == 1:
            # identifier
            output_string = self.identifier_value
        # elif self.kind == 2:
        elif 2 <= self.kind <= len(self.keyword_list) + 1:
            # keyword
            output_string = self.keyword_value
        # elif self.kind == 3:
        elif len(self.keyword_list) + 2 <= self.kind <= len(self.symbol_list) + len(self.keyword_list) + 1:
            # symbol
            output_string = self.symbol_value
        elif self.kind == 41:
            # eof
            output_string = self.eof_value
        else:
            output_string = "error: not a valid token"
        return output_string
