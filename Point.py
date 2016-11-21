from Objective import *

class Point(object):
    def __init__(self, model, value):
        self.model = model
        self.value = value
        self.objectives = Objective()

    def evaluateObjectives(self):
        self.objectives.cost = self.evaluateCost()
        self.objectives.featureRichness = self.evaluateFeatureRichness()
        self.objectives.constraintsFailed = self.evaluateConstraintsFailed()

    def evaluateCost(self):
        """ Code for calculating cost of the given point goes here """
        #value = [[id1,True],[id2,True],[id3,False]...]
        #print 'find cost'
        return sum([self.model.treeNodeMap[n[0]].cost if n[1] else 0.0 for n in self.value])

    def evaluateConstraintsFailed(self):
        """ Code for calculating how many constraints the point failed goes here """
        constraints_list = self.model.crossTreeConstraints
        leaves = [n[0] for n in self.value if n[1] is True]
        violations = 0
        for constraint in constraints_list:
            clauses = constraint.clauses
            isTrue = False
            for clause in clauses:
                node_id = clause[1:] if clause[0]=='~' else clause
                if (clause[0] =='~' and node_id not in leaves) or (clause[0] !='~' and node_id in leaves):
                    isTrue = isTrue or True
            if not isTrue:
                violations += 1
                for i in self.value:
                    node_id = i[0]
                    if i[1]:
                        if node_id in self.model.featureFailureCount:
                            self.model.featureFailureCount[node_id] += 1
                        else:
                            self.model.featureFailureCount[node_id] = 1
        return violations

    def evaluateFeatureRichness(self):
        """ Code for calculating Feature Richness of a point goes here """
        return sum([1 if n[1] else 0 for n in self.value])
