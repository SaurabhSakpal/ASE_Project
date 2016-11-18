from TreeStructureConstraint import TreeConstraintGenerator
class SplotModel:
    def __init__(self, name):
        self.root = None
        self.modelName = name
        self.crossTreeConstraints = []
        self.treeNodeMap = {}
        self.treeConstraints = []

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

    def printCrossTreeConstraints(self):
        for constraint in self.crossTreeConstraints:
            print constraint

    def printTreeConstraints(self):
        for constraint in self.treeConstraints:
            print constraint

    def generateTreeStructureConstraints(self,treeNode):
        for i in xrange(len(treeNode.children)):
            child = treeNode.children[i]
            self.treeConstraints.extend(TreeConstraintGenerator.getConstraints(treeNode, child, self))
            self.generateTreeStructureConstraints(treeNode.children[i])

    def printStatistics(self):
        print "MODEL ("+self.modelName+") STATISTICS\n"
        print "Total Cross Tree Constraints : " + str(len(self.crossTreeConstraints))
        print "Total Tree Structure  Constraints : " + str(len(self.treeConstraints))
        print "Total Nodes in the tree : " + str(len(self.treeNodeMap))
