class TreeNode:
    def __init__(self, id, name, type):
        self.name = name
        self.type = type
        self.id = id
        self.parentNode = None
        self.children = []

    def __str__(self):
        return self.id+ " " + self.name +" (" + self.type + ") " + (self.parentNode.id if self.parentNode != None else "")

    def updateParentNode(self, parentNode):
        self.parentNode = parentNode


class FeaturedGroupTreeNode(TreeNode):
    def __init__(self, id, name, type, minCard, maxCard):
        TreeNode.__init__(self, id, name, type)
        self.maxCardinality = maxCard
        self.minCardinality = minCard

    def __str__(self):
        return self.id+ " " + self.name +" (" + self.type + ")" + " ["+str(self.minCardinality)+", " +str(self.maxCardinality)+"] " + self.parentNode.id
