import sys
import os
from scipy.spatial import distance

def igd_calculator_wrapper(dr):
    global model_name

    result = {}
    true_pf_folder = dr+"/True_PF/"
    obtained_pf_folder = dr+"/Pareto_Fronts/"
    true_pf_file = true_pf_folder + os.listdir(true_pf_folder)[0]
    #obtained_pf_files = [obtained_pf_folder + name for name in os.listdir(obtained_pf_folder)]

    #algorithm_names = [name.split("_")[0] for name in os.listdir(obtained_pf_folder)]
    model_name = [name.split("_")[1] for name in os.listdir(obtained_pf_folder)]
    model_name = model_name[-1]

    true_pf =  [tuple(map(float,line.split(' '))) for line in open(true_pf_file,'r')]
    for algo_file in os.listdir(obtained_pf_folder):
        algorithm_name = algo_file.split("_")[0]
        obtained_pf_file = obtained_pf_folder+algo_file
        obtained_pf = [tuple(map(float,line.split(' ')))for line in open(obtained_pf_file,'r')]
        result[algorithm_name] = igd(obtained_pf, true_pf)

    return result

def igd(obtained, ideals):
    igd_val = 0
    for d in ideals:
        min_dist = sys.maxint
        for o in obtained:
            min_dist = min(min_dist, distance.euclidean(o, d))
        igd_val += min_dist
    return igd_val/len(ideals)

def writeToStatFile(igds):
    global OUT_PATH
    global model_name
    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)
    f = open(OUT_PATH+'igd_'+model_name,'w')
    for opt in igds:
        f.write(opt+' '+' '.join(map(str,igds[opt]))+'\n')

if len(sys.argv) != 2:
    print 'Usage: python igd_runner.py <patht_to_output>'
    exit()
IN_PATH = sys.argv[1]+'/'
OUT_PATH = '../../stats/'
super_dic = {}
model_name = ''
for dr in os.listdir(IN_PATH):
    rslt = igd_calculator_wrapper(IN_PATH+dr)
    for algo in rslt:
        if algo not in super_dic:
            super_dic[algo] = [rslt[algo]]
        else:
            super_dic[algo].append(rslt[algo])

writeToStatFile(super_dic)