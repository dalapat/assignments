from Box import Box

class IntegerBox(Box):
    def __init__(self):
        self.value = 0

    def __str__(self):
        return "IntegerBox(" + str(self.value) + ")"