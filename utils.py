import sys
from Constraint import Constraint
from scipy.spatial import distance

def lt(one, two):
	return one < two
def gt(one, two):
	return one > two

def getConstraintsFromCNF(cnf, constraintId, splotModel):
	clauseList = [clause.strip() for clause in cnf.split("or")]
	treeNodeIdList = [clause if (clause.find("~") == -1) else clause[1:] for clause in clauseList]
	return Constraint(constraintId, clauseList, treeNodeIdList, splotModel)

def bdom(one, two, weights):
	"""
	Return True if 'one' dominates 'two'
	"""
	dominates = False
	for i in range(len(one)):
	  better = lt if weights[i]<0 else gt
	  # TODO 3: Use the varaibles declared above to check if one dominates two
	  if better(one[i], two[i]):
			dominates = True
	  elif one[i]!=two[i]: 
			return False
	return dominates
 

def igd(obtained, ideals):
	igd_val = 0
	for d in ideals:
		min_dist = sys.maxint
		for o in obtained:
			min_dist = min(min_dist, distance.euclidean(o, d))
		igd_val += min_dist
	return igd_val/len(ideals)