from Type import Type

class Array(Type):

    def __init__(self, length, type):
        self.length = length
        self.type = type