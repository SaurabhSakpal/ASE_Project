from Constraint import Constraint

def lt(one, two):
	return one < two
def gt(one, two):
	return one > two

def getConstraintsFromCNF(cnf, constraintId, splotModel):
    clauseList = [clause.strip() for clause in cnf.split("or")]
    treeNodeIdList = [clause if (clause.find("~") == -1) else clause[1:] for clause in clauseList]
    return Constraint(constraintId, clauseList, treeNodeIdList, splotModel)

def bdom(one, two):
    """
    Return True if 'one' dominates 'two'
    """
    dominates = False
    for i, obj in enumerate(problem.objectives):
      better = lt if obj.do_minimize else gt
      # TODO 3: Use the varaibles declared above to check if one dominates two
      if better(one[i], two[i]):
            dominates = True
      elif one[i]!=two[i]: 
            return False
    return dominates
  
def fitness(one, dom):
    return len([1 for another in reference if dom(one, another)])