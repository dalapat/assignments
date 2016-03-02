from Entry import Entry

class Constant(Entry):

    def __init__(self, type, value):
        # what's the point of Entry?
        self.type = type
        self.value = value #make this 5 for now

    def get_value(self):
        return self.value
