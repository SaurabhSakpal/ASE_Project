import sys
from parser import SPLOTParser
from Simulator import Simulator

assert len(sys.argv) == 2, "SPLOT Parser takes path to model.xml file as argument"
modelFile = sys.argv[1]
model = SPLOTParser().parse(modelFile)
#model.printTree(model.root, 0)
model.generateTreeStructureConstraints(model.root)
simulator = Simulator(model)
print len(simulator.satSolveLeaves())
