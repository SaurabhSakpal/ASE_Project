def getIndividualPoint(simulator):
    pointList = simulator.generateNPoints()
    #print "\n\n --------------------------------\n"
    #print pointList[0].value
    pointList[0].evaluateObjectives()
    #print pointList[0].objectives
    ind = [1 if i[1] == True else 0 for i in pointList[0].value]
    #print ind
    return ind

def evaluateObjectives(model, ind1):
    cost = evaluateCost(ind1, model)
    featureRichness = evaluateFeatureRichness(ind1)
    constraintsFailed = evaluateConstraintsFailed(ind1, model)
    return (cost, constraintsFailed,featureRichness)


def evaluateCost(ind1, model):
    """ Code for calculating cost of the given point goes here """
    # value = [[id1,True],[id2,True],[id3,False]...]
    # print 'find cost'
    return sum([model.treeNodeMap[model.nodeOrder[i]].cost if ind1[i] == 1 else 0 for i in range(len(ind1))])


def evaluateConstraintsFailed(ind1, model):
    """ Code for calculating how many constraints the point failed goes here """
    constraints_list = model.crossTreeConstraints
    leaves = [model.nodeOrder[i] for i in range(len(ind1)) if ind1[i] is 1]
    #leaves = [n[0] for n in self.value if n[1] is True]
    violations = 0
    for constraint in constraints_list:
        clauses = constraint.clauses
        isTrue = False
        for clause in clauses:
            node_id = clause[1:] if clause[0] == '~' else clause
            if (clause[0] == '~' and node_id not in leaves) or (clause[0] != '~' and node_id in leaves):
                isTrue = isTrue or True
        if not isTrue:
            violations += 1
            for index in xrange(len(ind1)):
                node_id = model.nodeOrder[index]
                if ind1[index] == 1:
                    if node_id in model.featureFailureCount:
                        model.featureFailureCount[node_id] += 1
                    else:
                        model.featureFailureCount[node_id] = 1
    # print 'find violations'
    return violations


def evaluateFeatureRichness(ind1):
    """ Code for calculating Feature Richness of a point goes here """
    return sum(ind1)

def printPopulation(pop):
    for i in pop:
        print str(i) + " : " + str(i.fitness.values)


def matePoints(model, ind1, ind2):
    """ Logic for mate/crossover goes here  """
    ind1[len(ind1)-3] = 1
    ind2[len(ind2) - 3] = 1


def mutatePoints(model, ind1):
    """ Logic for mutation goes here """
    ind1[len(ind1) - 1] = 1

