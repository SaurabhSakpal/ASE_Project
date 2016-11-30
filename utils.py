import sys
from Constraint import Constraint
from scipy.spatial import distance
import math

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
 
def cdom(one, two, weights):
    """Returns whether or not *wvalues1* dominates *wvalues2*.
    
    :param wvalues1: The weighted fitness values that would be dominated.
    :param wvalues2: The weighted fitness values of the dominant.
    :returns: :obj:`True` if wvalues2 dominates wvalues1, :obj:`False`
              otherwise. Dominates = Continuous Dominates
    """
    one = [x*w for x,w in zip(one,weights)]
    two = [x*w for x,w in zip(two,weights)]
    def expLoss(x1, y1, n):
        return -1*math.e**( (x1 - y1) / n )

    def loss(x, y):
        losses = []
        n = len(x)

        for self_wvalue, other_wvalue in zip(x, y):
            losses += [expLoss( self_wvalue, other_wvalue, n)]

        return sum(losses) / n

    l1 = loss(one, two)
    l2 = loss(two, one)
    # print "\t" + str(l1) +" : " + str(l2)
    return l1 < l2

def igd(obtained, ideals):
	igd_val = 0
	for d in ideals:
		min_dist = sys.maxint
		for o in obtained:
			min_dist = min(min_dist, distance.euclidean(o, d))
		igd_val += min_dist
	return igd_val/len(ideals)