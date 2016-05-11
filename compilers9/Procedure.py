from Entry import Entry

class Procedure(Entry):

    def __init__(self, formal_parameters, local_variables, instructions, return_exp):
        self.formal_parameters = formal_parameters
        self.formal_parameter_order_list = []
        self.local_variables = local_variables
        self.body = instructions
        self.return_exp = return_exp

