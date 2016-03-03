from Type import Type
from Scope import Scope
import sys

class Record(Type):

    def __init__(self, scope):
        self.scope = scope

    def visit(self, visitor):
        visitor.visitRecord(self)
