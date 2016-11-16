class Objective:
    def __init__(self):
        self.__cost = None
        self.__constraintsFailed = None
        self.__featureRichness = None

    def __str__(self):
        return " Cost: " + str(self.__cost) + " ConstraintsFailed: " + str(self.__constraintsFailed) + " FeatureRichness: " + str(self.__featureRichness)
