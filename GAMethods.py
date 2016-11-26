import random

def getIndividualPoint(simulator):
    pointList = simulator.generateNPoints()
    #print "\n\n --------------------------------\n"
    #print pointList[0].value
    #pointList[0].evaluateObjectives()
    #print pointList[0].objectives
    ind = [1 if i[1] == True else 0 for i in pointList[0].value]
    #print ind
    return ind

def getSATSolverGeneratedPoint(simulator):
    startPopulation = simulator.startPopulation
    individual = startPopulation[random.choice(xrange(len(startPopulation)))]
    return individual


def evaluateObjectives(model, ind1):
    cost = evaluateCost(ind1, model)
    featureRichness = evaluateFeatureRichness(ind1)
    constraintsFailed = evaluateConstraintsFailed(ind1, model)
    defects = evaluateDefects(ind1, model)
    benefits = evaluateBenefits(ind1, model)
    return (cost, constraintsFailed, featureRichness, defects, benefits)


def evaluateCost(ind1, model):
    """ Code for calculating cost of the given point goes here """
    # value = [[id1,True],[id2,True],[id3,False]...]
    # print 'find cost'
    return sum([model.treeNodeMap[model.nodeOrder[i]].cost if ind1[i] == 1 else 0 for i in range(len(ind1))])

def evaluateBenefits(ind1, model):
    """ Code for calculating cost of the given point goes here """
    # value = [[id1,True],[id2,True],[id3,False]...]
    # print 'find cost'
    return sum([model.treeNodeMap[model.nodeOrder[i]].benefits if ind1[i] == 1 else 0 for i in range(len(ind1))])

def evaluateDefects(ind1, model):
    """ Code for calculating cost of the given point goes here """
    # value = [[id1,True],[id2,True],[id3,False]...]
    # print 'find cost'
    return sum([model.treeNodeMap[model.nodeOrder[i]].defects if ind1[i] == 1 else 0 for i in range(len(ind1))])


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
    return violations


def evaluateFeatureRichness(ind1):
    """ Code for calculating Feature Richness of a point goes here """
    return sum(ind1)

def printPopulation(pop):
    for i in pop:
        print str(i) + " : " + str(i.fitness.values)


def getOrRelationshipChoiceString(numberOfChild):
    binaryString = ""
    for i in xrange(numberOfChild):
        if random.random() < 0.5:
            binaryString += "1"
        else:
            binaryString += "0"
    if binaryString.find("1") != -1:
        # print binaryString
        return binaryString
    else:
        index = random.choice(xrange(numberOfChild))
        binaryString = ""
        for i in xrange(numberOfChild):
            if i != index:
                binaryString += "0"
            else:
                binaryString += "1"
        # print binaryString
        return binaryString

def dfs_mutate(treeNode, point, parentDecision, nodeDecisions, isMutated):
    if parentDecision and treeNode.type == "Mandatory":
        point.append([treeNode.id, nodeDecisions[treeNode.id]])
        parentDecision = True
        for i in xrange(len(treeNode.children)):
            dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
    elif parentDecision and treeNode.type == "Optional":
        if not isMutated:
            if random.random() < 0.8:
                parentDecision = nodeDecisions[treeNode.id]
                point.append([treeNode.id, nodeDecisions[treeNode.id]])
            else:
                isMutated = True
                parentDecision = not nodeDecisions[treeNode.id]
                point.append([treeNode.id, not nodeDecisions[treeNode.id]])
            for i in xrange(len(treeNode.children)):
                dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
        else:
            if random.random() < 0.5:
                parentDecision = True
                point.append([treeNode.id, True])
            else:
                parentDecision = False
                point.append([treeNode.id, False])
            for i in xrange(len(treeNode.children)):
                dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
    elif parentDecision and treeNode.type == "Featured Group":
        if isMutated:
            if treeNode.maxCardinality == 1 and treeNode.minCardinality == 1:
                index = random.choice(xrange(len(treeNode.children)))
                for i in xrange(len(treeNode.children)):
                    if index == i:
                        parentDecision = True
                        point.append([treeNode.children[i].id, True])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
                    else:
                        parentDecision = False
                        point.append([treeNode.children[i].id, False])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
            elif treeNode.minCardinality == 1 and treeNode.maxCardinality == -1:
                choiceString = getOrRelationshipChoiceString(len(treeNode.children))
                for i in xrange(len(treeNode.children)):
                    if choiceString[i] == '1':
                        parentDecision = True
                        point.append([treeNode.children[i].id, True])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
                    else:
                        parentDecision = False
                        point.append([treeNode.children[i].id, False])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
        else:
            if treeNode.maxCardinality == 1 and treeNode.minCardinality == 1:
                if random.random() < 0.8:
                    isMutated = False
                    for i in xrange(len(treeNode.children)):
                        parentDecision = nodeDecisions[treeNode.children[i].id]
                        point.append([treeNode.children[i].id, nodeDecisions[treeNode.children[i].id]])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, False)
                else:
                    isMutated = True
                    index = random.choice(xrange(len(treeNode.children)))
                    for i in xrange(len(treeNode.children)):
                        if index == i:
                            parentDecision = True
                            point.append([treeNode.children[i].id, True])
                            dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, True)
                        else:
                            parentDecision = False
                            point.append([treeNode.children[i].id, False])
                            dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, True)
            elif treeNode.minCardinality == 1 and treeNode.maxCardinality == -1:
                for i in xrange(len(treeNode.children)):
                    if random.random() < 0.8:
                        parentDecision = nodeDecisions[treeNode.children[i].id]
                        point.append([treeNode.children[i].id, nodeDecisions[treeNode.children[i].id]])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
                    else:
                        parentDecision = not nodeDecisions[treeNode.children[i].id]
                        point.append([treeNode.children[i].id, (not nodeDecisions[treeNode.children[i].id])])
                        dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, True)

    elif parentDecision and treeNode.type == "Group":
        for i in xrange(len(treeNode.children)):
            dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)
    elif parentDecision and treeNode.type == "Root":
        point.append([treeNode.id, True])
        parentDecision = True
        for i in xrange(len(treeNode.children)):
            dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, False)
    elif not parentDecision:
        if treeNode.type == "Mandatory" or treeNode.type == "Optional":
            point.append([treeNode.id, False])
        elif treeNode.type == "Featured Group":
            for i in xrange(len(treeNode.children)):
                point.append([treeNode.children[i].id, False])
        for i in xrange(len(treeNode.children)):
            dfs_mutate(treeNode.children[i], point, parentDecision, nodeDecisions, isMutated)


def dfs_mate(treeNode, point, parentDecision, dadDecisions, momDecisions, selectedParent):
    if parentDecision and treeNode.type == "Mandatory":
        if selectedParent == 1:
            point.append([treeNode.id, dadDecisions[treeNode.id]])
            parentDecision = dadDecisions[treeNode.id]
            for i in xrange(len(treeNode.children)):
                dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions, 1)
        elif selectedParent == 2:
            point.append([treeNode.id, momDecisions[treeNode.id]])
            parentDecision = momDecisions[treeNode.id]
            for i in xrange(len(treeNode.children)):
                dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions, 2)
        elif selectedParent == 0:
            point.append([treeNode.id, True])
            parentDecision = True
            for i in xrange(len(treeNode.children)):
                dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions, 0)
    elif parentDecision and treeNode.type == "Optional":
        if selectedParent == 1:
            parentDecision = dadDecisions[treeNode.id]
            point.append([treeNode.id, dadDecisions[treeNode.id]])
            for i in xrange(len(treeNode.children)):
                dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions, 1)
        elif selectedParent == 2:
            parentDecision = momDecisions[treeNode.id]
            point.append([treeNode.id, momDecisions[treeNode.id]])
            for i in xrange(len(treeNode.children)):
                dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions, 2)
        elif selectedParent == 0:
            if random.random() < 0.5:
                selectedParent = 1
                parentDecision = dadDecisions[treeNode.id]
                point.append([treeNode.id, dadDecisions[treeNode.id]])
                for i in xrange(len(treeNode.children)):
                    dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions, selectedParent)
            else:
                selectedParent = 2
                parentDecision = momDecisions[treeNode.id]
                point.append([treeNode.id, momDecisions[treeNode.id]])
                for i in xrange(len(treeNode.children)):
                    dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions, selectedParent)
    elif parentDecision and treeNode.type == "Featured Group":
        if selectedParent == 0:
            if random.random < 0.5:
                for i in xrange(len(treeNode.children)):
                    parentDecision = dadDecisions[treeNode.children[i].id]
                    point.append([treeNode.children[i].id, dadDecisions[treeNode.children[i].id]])
                    dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions, 1)
            else:
                for i in xrange(len(treeNode.children)):
                    parentDecision = momDecisions[treeNode.children[i].id]
                    point.append([treeNode.children[i].id, momDecisions[treeNode.children[i].id]])
                    dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions,2)
        else:
            for i in xrange(len(treeNode.children)):
                parentDecision = momDecisions[treeNode.children[i].id] if selectedParent == 2 else dadDecisions[treeNode.children[i].id]
                point.append([treeNode.children[i].id, parentDecision])
                dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions, selectedParent)
    elif parentDecision and treeNode.type == "Group":
        for i in xrange(len(treeNode.children)):
            dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions, selectedParent)
    elif parentDecision and treeNode.type == "Root":
        point.append([treeNode.id, True])
        parentDecision = True
        for i in xrange(len(treeNode.children)):
            dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions, selectedParent)
    elif not parentDecision:
        if treeNode.type == "Mandatory" or treeNode.type == "Optional":
            point.append([treeNode.id, False])
        elif treeNode.type == "Featured Group":
            for i in xrange(len(treeNode.children)):
                point.append([treeNode.children[i].id, False])
        for i in xrange(len(treeNode.children)):
            dfs_mate(treeNode.children[i], point, parentDecision, dadDecisions, momDecisions, selectedParent)



def matePoints(model, ind1, ind2):
    """ Logic for mate/crossover goes here  """
    dadDecisions = {}
    for index in range(len(ind1)):
        dadDecisions[model.nodeOrder[index]] = (ind1[index]==1)
    momDecisions = {}
    for index in range(len(ind2)):
        momDecisions[model.nodeOrder[index]] = (ind2[index]==1)
    point1 = []
    dfs_mate(model.root, point1, True, dadDecisions, momDecisions, 0)
    point2 = []
    dfs_mate(model.root, point2, True, dadDecisions, momDecisions, 0)
    #print point1
    #print point2
    i1 = [1 if i[1] == True else 0 for i in point1]
    i2 = [1 if i[1] == True else 0 for i in point2]
    for index in range(len(i1)):
        ind1[index] = i1[index]

    for index in range(len(i2)):
        ind2[index] = i2[index]


def mutatePoints(model, ind1):
    """ Logic for mutation goes here """
    nodeDecisions = {}
    for index in range(len(ind1)):
        nodeDecisions[model.nodeOrder[index]] = (ind1[index]==1)
    point = []
    dfs_mutate(model.root , point, True, nodeDecisions, False)
    ind = [1 if i[1] == True else 0 for i in point]
    #print str(ind1) + " ---> " + str(ind)
    for index in range(len(ind)):
        ind1[index] = ind[index]

def selectNSGA2(individuals, k, nd='standard'):
    """Apply NSGA-II selection operator on the *individuals*. Usually, the
    size of *individuals* will be larger than *k* because any individual
    present in *individuals* will appear in the returned list at most once.
    Having the size of *individuals* equals to *k* will have no effect other
    than sorting the population according to their front rank. The
    list returned contains references to the input *individuals*. For more
    details on the NSGA-II operator see [Deb2002]_.
    
    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :param nd: Specify the non-dominated algorithm to use: 'standard' or 'log'.
    :returns: A list of selected individuals.
    
    .. [Deb2002] Deb, Pratab, Agarwal, and Meyarivan, "A fast elitist
       non-dominated sorting genetic algorithm for multi-objective
       optimization: NSGA-II", 2002.
    """
    if nd == 'standard':
        pareto_fronts = sortNondominated(individuals, k)
    elif nd == 'log':
        pareto_fronts = sortLogNondominated(individuals, k)
    else:
        raise Exception('selNSGA2: The choice of non-dominated sorting '
                        'method "{0}" is invalid.'.format(nd))

    for front in pareto_fronts:
        assignCrowdingDist(front)
    
    chosen = list(chain(*pareto_fronts[:-1]))
    k = k - len(chosen)
    if k > 0:
        sorted_front = sorted(pareto_fronts[-1], key=attrgetter("fitness.crowding_dist"), reverse=True)
        chosen.extend(sorted_front[:k])
        
    return chosen