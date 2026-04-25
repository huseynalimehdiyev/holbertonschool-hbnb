import uuid

class User:
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())
