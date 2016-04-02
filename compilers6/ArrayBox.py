from Box import Box
import sys
class ArrayBox(Box):

    def __init__(self, list):
        self.list = list
        self.length = len(list)

    def index(self, i):
        if 0 <= i <= self.length:
            return self.list[i]
        else:
            sys.stderr.write("error: index out of bounds")
            exit(1)

    def copy(self, array):
        if not isinstance(array, ArrayBox):
            sys.stderr.write("error: cannot copy nonarray to array")
            exit(1)
        if not self.length == array.length:
            sys.stderr.write("error: lengths of array are different")
            exit(1)
        for i in range(array.length):
            self.list[i] = array.list[i]

