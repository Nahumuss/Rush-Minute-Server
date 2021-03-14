class Message(str):
    def __init__(self, targets = []):
        self.targets = targets