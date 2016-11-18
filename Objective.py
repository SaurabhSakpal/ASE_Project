class Objective:
    def __init__(self):
        self.cost = None
        self.constraintsFailed = None
        self.featureRichness = None

    def __str__(self):
        return " Cost: " + str(self.cost) + " ConstraintsFailed: " + str(self.constraintsFailed) + " FeatureRichness: " + str(self.featureRichness)
