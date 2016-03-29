from InstructionNode import InstructionNode
import sys

class ReadNode(InstructionNode):

    def __init__(self, next, location):
        InstructionNode.__init__(self, next)
        self.location = location

    def to_string(self):
        output = "location: {0}\n".format(self.location)
        sys.stdout.write(output+'\n')