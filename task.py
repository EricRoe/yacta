class Task:
    def __init__(self, text, tags, priority, id):
        self.text = text
        self.tags = tags
        self.priority = priority
        self.id = id


    def __str__(self):
        return '{} :: tags:{} :: priority:{} :: id:{}'\
                .format(self.text, self.tags, self.priority, id(self))