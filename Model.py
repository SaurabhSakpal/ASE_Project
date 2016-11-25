from TreeStructureConstraint import TreeConstraintGenerator
class SplotModel:
    def __init__(self, name):
        self.root = None
        self.modelName = name
        self.crossTreeConstraints = []
        self.treeNodeMap = {}
        self.treeConstraints = []
        self.nodeOrder = []
        self.featureFailureCount = {}
        self.maxCost = 0
        self.maxDefect = 0
        self.maxBenefits = 0

    def findMaxObjectives(self):
        maxCost = -1
        maxBenefits = -1
        maxDefects = -1
        for i in self.treeNodeMap:
            maxCost += self.treeNodeMap[i].cost
            maxBenefits += self.treeNodeMap[i].benefits
            maxDefects += self.treeNodeMap[i].defects
        self.maxCost = maxCost
        self.maxDefect = maxDefects
        self.maxBenefits = maxBenefits

        print maxCost, maxBenefits, maxDefects



    def addTreeNodeToMap(self, treeNode):
        self.treeNodeMap[treeNode.id] = treeNode

    def getTreeNodeFromId(self, nodeId):
        return self.treeNodeMap[nodeId]

    def setConstraints(self, constraintList):
        self.crossTreeConstraints = constraintList

    def updateRootNode(self, rootNode):
        self.root = rootNode
        self.populateNodeOrder(self.root)
        self.findMaxObjectives()

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

    def populateNodeOrder(self, treeNode):
        if treeNode.type != "Featured Group":
            self.nodeOrder.append(treeNode.id)
        for i in xrange(len(treeNode.children)):
            self.populateNodeOrder(treeNode.children[i])

