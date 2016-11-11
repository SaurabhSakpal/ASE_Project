from TreeNode import *
from Constraint import *


class SplotModel:
    def __init__(self, name):
        self.root = None
        self.modelName = name
        self.crossTreeConstraints = []
        self.treeNodeMap = {}

    def addTreeNodeToMap(self, treeNode):
        self.treeNodeMap[treeNode.id] = treeNode

    def getTreeNodeFromId(self, nodeId):
        return self.treeNodeMap[nodeId]

    def setConstraints(self, constraintList):
        self.crossTreeConstraints = constraintList

    def updateRootNode(self, rootNode):
        self.root = rootNode

    def printTree(self, treeNode, tabCount):
        tabs = "\t" * tabCount
        print tabs, treeNode
        for i in xrange(len(treeNode.children)):
            self.printTree(treeNode.children[i], tabCount + 1)

    def printConstraints(self):
        for constraint in self.crossTreeConstraints:
            print constraint