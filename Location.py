from Expression import Expression

class Location(Expression):
    def __init__(self):
        super(Location, self).__init__("Location")

    def __str__(self):
        return "Location"