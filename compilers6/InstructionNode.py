from Node import Node

class InstructionNode(Node):

    def __init__(self, _next):
        self._next = _next

    def to_string(self):
        pass

    #def int_visit(self, interpreter, environment):
    #    interpreter.interpret(self, environment)

    def int_visit(self, visitor):
        pass