class Objective:
    def __init__(self):
        self.cost = 0
        self.constraintsFailed = 0
        self.featureRichness = 0

    def getFeatureRichness(self):
        return self.featureRichness

    def getConstraintsFailed(self):
        return self.contriantsFailed

    def getCost(self):
        return self.cost

    def evaluateCost(self):
        """ Code for calculating cost of the given point goes here """

    def evaluateConstraintsFailed(self):
        """ Code for calculating how many constraints the point failed goes here """

    def evaluateFeatureRichness(self):
        """ Code for calculating Feature Richness of a point goes here """
