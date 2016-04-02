from Interpreter import Interpreter
class InterpeterVisitor:

    def __init__(self, environment):
        self.environment = environment
        self.interpreter = Interpreter()

    def visitNumberNode(self, num_node):
        pass