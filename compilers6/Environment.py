class Environment:
    def __init__(self):
        self.boxes = {}
        self.length = 0

    def insert(self, name, box):
        """Insert a string, box pair into the enviroment."""
        self.boxes[name] = box
        self.length += 1

    def __len__(self):
        return self.length

    '''
    def exists(self, name):
        """Whether the environment contains a name, box pair."""
        if name in self.boxes:
            return True
        return False
    '''

    def find(self, name):
        """Get the box with the specified name."""
        '''
        if self.exists(name):
            return self.boxes[name]
        else:
            return None
        '''
        try:
            return self.boxes[name]
        except KeyError:
            return None

    def __str__(self):
        return "Enviroment"