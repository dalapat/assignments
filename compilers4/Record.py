from Type import Type
from Scope import Scope

class Record(Type):

    def __init__(self, scope):
        self.scope = scope