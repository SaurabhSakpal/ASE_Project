from Constraint import Constraint

def getConstraintsFromCNF(cnf, constraintId, splotModel):
    clauseList = [clause.strip() for clause in cnf.split("or")]
    treeNodeIdList = [clause if (clause.find("~") == -1) else clause[1:] for clause in clauseList]
    return Constraint(constraintId, clauseList, treeNodeIdList, splotModel)
