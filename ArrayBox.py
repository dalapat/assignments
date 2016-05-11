from Box import Box

class ArrayBox(Box):
    def __init__(self, array):
        self.value = array

    def __str__(self):
        return "ArrayBox"