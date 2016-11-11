class TreeNode:
    def __init__(self, id, name, type):
        self.name = name
        self.type = type
        self.id = id
        self.children = []

    def __str__(self):
        return self.id+ " " + self.name +" (" + self.type + ")"