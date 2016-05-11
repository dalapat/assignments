# Eric Calder
# ecalder6@jhu.edu

# Visitor that creates the dot output for AST.
class ASTDotVisitor:
    def __init__(self):
        """Initializes the DOT visitor."""
        self.counter = 0

    def display(self):
        """Called by the Parser."""

        output = "digraph G {\n"
        output += self.visit_instructions(self.tree)
        output += "}"

        print(output)

    def visit_instructions(self, head):
        """Print every instruction."""
        output = ""

        prev = None
        instruction = head
        while instruction != None:
            output += instruction.accept(self)
            if prev != None:
                output += (
                    str(id(prev)) + "->" 
                    + str(id(instruction)) + "[label=\"next\"]\n"
                )
            prev = instruction
            instruction = instruction.next

        # Make sure all instruction nodes are horizontally aligned.
        instruction = head
        output += "{rank=same;"
        while instruction != None:
            output += str(id(instruction)) + ";"
            instruction = instruction.next
        output += "}\n"

        return output

    def visit_assign(self, assign):
        """Print everything in an assign tree."""
        output = str(id(assign)) + " [shape=box, label=\"=:\"]\n"

        output += assign.location.accept(self)
        output += assign.expression.accept(self)

        output += (
            str(id(assign)) + "->" 
            + str(id(assign.location)) + "[label=\"location\"]\n"
        )
        output += (
            str(id(assign)) + "->" 
            + str(id(assign.expression)) + "[label=\"expression\"]\n"
        )
        return output

    def visit_if(self, if_ins):
        """Print everything in an if tree."""
        output = str(id(if_ins)) + " [shape=box, label=\"If\"]\n"

        output += if_ins.condition.accept(self)
        output += self.visit_instructions(if_ins.instructions_true)
        if if_ins.instructions_false != None:
            output += self.visit_instructions(if_ins.instructions_false)

        output += (
            str(id(if_ins)) + "->" 
            + str(id(if_ins.condition)) + "[label=\"condition\"]\n"
        )
        output += (
            str(id(if_ins)) + "->" 
            + str(id(if_ins.instructions_true)) + "[label=\"true\"]\n"
        )
        if if_ins.instructions_false != None:
            output += (
                str(id(if_ins)) + "->" 
                + str(id(if_ins.instructions_false)) + "[label=\"false\"]\n"
            )

        return output

    def visit_repeat(self, repeat):
        """Print everything in a repeat tree."""
        output = str(id(repeat)) + " [shape=box, label=\"Repeat\"]\n"

        output += repeat.condition.accept(self)
        output += self.visit_instructions(repeat.instructions)

        output += (
            str(id(repeat)) + "->" 
            + str(id(repeat.condition)) + "[label=\"condition\"]\n"
        )
        output += (
            str(id(repeat)) + "->" 
            + str(id(repeat.instructions)) + "[label=\"instructions\"]\n"
        )

        return output

    def visit_read(self, read):
        """Print everything in a read tree."""
        output = str(id(read)) + " [shape=box, label=\"Read\"]\n"

        output += read.location.accept(self)

        output += (
            str(id(read)) + "->" 
            + str(id(read.location)) + "[label=\"location\"]\n"
        )

        return output

    def visit_write(self, write):
        """Print everything in a write tree."""
        output = str(id(write)) + " [shape=box, label=\"Write\"]\n"

        output += write.expression.accept(self)

        output += (
            str(id(write)) + "->" 
            + str(id(write.expression)) + "[label=\"expression\"]\n"
        )

        return output

    def visit_number(self, number):
        """Print everything in a write tree."""
        output = str(id(number)) + " [shape=box, label=\"Number\"]\n"

        # Ensure all number ST pointers point to unique diamonds.
        stid = "s" + str(self.counter) + str(id(number.entry))

        output += (
            stid + " [shape=diamond, label=\"" 
            + str(number.entry.value) +"\"]\n"
        )

        output += str(id(number)) + "->" + stid + "[label=\"ST\"]\n"

        self.counter += 1

        return output

    def visit_binary(self, binary):
        """Print everything in a binary tree."""
        output = (
            str(id(binary)) + " [shape=box, label=\"" 
            + str(binary.operator) + "\"]\n"
        )

        output += binary.left.accept(self)
        output += binary.right.accept(self)

        output += (
            str(id(binary)) + "->" 
            + str(id(binary.left)) + "[label=\"left\"]\n"
        )
        output += (
            str(id(binary)) + "->" 
            + str(id(binary.right)) + "[label=\"right\"]\n"
        )

        return output

    def visit_variableAST(self, variableAST):
        """Print everything in a variable tree."""
        output = str(id(variableAST)) + " [shape=box, label=\"Variable\"]\n"

        stid = "s" + str(self.counter) + str(id(variableAST.name))

        output += (
            stid + " [shape=circle, label=\"" + str(variableAST.name) +"\"]\n"
        )

        # Ensure all variable ST pointers point to unique circles.
        output += str(id(variableAST)) + "->" + stid + "[label=\"ST\"]\n"

        self.counter += 1

        return output

    def visit_index(self, index):
        """Print everything in an index tree."""
        output = str(id(index)) + " [shape=box, label=\"Index\"]\n"

        output += index.location.accept(self)
        output += index.expression.accept(self)

        output += (
            str(id(index)) + "->" 
            + str(id(index.location)) + "[label=\"location\"]\n"
        )
        output += (
            str(id(index)) + "->" 
            + str(id(index.expression)) + "[label=\"expression\"]\n"
        )

        return output

    def visit_fieldAST(self, fieldAST):
        """Print everything in a field tree."""
        output = str(id(fieldAST)) + " [shape=box, label=\"Field\"]\n"

        output += fieldAST.location.accept(self)
        output += fieldAST.variable.accept(self)

        output += (
            str(id(fieldAST)) + "->" 
            + str(id(fieldAST.location)) + "[label=\"location\"]\n"
        )
        output += (
            str(id(fieldAST)) + "->" 
            + str(id(fieldAST.variable)) + "[label=\"variable\"]\n"
        )

        return output

    def visit_condition(self, condition):
        """Print everything in a field tree."""
        output = (
            str(id(condition)) 
            + " [shape=box, label=\""+ str(condition.relation) +"\"]\n"
        )

        output += condition.left.accept(self)
        output += condition.right.accept(self)

        output += (
            str(id(condition)) + "->" 
            + str(id(condition.left)) + "[label=\"left\"]\n"
        )
        output += (
            str(id(condition)) + "->" 
            + str(id(condition.right)) + "[label=\"right\"]\n"
        )

        return output