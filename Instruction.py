from Node import Node

class Instruction(Node):
    def __init__(self):
        super(Instruction, self).__init__()
        self.next = None

    def __str__(self):
        return "Instruction"