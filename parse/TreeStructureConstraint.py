import utils

class TreeConstraintGenerator:
    
    @staticmethod
    def getConstraintId(parentId, childId):
        return "c:" + parentId + " " + childId

    @staticmethod
    def getMandatoryConstraints(parentId, childId, splotModel):
        return [utils.getConstraintsFromCNF(parentId+" or ~"+childId, TreeConstraintGenerator.getConstraintId(parentId, childId), splotModel),
                utils.getConstraintsFromCNF("~"+ parentId + " or " + childId, TreeConstraintGenerator.getConstraintId(parentId, childId), splotModel)]

    @staticmethod
    def getOptionalConstraints(parentId, childId, splotModel):
        return [utils.getConstraintsFromCNF(parentId + " or ~" + childId, TreeConstraintGenerator.getConstraintId(parentId, childId), splotModel)]

    @staticmethod
    def getFeatureGroupConstraints(parentNode, childNode, splotModel):
        constraints = []
        #print "Hello World"
        if childNode.type == "Featured Group":
            if childNode.minCardinality == 1 and (childNode.maxCardinality == -1 or childNode.maxCardinality == 1):
                for i in childNode.children:
                    if i.type != "Featured Group":
                        constraints.append(utils.getConstraintsFromCNF(parentNode.id + " or ~" + i.id, TreeConstraintGenerator.getConstraintId(parentNode.id, childNode.id), splotModel))
                    else:
                        raise Exception('Exception : Invalid Node Structure | Nested Featured Group Node')
                idlist = [i.id for i in childNode.children if i.type != "Featured Group"]
                cnf = ""
                for id in idlist:
                    cnf = cnf + " or " + id
                cnf = "~" + parentNode.id + cnf
                #print cnf
                constraints.append(utils.getConstraintsFromCNF(cnf, TreeConstraintGenerator.getConstraintId(parentNode.id, childNode.id), splotModel))
            if childNode.minCardinality == 1 and childNode.maxCardinality == 1:
                idlist = [i.id for i in childNode.children if i.type != "Featured Group"]
                cnf_1 = ""
                for id in idlist:
                    cnf_1 = cnf_1 + "~" + id + (" or " if id != idlist[-1] else "")
                #print cnf_1
                constraints.append(utils.getConstraintsFromCNF(cnf_1, TreeConstraintGenerator.getConstraintId(
                    parentNode.id, childNode.id), splotModel))
                for index in range(len(idlist)):
                    cnf_2 = ""
                    for id in idlist:
                        cnf_2 = cnf_2 + ("~" if id != idlist[index] else "") + id + (" or " if id != idlist[-1] else "")
                    #print cnf_2
                    constraints.append(utils.getConstraintsFromCNF(cnf_2, TreeConstraintGenerator.getConstraintId(parentNode.id, childNode.id), splotModel))
        return constraints

    @staticmethod
    def getConstraints(parentNode, childNode, splotModel):
        if childNode.type == "Mandatory":
            #print "Get Mandatory Constraints"
            return TreeConstraintGenerator.getMandatoryConstraints(parentNode.id, childNode.id, splotModel)
        elif childNode.type == "Optional":
            #print "Optional Constraints"
            return TreeConstraintGenerator.getOptionalConstraints(parentNode.id, childNode.id, splotModel)
        elif childNode.type == "Featured Group":
            return TreeConstraintGenerator.getFeatureGroupConstraints(parentNode, childNode, splotModel)
        return []
