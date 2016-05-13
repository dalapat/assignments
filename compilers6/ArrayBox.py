from Box import Box
import sys

'''
Simulate storage space for an identifier
that acts as an array in Simple
'''
class ArrayBox(Box):

    # initializes an array box
    def __init__(self, list):
        self.value = list # actual array elements
        self.length = len(list) # length of array

    # returns the array element at index i
    def index(self, i):
        if 0 <= i < self.length:
            return self.value[i]
        else:
            sys.stderr.write("error: index out of bounds")
            exit(1)

    # copies the elements of one array to another
    def set(self, array):
        if not isinstance(array, ArrayBox):
            sys.stderr.write("error: cannot copy nonarray to array")
            exit(1)
        if not self.length == array.length:
            sys.stderr.write("error: lengths of array are different")
            exit(1)
        for i in range(array.length):
            self.value[i] = array.list[i]

