from Box import Box

class RecordBox(Box):
    def __init__(self, record):
        self.value = record

    def __str__(self):
        return "RecordBox"