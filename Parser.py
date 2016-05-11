# Eric Calder
# ecalder6@jhu.edu

# The parser currently outputs a concrete syntax tree, a symbol table, or an
# abstract syntax tree from tokens provided by a scanner.
# The output can be in textual or graphical form. No outputs will
# be given when encountered token type mismatch, but the parser will parse the
# entire code and outputs the errors found.

import copy
from Scanner import *
from Error import *
from ParserObserver import *
from Entry import Entry
from Constant import Constant
from Variable import Variable
from Field import Field
from Type import Type
from Integer import Integer
from Invalid import Invalid
from Array import Array
from Record import Record
from Scope import Scope
from Node import Node
from Condition import Condition
from Instruction import Instruction
from Expression import Expression
from Assign import Assign
from If import If
from Repeat import Repeat
from Read import Read
from Write import Write
from Number import Number
from Location import Location
from VariableAST import VariableAST
from Index import Index
from FieldAST import FieldAST
from Binary import Binary
from Box import Box
from ArrayBox import ArrayBox
from RecordBox import RecordBox
from IntegerBox import IntegerBox
from Environment import Environment
from SymbolTableVisitor import SymbolTableVisitor

class Parser:
    def __init__(self, scanner, output_object, parser_type, style):
        """Initializes the parser with a scanner and output style (text or
        graph).
        """
        self.scanner = scanner
        self.last = None
        self.current = None
        self.style = style
        self.parser_type = parser_type
        self.output_object = output_object

        # The stack is used to store non-terminals for output. The
        # ParserObserver uses it to determine indentation and construct
        # edges for the graph.
        self.stack = []

        # Used as IDs for non-terminals in the graph.
        self.graph_index = 0

        # Number of tokens skipped after an error has occured.
        self.num_tokens_skipped = 0

        # Whether to supress error messages.
        self.supress = False

        # Whether to display output (will be false when an error occurs).
        self.display = True

        # The last token mismatched. Used to make sure mismatched tokens do not
        # increment supression counters more than once.
        self.last_mismatch = None

        self.weak_tokens = {";", ":", ",", ")", "]", "END"}

    def next(self):
        """Get the next token. From Peter's lecture."""
        self.last = self.current
        self.current = self.scanner.next()
        while self.current.kind == "INVALID":
            self.current = self.scanner.next()

    def invalid_token(self, e):
        """Handles an invalid token. Will print an error message if not
        supressed.
        """

        if not self.supress:
            self.supress = True
            self.num_tokens_skipped = 0
            self.display = False
            sys.stderr.write(e.message + "\n")

        self.last_mismatch = self.current

    def increment_skip(self):
        """If errors are being supressed, increment tokens skipped."""

        # Do not increment the counter if the token has already been
        # mismatched before.
        if (
            self.supress and (self.last_mismatch == None
            or self.last_mismatch != self.current)
        ):
            self.num_tokens_skipped += 1
            if self.num_tokens_skipped > 7:
                self.supress = False
                self.num_tokens_skipped = 0

    @ParserObserver.terminal
    def match(self, kind):
        """Match a token to kind(s). Parts from Peter's lecture.
        Return the token matched. """
        try:

            self.increment_skip()

            # Match token with a set of kinds.
            if type(kind) is set:

                # Token matched.
                if self.current.kind in kind:
                    self.next()
                    return self.last
                # Token mismatch. Throw an exception.
                else:
                    raise ParserInvalidKindError(kind, self.current)

            # Match token with a single kind
            else:
                # Token matched.
                if self.current.kind == kind:
                    self.next()
                    return self.last
                # Token mismatch. Throw an exception
                else:
                    raise ParserInvalidKindError(kind, self.current)
        except ParserInvalidKindError as e:
            # Handle the exception.
            self.invalid_token(e)

    def sync(self, kinds, terminals):
        """Resync the parser when there is a mismatch of non-weak symbols.
        The function will skip tokens until reaching a strong token in kinds
        or a symbol that terminates the program.
        """

        # Skip until finding a strong symbol in kinds.
        while self.current.kind not in kinds:
            # Raise an exception due to mismatch
            try:
                raise ParserInvalidKindError("Type", self.current)
            except ParserInvalidKindError as e:
                self.invalid_token(e)

            # The program ended before the parser is able to sync. end the loop.
            if self.current.kind in terminals:
                return False

            # Skip the current token.
            self.next()

        # Sucessfully re-synced the parser.
        return True

    def insert(self, name, value):
        """Insert an entry into the symbol table."""
        try:
            if self.current_scope.local(name.value):
                raise DuplicateDeclarationError(name)
            self.current_scope.insert(name.value, value)
        except DuplicateDeclarationError as e:
            self.invalid_token(e)

    def find(self, name):
        """Find an identifier in the symbol table."""
        try:
            entry = self.current_scope.find(name)
            if entry == None:
                raise EntryNotFoundInSymbolTable(self.last)
            return entry
        except EntryNotFoundInSymbolTable as e:
            self.invalid_token(e)

    def set_record_scope(self, entry):
        """Set the current scope to be a record's scope."""
        if isinstance(entry, Variable) or isinstance(entry, Field):
            # Record can be either in variable or field.
            if (
                isinstance(entry.type, Array)
                and isinstance(entry.type.element_type, Record)
                ):
                # An array of record.
                self.record_scope = entry.type.element_type.scope
            elif isinstance(entry.type, Record):
                # a record variable.
                self.record_scope = entry.type.scope
            else:
                self.record_scope = None
        else:
            self.record_scope = None

    def negate_relation(self, relation):
        """Negate the relation in a condition."""
        negation_map = {"=":"#", "#":"=", ">":"<=", 
                        "<":">=", ">=":"<", "<=":">"}
        return negation_map[relation]

    @ParserObserver.selector
    def selector(self, location):
        """Match the grammar of a selector."""
        ret = None

        # 0 to many patterns.
        while True:
            if self.current.kind == "[":
                self.match("[")

                self.stack.append("ExpressionList")
                expressions = self.expression_list()

                self.match("]")

                for expression in expressions:
                    if (
                        not isinstance(location, Location)
                        or not isinstance(location.type, Array)
                    ):
                        # Not an array variable.
                        try:
                            raise InvalidArray(location.type, self.last)
                        except InvalidArray as e:
                            self.invalid_token(e)

                    cur = Index(location, expression)
                    cur.token = self.last
                    ret = cur
                    location = cur

            elif self.current.kind == ".":
                self.match(".")
                name = self.match("identifier")
                if name == None:
                    continue

                if self.record_scope == None:
                    # Not a record variable.
                    try:
                        raise InvalidRecord(location.type, self.last)
                    except InvalidRecord as e:
                        self.invalid_token(e)
                        break

                # Access the record's scope and find the variable with name.
                self.current_scope = self.record_scope
                entry = self.find(name.value)
                var = VariableAST(name.value, entry)

                self.set_record_scope(entry)

                cur = FieldAST(location, var)
                ret = cur
                location = cur
            else:
                #Pattern ended.
                break

        self.current_scope = self.program_scope
        return ret

    @ParserObserver.non_terminal
    def designator(self):
        """Match the grammar for a designator."""
        name = self.match("identifier")
        if name == None:
            return None
        entry = self.find(name.value)
        if isinstance(entry, Constant):
            var = Number(entry)
        elif isinstance(entry, Variable):
            var = VariableAST(name.value, entry)
        else:
            # Identifier in designator cannot be a type.
            try:
                raise InvalidDesignator(entry, self.last)
            except InvalidDesignator as e:
                self.invalid_token(e)
                return VariableAST("INVALID", Variable(Invalid()))


        self.set_record_scope(entry)

        self.stack.append("Selector")
        ret = self.selector(var)

        if ret == None:
            ret = var

        if not isinstance(ret, Location) and not isinstance(ret, Number):
            try:
                raise InvalidDesignator(ret.type, self.last)
            except InvalidDesignator as e:
                self.invalid_token(e)
                return VariableAST("INVALID", Variable(Invalid()))

        return ret

    @ParserObserver.non_terminal
    def identifier_list(self):
        """Match the grammar for a identifier list."""
        id_list = []
        identifier = self.match("identifier")
        id_list.append(identifier)

        # 0 to many patterns.
        while True:
            if self.current.kind == ",":
                self.match(",")
                identifier = self.match("identifier")
                id_list.append(identifier)
            else:
                # Pattern ended.
                break

        return id_list

    @ParserObserver.non_terminal
    def expression_list(self):
        """Match the grammar for a expression list."""
        exp_list = []
        self.stack.append("Expression")
        exp_list.append(self.expression())

        # 0 to many patterns.
        while True:
            if self.current.kind == ",":
                self.match(",")

                self.stack.append("Expression")
                expression = self.expression()
                exp_list.append(expression)
            else:
                # Pattern ended.
                break

        return exp_list

    @ParserObserver.non_terminal
    def read(self):
        """Match the grammar for a read."""
        self.match("READ")

        self.stack.append("Designator")
        location = self.designator()

        if (
            not isinstance(location, Location) 
            or location.type != self.integer_type
        ):
            # Not an integer variable.
            try:
                raise InvalidRead(location.type, self.last)
            except InvalidRead as e:
                self.invalid_token(e)

        r = Read(location)
        r.token = self.last
        return r

    @ParserObserver.non_terminal
    def write(self):
        """Match the grammar for a write."""
        self.match("WRITE")

        self.stack.append("Expression")
        expression = self.expression()

        if expression.type != self.integer_type:
            # Not an integer.
            try:
                raise InvalidWrite(expression.type, self.last)
            except InvalidWrite as e:
                self.invalid_token(e)

        return Write(expression)

    @ParserObserver.non_terminal
    def condition(self):
        """Match the grammar for a condition."""
        self.stack.append("Expression")
        left = self.expression()

        # Match a token with a set of kinds.
        kinds = {"=", "#", "<", ">", "<=", ">="}
        relation = self.match(kinds)

        self.stack.append("Expression")
        right = self.expression()

        if (
            left.type != self.integer_type
            or right.type != self.integer_type
        ):
            # Either is not of Constant or Variable of type integer.
            try:
                raise InvalidCondition(
                    left.type, right.type, self.last
                )
            except InvalidCondition as e:
                self.invalid_token(e)

        return Condition(left, right, relation.kind)

    @ParserObserver.non_terminal
    def while_instruction(self):
        """Match the grammar for a while."""
        self.match("WHILE")

        self.stack.append("Condition")
        condition = self.condition()
        
        self.match("DO")

        self.stack.append("Instructions")
        instructions = self.instructions()

        self.match("END")

        # Replaces while with repeat in AST
        left = condition.left
        right = condition.right
        inverse = self.negate_relation(condition.relation)

        inverse_left = copy.deepcopy(left)
        inverse_right = copy.deepcopy(right)

        inverse_condition = Condition(inverse_left, inverse_right, inverse)

        repeat = Repeat(inverse_condition, instructions)
        repeat.next = None
        return If(condition, repeat, None)

    @ParserObserver.non_terminal
    def repeat(self):
        """Match the grammar for a repeat."""
        self.match("REPEAT")

        self.stack.append("Instructions")
        instructions = self.instructions()

        self.match("UNTIL")

        self.stack.append("Condition")
        condition = self.condition()
        
        self.match("END")

        return Repeat(condition, instructions)

    @ParserObserver.non_terminal
    def if_instruction(self):
        """Match the grammar for an if."""
        self.match("IF")

        self.stack.append("Condition")
        condition = self.condition()

        self.match("THEN")

        self.stack.append("Instructions")
        instructions_true = self.instructions()
        instructions_false = None

        # Optional match.
        if self.current.kind == "ELSE":
            self.match("ELSE")
            self.stack.append("Instructions")
            instructions_false = self.instructions()

        self.match("END")

        return If(condition, instructions_true, instructions_false)

    @ParserObserver.non_terminal
    def assign(self):
        """Match the grammar for an assign."""
        self.stack.append("Designator")
        location = self.designator()

        self.match(":=")

        self.stack.append("Expression")
        expression = self.expression()

        if (
            not isinstance(location, Location)
            or location.type != expression.type
        ):
            # Left side is not variable, or right side is a type, or types of
            # both sides do not match up.
            try:
                raise InvalidAssignment(
                    location.type, expression.type, self.last
                    )
            except InvalidAssignment as e:
                self.invalid_token(e)

        return Assign(location, expression)

    @ParserObserver.non_terminal
    def instruction(self):
        """Match the grammar for an instruction."""
        
        # The set of kinds to be matched.
        kinds = {"identifier", "IF", "REPEAT", "WHILE", "READ", "WRITE"}

        # The symbols that signal end of an instruction. In this case,
        # . and eof singal the end of the program, which must be the
        # end of an instruction.
        terminals = {"END", ".", "eof"}

        if self.current.kind == "identifier":
            self.stack.append("Assign")
            return self.assign()
        elif self.current.kind == "IF":
            self.stack.append("If")
            return self.if_instruction()
        elif self.current.kind == "REPEAT":
            self.stack.append("Repeat")
            return self.repeat()
        elif self.current.kind == "WHILE":
            self.stack.append("While")
            return self.while_instruction()
        elif self.current.kind == "READ":
            self.stack.append("Read")
            return self.read()
        elif self.current.kind == "WRITE":
            self.stack.append("Write")
            return self.write()
        elif self.current.kind == "END":
            # END signifies the end of instructions.
            return None
        else:
            # No match is made and no END of ending instructions. An error has
            # occured and the symbol missing is not weak. The parser must resync
            # with the code.
            if not self.sync(kinds, terminals):
                return None

    @ParserObserver.non_terminal
    def instructions(self):
        """Match the grammar for instructions."""
        self.stack.append("Instruction")
        head = instruction = self.instruction()

        # 0 or more patterns.
        while True:

            # These symbols preceed or end instructions. End the loop.
            if self.current.kind in {
                "THEN", "ELSE", "REPEAT", "DO", "END", "UNTIL", ".", "eof"
            }:
                break

            # A normal or a mismatch. If necessary resync will happen in
            # instruction.
            else:
                self.match(";")

                self.stack.append("Instruction")
                next_instruction = self.instruction()
                if next_instruction == None:
                    continue
                instruction.next = next_instruction
                instruction = instruction.next

        if instruction != None:
            instruction.next = None
        return head

    @ParserObserver.non_terminal
    def factor(self):
        """Match the grammar for a factor."""
        ret = None
        if self.current.kind == "integer":
            num = self.match("integer")
            const = Constant(self.integer_type, num.value)
            ret = Number(const)
        elif self.current.kind == "identifier":
            self.stack.append("Designator")
            ret = self.designator()

        elif self.current.kind == "(":
            self.match("(")

            self.stack.append("Expression")
            ret = self.expression()

            self.match(")")
        else:
            # An error has occured. Raise and catch it so we can handle the
            # error without crashing the program.
            try:
                self.increment_skip()
                raise ParserInvalidKindError("Factor", self.current)
            except ParserInvalidKindError as e:
                self.invalid_token(e)
        return ret

    @ParserObserver.non_terminal
    def term(self):
        """Match the grammar for a term."""
        self.stack.append("Factor")
        operator_map = {"*":"*", "DIV":"/", "MOD":"%"}
        cur = self.factor()

        # 0 or more patterns.
        while True:
            if (
                self.current.kind == "*" or self.current.kind == "DIV"
                or self.current.kind == "MOD"
            ):
                if self.current.kind == "*":
                    operator = self.match("*")
                elif self.current.kind == "DIV":
                    operator = self.match("DIV")
                else:
                    operator = self.match("MOD")

                self.stack.append("Factor")
                var = self.factor()

                if isinstance(cur, Number) and isinstance(var, Number):
                    # Constant folding.
                    try:
                        val = int(eval(
                                str(cur.entry.value) 
                                + str(operator_map[operator.kind]) 
                                + str(var.entry.value)
                                ))
                    except ZeroDivisionError:
                        # Divide by 0 error.
                        self.invalid_token(DivideByZero(self.last))
                        break

                    const = Constant(self.integer_type, val)
                    cur = Number(const)
                else:
                    if (
                        isinstance(cur, VariableAST) 
                        and (isinstance(cur.variable, Array) 
                            or isinstance(cur.variable, Record)
                        )
                    ):
                        # Trying to perform an operation on non-integers.
                        try:
                            raise InvalidArithmeticOperation(cur, self.last)
                        except InvalidArithmeticOperation as e:
                            self.invalid_token(e)

                    else:
                        cur = Binary(
                            operator.kind, cur, var, self.integer_type
                        )
                        # Remember the token for node in case of run time errors.
                        cur.token = self.last

            else:
                # Pattern ended.
                break

        return cur

    @ParserObserver.non_terminal
    def expression(self):
        """Match the grammar of an expression."""
        operator = None

        if self.current.kind == "+":
            operator = self.match("+")
        elif self.current.kind == "-":
            operator = self.match("-")

        self.stack.append("Term")
        cur = self.term()
        if operator != None and operator.kind == "-":
            # Negate the expression if needed.
            if isinstance(cur, Number):
                # Constant folding.
                cur = Number(
                    Constant(
                        self.integer_type,
                        eval(str(operator.kind) + str(cur.entry.value))
                    )
                )
            else:
                if (
                    isinstance(cur, VariableAST) 
                    and (isinstance(cur.variable, Array) 
                        or isinstance(cur.variable, Record)
                    )
                ):
                    # Trying to perform an operation on non-integers.
                    try:
                        raise InvalidArithmeticOperation(cur, self.last)
                    except InvalidArithmeticOperation as e:
                        self.invalid_token(e)

                else:
                    cur = Binary(
                        operator.kind, 
                        Number(Constant(self.integer_type, 0)), 
                        cur, self.integer_type
                    )

                    # Remember the token for node in case of run time errors.
                    cur.token = self.last

        # 0 or more patterns.
        while True:
            if self.current.kind in {"+", "-"}:
                if self.current.kind == "+":
                    operator = self.match("+")
                else:
                    operator = self.match("-")

                self.stack.append("Term")
                var = self.term()
                if isinstance(cur, Number) and isinstance(var, Number):
                    # Constant folding.
                    cur = Number(
                        Constant(
                            self.integer_type,
                            eval(str(cur.entry.value) + str(operator.kind) 
                            + str(var.entry.value))
                        )
                    )
                else:
                    if (
                        isinstance(cur, VariableAST) 
                        and (isinstance(cur.variable, Array) 
                            or isinstance(cur.variable, Record)
                        )
                    ):
                        # Trying to perform an operation on non-integers.
                        try:
                            raise InvalidArithmeticOperation(cur, self.last)
                        except InvalidArithmeticOperation as e:
                            self.invalid_token(e)
                    else:
                        cur = Binary(
                            operator.kind, cur, var, self.integer_type
                        )

                        # Remember token for node in case of run time errors.
                        cur.token = self.last
            else:
                # Pattern ended.
                break

        if cur == None:
            # Return an invalid variable node in case of parsing errors.
            cur = VariableAST("INVALID", Variable(Invalid()))
        return cur

    @ParserObserver.non_terminal
    def type(self):
        """Match the grammar of a type."""
        type_obj = None
        if self.current.kind == "identifier":
            name = self.match("identifier")

            # Return the type object found in current scope
            try:
                type_obj = self.current_scope.find(name.value)
                if type_obj == None:
                    raise IdentifierUsedBeforeDeclared(name)
                elif not isinstance(type_obj, Type):
                    raise IdentifierDoesNotDenoteType(name, type_obj)
            except (IdentifierUsedBeforeDeclared, IdentifierDoesNotDenoteType)\
            as e:
                type_obj = Invalid()
                self.invalid_token(e)

        elif self.current.kind == "ARRAY":
            self.match("ARRAY")

            self.stack.append("Expression")
            size = self.expression()

            try:
                if (
                    not isinstance(size, Number) 
                    or (isinstance(size, Number) and size.entry.value <= 0)
                ):
                    # Arrays need to have size greater than 0.
                    raise InvalidArraySize(size, self.last)
            except InvalidArraySize as e:
                type_obj = Invalid()
                self.invalid_token(e)
                return type_obj

            self.match("OF")

            self.stack.append("Type")
            t = self.type()

            # Create an Array type object.
            type_obj = Array(t, size.entry.value)
        elif self.current.kind == "RECORD":
            self.match("RECORD")

            # Create a new scope for the record and set the current scope
            # to the record scope.
            record_scope = Scope(self.current_scope)
            self.current_scope = record_scope

            # 0 or more patterns.
            while True:
                if self.current.kind == "identifier":
                    self.stack.append("IdentifierList")
                    id_list = self.identifier_list()

                    self.match(":")

                    self.stack.append("Type")
                    t = self.type()

                    self.match(";")

                    # Insert the type objects into the current scope.
                    field = Field(t)
                    for name in id_list:
                        self.insert(name, field)
                else:
                    # pattern ended.
                    break
            self.match("END")

            # Create a Record object with the current scope. Also set the
            # current scope to the outer scope and remove the outer pointer.
            type_obj = Record(self.current_scope)
            outer = self.current_scope.outer
            self.current_scope.outer = None
            self.current_scope = outer
        else:
            # An error has occured. Raise and catch it so we can handle the
            # error without crashing the program.
            try:
                self.increment_skip()
                raise ParserInvalidKindError("Type", self.current)
            except ParserInvalidKindError as e:
                self.invalid_token(e)

        return type_obj

    @ParserObserver.non_terminal
    def const_decl(self):
        """Match the grammar of a const declaration."""
        self.match("CONST")

        # 0 or more patterns.
        while True:
            if self.current.kind == "identifier":
                name = self.match("identifier")

                self.match("=")

                self.stack.append("Expression")
                value = self.expression()

                self.match(";")


                try:
                    if isinstance(value, Number):
                        # Create Constant object and insert into symbol table.
                        const = Constant(self.integer_type, value.entry.value)
                        self.insert(name, const)
                    else:
                        self.insert(name, Variable(Invalid()))
                        raise InvalidConstantValue(value, self.last)

                except InvalidConstantValue as e:
                    self.invalid_token(e)

            else:
                # Pattern ended.
                break

    @ParserObserver.non_terminal
    def type_decl(self):
        """Match the grammar of a type declaration."""
        self.match("TYPE")

        # 0 or more patterns.
        while True:
            if self.current.kind == "identifier":
                name = self.match("identifier")
                self.match("=")

                self.stack.append("Type")
                t = self.type()

                self.match(";")

                self.insert(name, t)
            else:
                # Pattern ended.
                break

    @ParserObserver.non_terminal
    def var_decl(self):
        """Match the grammar of a var declaration."""
        self.match("VAR")

        # 0 or more patterns.
        while True:
            if self.current.kind == "identifier":
                self.stack.append("IdentifierList")
                id_list = self.identifier_list()

                self.match(":")

                self.stack.append("Type")
                var_type = self.type()

                self.match(";")

                # Create Variable object(s) and insert them into symbol table.
                for name in id_list:
                    var = Variable(var_type)
                    self.insert(name, var)
            else:
                # Pattern ended.
                break

    @ParserObserver.non_terminal
    def declarations(self):
        """Match the grammar of declarations."""

        # Strong symbols for resync
        kinds = {"CONST", "TYPE", "VAR"}

        # Signify end of declaration.
        terminals = {".", "eof", "BEGIN"}

        # 0 or more patterns.
        while True:
            if self.current.kind == "CONST":
                self.stack.append("ConstDecl")
                self.const_decl()
            elif self.current.kind == "TYPE":
                self.stack.append("TypeDecl")
                self.type_decl()
            elif self.current.kind == "VAR":
                self.stack.append("VarDecl")
                self.var_decl()

            # A normal end of declaration.
            elif self.current.kind in {"BEGIN", "END"}:
                break

            # A strong symbol mismatch. Need to resync the parser.
            else:
                if not self.sync(kinds, terminals):
                    return

    @ParserObserver.non_terminal
    def program(self):
        """Match the grammar of the program."""

        # Create the program scope
        self.program_scope = Scope(self.universe_scope)
        self.current_scope = self.program_scope

        self.match("PROGRAM")
        begin_name = self.match("identifier")
        self.match(";")

        self.stack.append("Declarations")
        self.declarations()

        # AST instruction tree.
        tree = None

        # Optional begin symbol.
        if self.current.kind == "BEGIN":
            self.match("BEGIN")

            self.stack.append("Instructions")
            tree = self.instructions()

        self.match("END")
        end_name = self.match("identifier")

        # Throw an exception if there is a program name mismatch
        if (
            begin_name == None or end_name == None or begin_name.value == None 
            or end_name.value == None or begin_name.value != end_name.value
        ):
            try:
                raise ProgramNameMismatch(begin_name, end_name)
            except ProgramNameMismatch as e:
                self.invalid_token(e)

        self.match(".")
        self.match("eof")

        return tree

    def parse(self):
        """Method called by sc to parse the code."""

        # Create the universe scope.
        self.universe_scope = Scope(None)
        self.record_scope = None
        self.integer_type = Integer()
        self.universe_scope.insert("INTEGER", self.integer_type)

        # Start by getting the first token.
        self.next()

        # Start parsing by matching the grammar of program.
        self.stack.append("Program")
        tree = self.program()

        # Display the output only if no error has occured.
        if self.display:
            if self.parser_type == "-t":
                # Set the program scope if printing symbol table.
                self.output_object.program_scope = self.program_scope
            elif self.parser_type == "-a":
                # Set the program scope and instruction tree for AST output.
                self.output_object.program_scope = self.program_scope
                self.output_object.tree = tree
            elif self.parser_type == "-i":
                # Set the environment and instruction tree for interpreter.
                visitor = SymbolTableVisitor()
                self.output_object.env = self.current_scope.accept(visitor)
                self.output_object.tree = tree

            self.output_object.display()