import unittest
from Entry import Entry
from Constant import Constant
from Variable import Variable
from Type import Type
from Integer import Integer
from Array import Array
from Record import Record
from Scope import Scope
from Node import Node
from Instruction import Instruction
from Condition import Condition
from Expression import Expression
from Assign import Assign
from If import If
from Repeat import Repeat
from Read import Read
from Write import Write


class TestSymbolTable(unittest.TestCase):

# Simple Unit tests for Scope, Entry, and Entry's descendents.
    def test_entry(self):
        e = Entry()
        self.assertEqual("Entry", str(e))

    def test_type(self):
        t = Type()
        self.assertEqual("Type", str(t))

    def test_integer(self):
        i = Integer()
        self.assertEqual("INTEGER", str(i))

    def test_constant(self):
        c = Constant(Integer(), 5)
        self.assertEqual("Constant(INTEGER: 5)", str(c))

    def test_variable(self):
        v = Variable(Integer())
        self.assertEqual("Variable(INTEGER)", str(v))
    
    def test_array(self):
        a = Array(Integer(), 5)
        self.assertEqual("Array length 5 of INTEGER", str(a))
    
    def test_scope(self):
        s = Scope(None)
        self.assertEqual("Scope", str(s))
        self.assertEqual(None, s.outer)

    def test_scope_outer(self):
        u = Scope(None)
        p = Scope(u)
        self.assertEqual(None, u.outer)
        self.assertEqual(u, p.outer)

    def test_scope_insert(self):
        s = Scope(None)
        i = Integer()
        s.insert("Integer", i)
        self.assertEqual(i, s.find("Integer"))

    def test_scope_local(self):
        u = Scope(None)
        i = Integer()
        u.insert("Integer", i)
        p = Scope(u)
        c = Constant(i, 5)
        p.insert("const", c)

        self.assertTrue(u.local("Integer"))
        self.assertTrue(p.local("const"))
        self.assertEqual(None, u.find("const"))
        self.assertEqual(i, p.find("Integer"))

    def test_record(self):
        s = Scope(None)
        r = Record(s)
        self.assertEqual("Record", str(r))


    # Tests for AST classes
    def test_Node(self):
        n = Node()
        self.assertEqual("Node", str(n))

    def test_Instruction(self):
        i = Instruction(None)
        self.assertEqual("Instruction", str(i))
        self.assertEqual(None, i.next)
        i2 = Instruction(i)
        self.assertEqual("Instruction", str(i2.next))

    def test_Condition(self):
        c = Condition("left", "right", ">=")
        self.assertEqual("Condition", str(c))
        self.assertEqual("left", str(c.left))
        self.assertEqual("right", str(c.right))
        self.assertEqual(">=", str(c.relation))


if __name__ == "__main__":
    unittest.main()