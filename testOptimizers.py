from __future__ import print_function
import sys
import numpy as np
from parser import SPLOTParser
from Simulator import Simulator
import numpy as np
from Optimisers import *
import matplotlib.pyplot as plt

def writeToFile(paretos, folder, pareto_name):
    colors = ['r','b']
    for c,algo in enumerate(paretos):
        fit_array = np.array(paretos[algo], dtype=float)
        fit_array_norm = fit_array/ fit_array.max(axis=0)
        f = open(folder+pareto_name+'_'+algo+'.txt','w')
        for i in range(fit_array_norm.shape[0]):
            print(fit_array_norm[i,:])
            print(' '.join(map(str, fit_array_norm[i,:].tolist())), file=f)
        plt.scatter(fit_array_norm[:,0],fit_array_norm[:,2], color=colors[c])
    plt.savefig('./graph/pareto.png')

def writeTruePareto(paretos, folder, file):
    reference_set = []
    for algo in paretos:
        reference_set.extend(paretos[algo])
    reference_set = np.array(reference_set, dtype=float)

def main():
    assert len(sys.argv) == 2, "SPLOT Parser takes path to model.xml file as argument"
    modelFile = sys.argv[1]
    model = SPLOTParser().parse(modelFile)
    model.generateTreeStructureConstraints(model.root)

    algos = [nsga2, ga]
    simulator = Simulator(model)
    n = 1000
    cost = []
    violations = []
    num_features = []
    pareto_folder = './Spread-HyperVolume/HyperVolume/Pareto_Fronts/'
    true_pareto_folder = './Spread-HyperVolume/Spread/True_PF/'
    paretos = {}
    for algo in algos:
        paretos[algo.__name__] = runOptimiser(simulator, model, algo)
    writeToFile(paretos, pareto_folder, modelFile.split('/')[1].split('.')[0])
    writeTruePareto(paretos, true_pareto_folder, modelFile.split('/')[1].split('.')[0])

if __name__ == "__main__":
    main()