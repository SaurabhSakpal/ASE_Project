class Constraint:
    def __init__(self, constraintId, clauses, treeNodeList, splotModel):
        self.constraintId = constraintId
        self.clauses = clauses
        self.treeNodeList = [splotModel.getTreeNodeFromId(nodeId) for nodeId in treeNodeList]