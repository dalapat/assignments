from Box import Box

class CGIntegerBox(Box):

    def __init__(self):
        self.size = 4
        self.offset = 0

    def get_offset(self):
        return self.offset

    def get_size(self):
        return self.size