from Objective import *

class Point:
    def __init__(self, model, value):
        self.model = model
        self.value = value
        self.objectives = Objective()

    def evaluateObjectives(self):
        self.objectives.cost = self.evaluateCost()
        self.objectives.featureRichness = self.evaluateFeatureRichness()
        self.objectives.constraintsFailed = self.evaluateConstraintsFailed()

    def evaluateCost(self):
        """ Code for calculating cost of the given point goes here """

    def evaluateConstraintsFailed(self):
        """ Code for calculating how many constraints the point failed goes here """

    def evaluateFeatureRichness(self):
        """ Code for calculating Feature Richness of a point goes here """
