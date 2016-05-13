from Box import Box
import sys

class RecordBox(Box):

    def __init__(self, fields):
        self.value = fields
        self.length = len(fields)

    def get_field(self, field):
        return self.value[field]

    def copy(self, record_box):
        if not isinstance(record_box, RecordBox):
            sys.stderr.write("error: cannot copy non-recordbox type to RecordBox")
            exit(1)
        if not self.length == record_box.length:
            sys.stderr.write("error: number of fields mismatched")

        for field in record_box.value:
            self.value[field] = record_box.value[field]