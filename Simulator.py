from TreeNode import *
from Model import *
from Constraint import *
import random

class Simulator:
    def __init__(self, splotModel):
        self.model = splotModel


    def dfs(self, treeNode, point, parentDecision):
        if parentDecision and treeNode.type == "Mandatory":
            point.append([treeNode.id, True])
            parentDecision = True
            for i in xrange(len(treeNode.children)):
                self.dfs(treeNode.children[i], point, parentDecision)
        elif parentDecision and treeNode.type == "Optional":
            if random.random() < 0.5:
                parentDecision =  True
                point.append([treeNode.id, True])
            else:
                parentDecision = False
                point.append([treeNode.id, False])
            for i in xrange(len(treeNode.children)):
                self.dfs(treeNode.children[i], point, parentDecision)
        elif parentDecision and treeNode.type == "Featured Group":
            if treeNode.maxCardinality == 1 and treeNode.minCardinality == 1:
                index = random.choice(xrange(len(treeNode.children)))
                for i in xrange(len(treeNode.children)):
                    if index == i:
                        parentDecision =  True
                        point.append([treeNode.children[i].id, True])
                        self.dfs(treeNode.children[i], point, parentDecision)
                    else:
                        parentDecision = False
                        point.append([treeNode.children[i].id, False])
                        self.dfs(treeNode.children[i], point, parentDecision)
            elif treeNode.minCardinality == 1 and treeNode.maxCardinality == -1:
                for i in xrange(len(treeNode.children)):
                    if random.random() < 0.5:
                        parentDecision =  True
                        point.append([treeNode.children[i].id, True])
                        self.dfs(treeNode.children[i], point, parentDecision)
                    else:
                        parentDecision = False
                        point.append([treeNode.children[i].id, False])
                        self.dfs(treeNode.children[i], point, parentDecision)
        elif parentDecision and treeNode.type == "Group":
            for i in xrange(len(treeNode.children)):
                self.dfs(treeNode.children[i], point, parentDecision)
        elif parentDecision and treeNode.type == "Root":
            point.append([treeNode.id, True])
            parentDecision = True
            for i in xrange(len(treeNode.children)):
                self.dfs(treeNode.children[i], point, parentDecision)
        elif not parentDecision:
            if treeNode.type == "Mandatory" or treeNode.type == "Optional":
                point.append([treeNode.id, False])
            elif treeNode.type == "Featured Group":
                for i in xrange(len(treeNode.children)):
                    point.append([treeNode.children[i].id, False])
            for i in xrange(len(treeNode.children)):
                self.dfs(treeNode.children[i], point, parentDecision)


    def generatePoint(self, count=1):
        point = []
        self.dfs(self.model.root, point, True)
        print point
