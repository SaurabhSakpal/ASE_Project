from Model import *
from parser import *
from Constraint import *
from TreeNode import *

class TreeConstraintGenerator:

    @staticmethod
    def getConstraintId(parentId, childId):
        return "c: " + parentId + " : " + childId

    @staticmethod
    def getMandatoryConstraints(parentId, childId, splotModel):
        return [SPLOTParser.getConstraintsFromCNF(parentId+" or ~"+childId, TreeStructureConstraintGenerator.getConstraintId(parentId, childId), splotModel),
                SPLOTParser.getConstraintsFromCNF("~"+ parentId + " or " + childId, TreeStructureConstraintGenerator.getConstraintId(parentId, childId), splotModel)]

    @staticmethod
    def getOptionalConstraints(parentId, childId, splotModel):
        return [SPLOTParser.getConstraintsFromCNF(parentId + " or ~" + childId, TreeStructureConstraintGenerator.getConstraintId(parentId, childId), splotModel)]

    @staticmethod
    def getFeatureGroupConstraints(parentNode, childNode, splotModel):
        if type(childNode) == FeaturedGroupTreeNode:
            if childNode.minCardinality == 1 and childNode.maxCardinality == -1:
                
        return []

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
