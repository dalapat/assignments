from Node import Node

class Condition(Node):
    def __init__(self, left, right, relation):
        self.left = left
        self.right = right
        self.relation = relation

    def accept(self, visitor):
        """Use Visitor to produce output."""
        return visitor.visit_condition(self)

    def __str__(self):
        return "Condition"