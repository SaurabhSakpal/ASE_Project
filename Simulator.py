import random
from Point import Point
import pycosat

class Simulator:
    def __init__(self, splotModel):
        self.model = splotModel
        self.population_limit  = 100
        self.startPopulation = []

    def setPopulationSize(self, size):
        self.population_limit = size

    def generateInitialPopulation(self):
        self.startPopulation = self.satSolveLeaves()

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
            #print point
            print "\n"
            n_point_list.append(Point(self.model, point))
        return n_point_list

    def satSolveLeaves(self):
        constraint_list = self.model.crossTreeConstraints
        tree_constraint_list = self.model.treeConstraints
        constraint_list.extend(tree_constraint_list)

        id2tag = {i + 1: v for i, v in enumerate(list(self.model.nodeOrder))}
        tag2id = {v: i + 1 for i, v in enumerate(list(self.model.nodeOrder))}
        sat_input = []
        for constraint in constraint_list:
            clause_encoding = []
            for clause in constraint.clauses:
                node_tag = clause[1:] if clause[0] == '~' else clause
                mult = - 1 if clause[0] == '~' else 1
                clause_encoding.append(mult * tag2id[node_tag])
            sat_input.append(clause_encoding)
        #print sat_input
        validPopulation = []
        count = 0
        for sol in pycosat.itersolve(sat_input, len(self.model.nodeOrder)):
            validPopulation.append(sol)
            count += 1
            if count == (self.population_limit * 10):
                break
        #print 'count =', count
        population = []
        for index in xrange(len(validPopulation)):
            ind = [1 if i > 0 else 0 for i in validPopulation[index]]
            population.append(ind)
        print population
        return population

    def satSolveCrossTreeConstraints(self):
        mandatoryNodes = []
        print self.model.crossTreeConstraints
        constraint_list = self.model.crossTreeConstraints
        sat_vars = set([node.id for constraint in constraint_list for node in constraint.treeNodeList])
        id2tag = {i + 1: v for i, v in enumerate(list(sat_vars))}
        tag2id = {v: i + 1 for i, v in enumerate(list(sat_vars))}

        sat_input = []
        for constraint in constraint_list:
            clause_encoding = []
            for clause in constraint.clauses:
                node_tag = clause[1:] if clause[0] == '~' else clause
                mult = - 1 if clause[0] == '~' else 1
                clause_encoding.append(mult * tag2id[node_tag])
            sat_input.append(clause_encoding)
        print id2tag
        #print sat_input
        count = 0
        for sol in pycosat.itersolve(sat_input):
            mandatoryNodes.append(sol)
            if count == (self.population_limit * 10):
                break
            count += 1
        print 'count =', count
        allPartialSolutions = []
        for partialSolution in mandatoryNodes:
            solnMap = {}
            for i in partialSolution:
                if i > 0:
                    solnMap[id2tag[i]] = True
                else:
                    solnMap[id2tag[i*-1]] = False
            allPartialSolutions.append(solnMap)
        #print allPartialSolutions
        return allPartialSolutions

    def dfsPartial(self, treeNode, point, parentDecision, partialSolutionMap):
        if parentDecision and treeNode.type == "Mandatory":
            point.append([treeNode.id, True])
            parentDecision = True
            for i in xrange(len(treeNode.children)):
                self.dfsPartial(treeNode.children[i], point, parentDecision)
        elif parentDecision and treeNode.type == "Optional":
            if random.random() < 0.5:
                parentDecision =  True
                point.append([treeNode.id, True])
            else:
                parentDecision = False
                point.append([treeNode.id, False])
            for i in xrange(len(treeNode.children)):
                self.dfsPartial(treeNode.children[i], point, parentDecision)
        elif parentDecision and treeNode.type == "Featured Group":
            if treeNode.maxCardinality == 1 and treeNode.minCardinality == 1:
                index = random.choice(xrange(len(treeNode.children)))
                for i in xrange(len(treeNode.children)):
                    if index == i:
                        parentDecision =  True
                        point.append([treeNode.children[i].id, True])
                        self.dfsPartial(treeNode.children[i], point, parentDecision)
                    else:
                        parentDecision = False
                        point.append([treeNode.children[i].id, False])
                        self.dfsPartial(treeNode.children[i], point, parentDecision)
            elif treeNode.minCardinality == 1 and treeNode.maxCardinality == -1:
                choiceString = self.getOrRelationshipChoiceString(len(treeNode.children))
                for i in xrange(len(treeNode.children)):
                    if choiceString[i] == '1':
                        parentDecision = True
                        point.append([treeNode.children[i].id, True])
                        self.dfsPartial(treeNode.children[i], point, parentDecision)
                    else:
                        parentDecision = False
                        point.append([treeNode.children[i].id, False])
                        self.dfsPartial(treeNode.children[i], point, parentDecision)
        elif parentDecision and treeNode.type == "Group":
            for i in xrange(len(treeNode.children)):
                self.dfsPartial(treeNode.children[i], point, parentDecision)
        elif parentDecision and treeNode.type == "Root":
            point.append([treeNode.id, True])
            parentDecision = True
            for i in xrange(len(treeNode.children)):
                self.dfsPartial(treeNode.children[i], point, parentDecision)
        elif not parentDecision:
            if treeNode.type == "Mandatory" or treeNode.type == "Optional":
                point.append([treeNode.id, False])
            elif treeNode.type == "Featured Group":
                for i in xrange(len(treeNode.children)):
                    point.append([treeNode.children[i].id, False])
            for i in xrange(len(treeNode.children)):
                self.dfsPartial(treeNode.children[i], point, parentDecision)

    def solveTree(self):
        partialSolutions = self.satSolveCrossTreeConstraints()
        for soln in partialSolutions:
            #print "\n\n\n"
            print len(soln)
            #print "\n"
            for key in list(soln):
                temp = self.model.treeNodeMap[key]
                if soln[key]:
                    while temp.parentNode != None:
                        temp = temp.parentNode
                        if temp.type != "Featured Group":
                            soln[temp.id] = True
                        else:
                            temp = temp.parentNode
            #print soln
            #print sorted(soln.items())
        for i in partialSolutions:
            point = []
            print len(i)
            #self.dfsPartial(self.model.root, point, True, i)
        return []