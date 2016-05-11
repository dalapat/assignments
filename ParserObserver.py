# Eric Calder
# ecalder6@jhu.edu

# The decorator observer than does the output depending on the style passed into
# the parser.

class ParserObserver():

    def __init__(self, style, observe):
        """Initializes the observer."""

        # The global "static" variables are used by the "static methods"
        global output
        global display
        display = observe

        self.style = style
        if self.style == "graph":
            output = "digraph G {\n"
        else:
            output = ""

    def display(self):
        """Print the output. Called by Parser."""
        global output
        if self.style == "graph":
            output += "}"
        print(output)

    def non_terminal_text(parser):
        """For textual output."""
        global output

        # Calculate the amount of indentation needed by counting the
        # numberof non-terminals in the stack, as each non-terminal
        # introduces 2 spaces to the identation.
        indent = ""
        for i in range(len(parser.stack) - 1):
            indent += "  "

        output += indent + parser.stack[len(parser.stack) - 1] + "\n"

    def non_terminal_graph(parser):
        """For graph output."""
        global output

        # Get the current non-terminal from top of the stack.
        cur = parser.stack[len(parser.stack) - 1]

        # Assign each non-terminal with an ID and push the list
        #containing both back into the stack.
        comb = [cur, parser.graph_index]
        parser.stack.pop()
        parser.stack.append(comb)

        # Set the shape and label of the node.
        output += (
            "    \"" + str(comb[1]) +
            "\" [label=" + cur + ", shape=box];\n"
        )

        # If this node has a parent, create an edge from the parent to
        # the this node. Note that the parent will always be the
        # non-terminal that is second from the top on the stack.
        if (len(parser.stack) > 1):
            prev = parser.stack[len(parser.stack) - 2]
            output += (
                "    \"" + str(prev[1]) + "\" -> " + str(comb[1])
                + ";\n"
            )

        # Increment the ID.
        parser.graph_index += 1

    def non_terminal(function):
        """Produces output for non-terminals."""
        def print_non_terminal(parser):
            # Simply run the method if we do not print parse tree.
            if display == False:
                return function(parser)

            if parser.style == "text":
                ParserObserver.non_terminal_text(parser)

            elif parser.style == "graph":
                ParserObserver.non_terminal_graph(parser)

            # Call the actual function that is being decorated.
            return_value = function(parser)

            # Pop the current non-terminal.
            parser.stack.pop()

            return return_value

        return print_non_terminal

    def selector(function):
        """Produces output for selectors."""
        def print_selector(parser, prev):
            # Simply run the method if we do not print parse tree.
            if display == False:
                return function(parser, prev)

            if parser.style == "text":
                ParserObserver.non_terminal_text(parser)

            elif parser.style == "graph":
                ParserObserver.non_terminal_graph(parser)

            # Call the actual function that is being decorated.
            return_value = function(parser, prev)

            # Pop the current non-terminal.
            parser.stack.pop()

            return return_value

        return print_selector

    def terminal(match):
        """Produces output for terminals."""
        def print_terminal(parser, kind):
            global output
            global style

            # Simply run the method if we do not print parse tree.
            if display == False:
                return match(parser, kind)

            # Call the function being decorated and get the token matched.
            token = match(parser, kind)

            # Do not output anything for mismatched token or eof.
            if token == None or token.kind == "eof":
                return

            # For textual output
            if parser.style == "text":

                # Calculate the amount of indentation needed by counting the
                # number of non-terminals in the stack, as each non-terminal
                # introduces 2 spaces to the identation.
                indent = ""
                for i in range(len(parser.stack)):
                    indent += "  "

                output += indent + str(token) + "\n"

            # For graph output
            elif parser.style == "graph":
                # If the token is a keyword, display their kind.
                if (token.value == None):
                    t = token.kind
                # Otherwise display their value.
                else:
                    t = token.value

                # Set the label and shape of the node. The ID of the node is
                # "p" + start position of the token.
                output += (
                    "    \"p" + str(token.start_pos) + "\" [label=\"" + str(t)
                    + "\", shape=diamond];\n"
                )

                # If this node has a parent, create an edge from the parent to
                # the this node. Note that the parent will always be the
                # non-terminal on top of the stack.
                prev = parser.stack[len(parser.stack) - 1]
                output += (
                    "    \"" + str(parser.stack[len(parser.stack) - 1][1])
                    + "\" -> \"p" + str(token.start_pos) + "\";\n"
                )
            return token

        return print_terminal