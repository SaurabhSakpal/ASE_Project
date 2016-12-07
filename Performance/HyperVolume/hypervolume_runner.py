from hypervolume import InnerHyperVolume
import os
import sys

class HyperVolumeContainer():
    def __init__(self, filename, results):
        self.name = filename
        self.dimension = len(results[0])
        self.results = results  # list of list
        self.reference_point = None
        self.hypervolume = None

    def get_reference_point(self):
        if self.reference_point is None:
            dimension = len(self.results[0])
            self.reference_point = [max([result[i] for result in self.results]) for i in xrange(dimension)]
        return self.reference_point

    def set_reference_point(self, reference_point):
        assert(len(reference_point) == self.dimension), \
            "Length of the reference point should be equal to dimension of the problem"
        self.reference_point = reference_point

    def set_hypervolume(self, hypervolume):
        if self.hypervolume is None: self.hypervolume = hypervolume
        else: print "HyperVolume has already been set"

    def get_hypervolume(self):
        return self.hypervolume

    def __str__(self):
        return "Name: " + self.name + " HyperVolume: " + str(self.hypervolume)


def file_reader(filepath, separator=" "):
    from os.path import isfile
    assert(isfile(filepath) == True), "file doesn't exist"
    content = []
    for line in open(filepath, "r"):
        content.append([float(element) for element in line.split(separator) if element != "\n"])
    return content


def HyperVolume(list_result_object):
    """Receives list of  HyperVolumeContainer"""
    # Calculate the reference points: This is for minimization problems only
    dimension = list_result_object[0].dimension
    # find the maximum point of each coordinate and increase it to 150%
    reference_point = [1.5 * max([one.get_reference_point()[i] for one in list_result_object]) for i in xrange(dimension)]

    result_dic = {}
    HV = InnerHyperVolume(reference_point)
    for result_object in list_result_object:
        result_object.hypervolume = HV.compute(result_object.results)
        result_dic[result_object.name] = result_object.hypervolume
    return result_dic

def writeToStatFile(hypervolumes):
    global OUT_PATH
    model_name = hypervolumes.keys()[0].split('_')[1]
    full_path = OUT_PATH+'hv_'+model_name
    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)
    f = open(full_path,'w')
    for opt in hypervolumes:
        f.write(opt.split('_')[0]+' '+' '.join(map(str,hypervolumes[opt]))+'\n')

def HyperVolume_wrapper():
    global IN_PATH
    folder_path = "Pareto_Fronts/"
    super_dic = {}
    for config in os.listdir(IN_PATH):
        filenames = [IN_PATH+config+'/'+folder_path + file for file in os.listdir(IN_PATH+config+'/'+folder_path)]
        fronts = [HyperVolumeContainer(filename.split("/")[-1], file_reader(filename)) for filename in filenames]
        hvs = HyperVolume(fronts)
        for k in hvs:
            if k in super_dic:
                super_dic[k].append(hvs[k])
            else:
                super_dic[k] = [hvs[k]]
    writeToStatFile(super_dic)

if len(sys.argv) != 2:
    print 'Usage: python hypervlume_runner.py <patht_to_output>'
    exit()
IN_PATH = sys.argv[1]+'/'
OUT_PATH = '../../stats/'
HyperVolume_wrapper()