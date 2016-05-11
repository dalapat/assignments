from Instruction import Instruction

class Read(Instruction):
    def __init__(self, location):
        super(Read, self).__init__()
        self.location = location

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_read(self)

    def __str__(self):
        return "Read"