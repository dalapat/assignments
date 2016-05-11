from Entry import Entry

class Type(Entry):
    # superclass of Array, Integer, Record

    def __init__(self):
        self.size = 0

    def set_size(self, value):
        self.size = value

    def get_size(self):
        return self.size

