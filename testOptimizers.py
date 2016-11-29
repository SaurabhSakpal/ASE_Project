from __future__ import print_function
import sys
import numpy as np
from parser import SPLOTParser
from Simulator import Simulator
import numpy as np
from Optimisers import *
import matplotlib.pyplot as plt
import utils

def writeToFile(opt2paretos, folder, pareto_name):
    colors = ['r','b']
    cc = 0
    for opt in opt2paretos:
        fit_array = np.array(opt2paretos[opt], dtype=float)
        num_obj = fit_array.shape[1]
        fit_array_norm = np.vstack(tuple([fit_array[:,c]/max(1,np.max(fit_array[:,c])) for c in range(num_obj)]))
        #fit_array_norm = fit_array/ fit_array.max(axis=0)
        fit_array_norm = fit_array_norm.T

        f = open(folder+opt+'_'+pareto_name+'.txt','w')
        for i in range(fit_array_norm.shape[0]):
            print(' '.join(map(str, fit_array_norm[i,:].tolist())), file=f)
        
        plt.scatter(fit_array_norm[:,0],fit_array_norm[:,2], color=colors[cc])
        cc += 1
    plt.savefig('./graphs/pareto_'+pareto_name+'.png')

def writeTruePareto(opt2paretos, dom, folder, file):
    reference_set = []
    retain_size = sum([len(opt2paretos[k]) for k in opt2paretos])/len(opt2paretos)
    #print('retain_size = ', retain_size)
    for opt in opt2paretos:
        reference_set.extend(opt2paretos[opt])
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
    assert len(sys.argv) == 4, "SPLOT Parser takes path to model.xml file as argument"
    modelFile = sys.argv[1]
    MU = int(sys.argv[2])
    NGEN = int(sys.argv[3])
    model = SPLOTParser().parse(modelFile)
    model.generateTreeStructureConstraints(model.root)

    optimisers = [ga, nsga2]
    simulator = Simulator(model)
    cost = []
    violations = []
    num_features = []
    pareto_folder = './output/Pareto_Fronts/'
    true_pareto_folder = './output/True_PF/'
    opt2paretos = {}
    for optimiser in optimisers:
        opt2paretos[optimiser.__name__] = runOptimiser(simulator, model, optimiser, MU, NGEN)
        print('done running'+optimiser.__name__)
    writeToFile(opt2paretos, pareto_folder, modelFile.split('/')[1].split('.')[0])
    reference_set = writeTruePareto(opt2paretos, utils.bdom, true_pareto_folder, modelFile.split('/')[1].split('.')[0])

    for opt in opt2paretos:
        print(opt+' = ',utils.igd(opt2paretos[opt],reference_set))
if __name__ == "__main__":
    main()