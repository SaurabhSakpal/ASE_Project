from __future__ import print_function
import sys
import os
import utils

path_to_output = sys.argv[1]

def lt(one, two):
	return one < two
def gt(one, two):
	return one > two	

for dr in os.listdir(path_to_output):
	path_obtained_pf = path_to_output+'/'+dr+'/'+'Pareto_Fronts'
	true_pf_file = path_to_output+'/'+dr+'/'+'True_PF'
	if not os.path.exists(true_pf_file):
		os.makedirs(true_pf_file)
	reference_set = []
	retain_size = 0
	for file in os.listdir(path_obtained_pf):
		model_name = file.split('_')[-1]
		f = open(path_obtained_pf+'/'+file,'r')
		print(path_obtained_pf+'/'+file,'r')
		content = [tuple(map(float,line.split(' '))) for line in f]
		reference_set.extend(content)
		retain_size = len(content)

	true_pf_file = true_pf_file+'/'+model_name

	def fitness(one):
		return len([1 for another in reference_set if utils.cdom(one, another,[-1.0, -1.0, 1.0, -1.0, 1.0])])

	fitnesses = []
	for point in reference_set:
		fitnesses.append((fitness(point), point))
	reference_set = [tup[1] for tup in sorted(fitnesses, reverse=True)]
	wf = open(true_pf_file,'w')
	reference_set = reference_set[:retain_size]
	for point in reference_set:
		print(' '.join(map(str,point)),file=wf)

	