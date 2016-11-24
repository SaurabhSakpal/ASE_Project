import random
from Point import Point
import pycosat

class Simulator:
    def __init__(self, splotModel):
        self.model = splotModel

    def getOrRelationshipChoiceString(self, numberOfChild):
        binaryString = ""
        for i in xrange(numberOfChild):
            if random.random() < 0.5:
                binaryString += "1"
            else:
                binaryString += "0"
        if binaryString.find("1") != -1:
            #print binaryString
            return binaryString
        else:
            index = random.choice(xrange(numberOfChild))
            binaryString = ""
            for i in xrange(numberOfChild):
                if i != index:
                    binaryString += "0"
                else:
                    binaryString += "1"
            #print binaryString
            return binaryString



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
                choiceString = self.getOrRelationshipChoiceString(len(treeNode.children))
                for i in xrange(len(treeNode.children)):
                    if choiceString[i] == '1':
                        parentDecision = True
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


    def generateNPoints(self, count=1):
        n_point_list = []
        for i in xrange(count):
            point = []
            self.dfs(self.model.root, point, True)
            print point
            print "\n"
            n_point_list.append(Point(self.model, point))
        return n_point_list

    def generateCrossTreePivots(self):
        tree_map = self.model.treeNodeMap
        constraint_list = self.model.crossTreeConstraints
        sat_vars = set([node.id for constraint in constraint_list for node in constraint.treeNodeList])
        id2tag = {i+1: v for i,v in enumerate(list(sat_vars))} 
        tag2id = {v: i+1 for i,v in enumerate(list(sat_vars))} 
        
        sat_input = []
        for constraint in constraint_list:
            clause_encoding = []
            for clause in constraint.clauses:
                node_tag = clause[1:] if clause[0]=='~' else clause
                mult = - 1 if clause[0]=='~' else 1
                clause_encoding.append(mult*tag2id[node_tag])
            sat_input.append(clause_encoding)

        solution = pycosat.solve(sat_input)
        cross_tree_pivots = {id2tag[abs(val)]: 0 if val<0 else 1 for val in solution}
        # count = 0
        # for sol in pycosat.itersolve(sat_input):
        #     count +=1
        # print 'count =', count
        #print cross_tree_pivots
        
        sol_nodes = cross_tree_pivots.keys()
        for k in cross_tree_pivots.keys():
            print self.model.treeNodeMap[k].type, cross_tree_pivots[k]
        for tag in sol_nodes:
            isPresent = 1 if cross_tree_pivots[tag] else 0
            parent = tree_map[tag].parentNode
            while parent:
                cross_tree_pivots[parent.id] = isPresent
                parent = tree_map[parent.id].parentNode

        return cross_tree_pivots

    def dfs2(self, treeNode, point, cross_tree_pivots):
        if treeNode.type == "Mandatory" or treeNode.type == "Root":
            point[treeNode.id] = True
            for i in xrange(len(treeNode.children)):
                self.dfs2(treeNode.children[i], point, cross_tree_pivots)
        
        elif treeNode.type == "Optional":
            if random.random() < 0.5:
                point[treeNode.id] = True
                for i in xrange(len(treeNode.children)):
                    self.dfs2(treeNode.children[i], point, cross_tree_pivots)
        elif treeNode.type == "Featured Group":
            if treeNode.maxCardinality == 1 and treeNode.minCardinality == 1:
                index = random.choice(xrange(len(treeNode.children)))
                #point.append([treeNode.children[index].id, True])
                self.dfs2(treeNode.children[index], point, cross_tree_pivots)

            elif treeNode.minCardinality == 1 and treeNode.maxCardinality == -1:
                choiceString = self.getOrRelationshipChoiceString(len(treeNode.children))
                for i in xrange(len(treeNode.children)):
                    if choiceString[i] == '1':
                        #point.append([treeNode.children[i].id, True])
                        self.dfs2(treeNode.children[i], point, cross_tree_pivots)
        elif treeNode.type == "Group":
            for i in xrange(len(treeNode.children)):
                self.dfs2(treeNode.children[i], point, cross_tree_pivots)
       
    def cnfSatisfiedTree(self):
        cross_tree_pivots = self.generateCrossTreePivots()
        point = {}
        #self.dfs2(self.model.root, point, cross_tree_pivots)
        #print point

