from __future__ import print_function
import sys
import numpy as np
from parser import SPLOTParser
from Simulator import Simulator
import numpy as np
from Optimisers import *
import matplotlib.pyplot as plt
import utils

def writeToFile(paretos, folder, pareto_name):
    colors = ['r','b']
    cc = 0
    for algo in paretos:
        fit_array = np.array(paretos[algo], dtype=float)
        print('fit array shape',fit_array.shape)
        num_obj = fit_array.shape[1]
        fit_array_norm = np.vstack(tuple([fit_array[:,c]/max(1,np.max(fit_array[:,c])) for c in range(num_obj)]))
        #fit_array_norm = fit_array/ fit_array.max(axis=0)
        fit_array_norm = fit_array_norm.T
        print('norm shape',fit_array_norm.shape)
        print(fit_array_norm)
        f = open(folder+algo+'_'+pareto_name+'.txt','w')
        for i in range(fit_array_norm.shape[0]):
            print(' '.join(map(str, fit_array_norm[i,:].tolist())), file=f)
        
        plt.scatter(fit_array_norm[:,0],fit_array_norm[:,2], color=colors[cc])
        cc += 1
    plt.savefig('./graphs/pareto.png')

def writeTruePareto(paretos, dom, folder, file):
    reference_set = []
    retain_size = sum([len(paretos[k]) for k in paretos])/len(paretos)
    print('retain_size = ', retain_size)
    for algo in paretos:
        reference_set.extend(paretos[algo])
    #reference_set = np.array(reference_set, dtype=float)
    def fitness(one, dom):
        return len([1 for another in reference_set if dom(one, another,[-1.0, -1.0, 1.0, -1.0, 1.0])])
    
    fitnesses = []
    for point in reference_set:
        fitnesses.append((fitness(point, dom), point))
    reference_set = [tup[1] for tup in sorted(fitnesses, reverse=True)]
    f = open(folder+file+'.txt','w')
    reference_set = reference_set[:retain_size]
    for point in reference_set:
        print(' '.join(map(str,point)),file=f)

    return reference_set

def main():
    assert len(sys.argv) == 2, "SPLOT Parser takes path to model.xml file as argument"
    modelFile = sys.argv[1]
    model = SPLOTParser().parse(modelFile)
    model.generateTreeStructureConstraints(model.root)

    algos = [nsga2Cdom, nsga2]
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
    reference_set = writeTruePareto(paretos, utils.bdom, true_pareto_folder, modelFile.split('/')[1].split('.')[0])

    for opt in paretos:
        print(opt+' = ',utils.igd(paretos[opt],reference_set))
if __name__ == "__main__":
    main()