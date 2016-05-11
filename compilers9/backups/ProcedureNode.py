from InstructionNode import InstructionNode

class ProcedureNode(InstructionNode):

    def __init__(self, _next, proc_obj):
        InstructionNode.__init__(self, _next)
        self.proc_obj = proc_obj