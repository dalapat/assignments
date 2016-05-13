from Box import Box

class CGArrayBox(Box):

    def __init__(self, boxlist):
        self.offset = 0
        self.size = 0
        self.unit_size = 0
        self.length = 0
        self.box_list = boxlist

