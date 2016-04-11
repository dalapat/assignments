from Interpreter import Interpreter

class InterpreterVisitor:

    def __init__(self, environment):
        self.environment = environment
        self.interpreter = Interpreter()

    def visitNode(self, ast):
        self.interpreter.interpret(ast, self.environment)
        if ast._next is not None:
            ast._next.int_visit(self)

    #def visitNumberNode(self, ast):
    #    self.interpreter

