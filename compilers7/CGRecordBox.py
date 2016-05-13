from Box import Box

class CGRecordBox(Box):

    def __init__(self, fields):
        self.value = fields
        self.offset = 0
        self.size = 0