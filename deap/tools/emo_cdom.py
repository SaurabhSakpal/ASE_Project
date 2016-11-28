from __future__ import division
import bisect
import math
import random

from itertools import chain
from operator import attrgetter, itemgetter
from collections import defaultdict

######################################
# Non-Dominated Sorting   (NSGA-II)  #
######################################

def selNSGA2Cdom(individuals, k, nd='standard'):
    """Apply NSGA-II selection operator on the *individuals*. Usually, the
    size of *individuals* will be larger than *k* because any individual
    present in *individuals* will appear in the returned list at most once.
    Having the size of *individuals* equals to *k* will have no effect other
    than sorting the population according to their front rank. The
    list returned contains references to the input *individuals*. For more
    details on the NSGA-II operator see [Deb2002]_.
    
    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :param nd: Specify the non-dominated algorithm to use: 'standard' or 'log'.
    :returns: A list of selected individuals.
    
    .. [Deb2002] Deb, Pratab, Agarwal, and Meyarivan, "A fast elitist
       non-dominated sorting genetic algorithm for multi-objective
       optimization: NSGA-II", 2002.
    """
    if nd == 'standard':
        pareto_fronts = sortNondominated(individuals, k)
    elif nd == 'log':
        pareto_fronts = sortLogNondominated(individuals, k)
    else:
        raise Exception('selNSGA2: The choice of non-dominated sorting '
                        'method "{0}" is invalid.'.format(nd))

    for front in pareto_fronts:
        assignCrowdingDist(front)
    
    chosen = list(chain(*pareto_fronts[:-1]))
    k = k - len(chosen)
    if k > 0:
        sorted_front = sorted(pareto_fronts[-1], key=attrgetter("fitness.crowding_dist"), reverse=True)
        chosen.extend(sorted_front[:k])
        
    return chosen


def sortNondominated(individuals, k, first_front_only=False):
    """Sort the first *k* *individuals* into different nondomination levels 
    using the "Fast Nondominated Sorting Approach" proposed by Deb et al.,
    see [Deb2002]_. This algorithm has a time complexity of :math:`O(MN^2)`, 
    where :math:`M` is the number of objectives and :math:`N` the number of 
    individuals.
    
    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :param first_front_only: If :obj:`True` sort only the first front and
                             exit.
    :returns: A list of Pareto fronts (lists), the first list includes 
              nondominated individuals.

    .. [Deb2002] Deb, Pratab, Agarwal, and Meyarivan, "A fast elitist
       non-dominated sorting genetic algorithm for multi-objective
       optimization: NSGA-II", 2002.
    """
    if k == 0:
        return []

    map_fit_ind = defaultdict(list)
    for ind in individuals:
        map_fit_ind[ind.fitness].append(ind)
    fits = map_fit_ind.keys()
    
    current_front = []
    next_front = []
    dominating_fits = defaultdict(int)
    dominated_fits = defaultdict(list)
    dominatedby_fits = defaultdict(list)
    dominatedCount_fits = defaultdict(int)

    maxValues = []
    for i, fit_i in enumerate(fits):
        if i == 0:
            maxValues = list(fit_i.values)
        else:
            for i in range(len(fit_i.values)):
                if maxValues[i] < fit_i.values[i]:
                    maxValues[i] = fit_i.values[i]

    # print maxValues

    for i, fit_i in enumerate(fits):
        normalised_value = []
        for j in range(len(fit_i.values)):
            if maxValues[j] != 0:
                normalised_value.append(fit_i.wvalues[j] / maxValues[j])
            else:
                normalised_value.append(fit_i.wvalues[j])
        fit_i.normalisedValue = normalised_value
        #print normalised_value

    # Rank first Pareto front
    for i, fit_i in enumerate(fits):
        for fit_j in fits[i+1:]:
            # print str(i) + " : "+str(fits.index(fit_j))
            # print "\t "+ str(fit_i) + " : "+ str(fit_j)
            # print fit_j.normalisedValue
            if fit_i.dominatesCdom(fit_j):
                dominating_fits[fit_j] += 1
                dominated_fits[fit_i].append(fit_j)
                dominatedby_fits[fit_j].append(fit_i)
                dominatedCount_fits[fit_i] += 1
            elif fit_j.dominatesCdom(fit_i):
                dominating_fits[fit_i] += 1
                dominated_fits[fit_j].append(fit_i)
                dominatedby_fits[fit_i].append(fit_j)
                dominatedCount_fits[fit_j] += 1
        if dominating_fits[fit_i] == 0:
            current_front.append(fit_i)

    fronts = [[]]
    for fit in current_front:
        fronts[-1].extend(map_fit_ind[fit])
    pareto_sorted = len(fronts[-1])

    # for i, fit_i in enumerate(fits):
    #     dominatedStr = ""
    #     for fit_d in dominatedby_fits[fit_i]:
    #         dominatedStr  = dominatedStr + " "+ str(fits.index(fit_d))
    #     print str(i) + "("+str(dominating_fits[fit_i])+")(" + str(len(dominated_fits[fit_i])) + ") : " + dominatedStr

    # print "Current Fronts Size: " + str(len(current_front)) + " pareto_shared : " + str(pareto_sorted)
    sorted_points = defaultdict(list)
    test = []
    for key, value in sorted(dominatedCount_fits.iteritems()):
        sorted_points[value].append(key)

    if not first_front_only:
        N = min(len(individuals), k)
        while pareto_sorted < N:
            fronts.append([])
            for count in sorted(sorted_points, reverse=True):
                for fit_p in sorted_points[count]:
                    fronts[-1].extend(map_fit_ind[fit_p])
                    pareto_sorted += 1

    """"
    # Rank the next front until all individuals are sorted or
    # the given number of individual are sorted.
    if not first_front_only:
        N = min(len(individuals), k)
        while pareto_sorted < N:
            fronts.append([])
            for fit_p in current_front:
                templist =  dominated_fits[fit_p]
                for fit_d in dominated_fits[fit_p]:
                    dominating_fits[fit_d] -= 1
                    temp = dominating_fits[fit_d]
                    if dominating_fits[fit_d] == 0:
                        next_front.append(fit_d)
                        pareto_sorted += len(map_fit_ind[fit_d])
                        fronts[-1].extend(map_fit_ind[fit_d])
            current_front = next_front
            next_front = []
    """
    
    return fronts

def assignCrowdingDist(individuals):
    """Assign a crowding distance to each individual's fitness. The 
    crowding distance can be retrieve via the :attr:`crowding_dist` 
    attribute of each individual's fitness.
    """
    if len(individuals) == 0:
        return
    
    distances = [0.0] * len(individuals)
    crowd = [(ind.fitness.values, i) for i, ind in enumerate(individuals)]
    
    nobj = len(individuals[0].fitness.values)
    
    for i in xrange(nobj):
        crowd.sort(key=lambda element: element[0][i])
        distances[crowd[0][1]] = float("inf")
        distances[crowd[-1][1]] = float("inf")
        if crowd[-1][0][i] == crowd[0][0][i]:
            continue
        norm = nobj * float(crowd[-1][0][i] - crowd[0][0][i])
        for prev, cur, next in zip(crowd[:-2], crowd[1:-1], crowd[2:]):
            distances[cur[1]] += (next[0][i] - prev[0][i]) / norm

    for i, dist in enumerate(distances):
        individuals[i].fitness.crowding_dist = dist

def selTournamentDCDCdom(individuals, k):
        """Tournament selection based on dominance (D) between two individuals, if
        the two individuals do not interdominate the selection is made
        based on crowding distance (CD). The *individuals* sequence length has to
        be a multiple of 4. Starting from the beginning of the selected
        individuals, two consecutive individuals will be different (assuming all
        individuals in the input list are unique). Each individual from the input
        list won't be selected more than twice.

        This selection requires the individuals to have a :attr:`crowding_dist`
        attribute, which can be set by the :func:`assignCrowdingDist` function.

        :param individuals: A list of individuals to select from.
        :param k: The number of individuals to select.
        :returns: A list of selected individuals.
        """

        def tourn(ind1, ind2):
            if ind1.fitness.dominatesCdom(ind2.fitness):
                return ind1
            elif ind2.fitness.dominatesCdom(ind1.fitness):
                return ind2

            if ind1.fitness.crowding_dist < ind2.fitness.crowding_dist:
                return ind2
            elif ind1.fitness.crowding_dist > ind2.fitness.crowding_dist:
                return ind1

            if random.random() <= 0.5:
                return ind1
            return ind2

        # start
        map_fit_ind = defaultdict(list)
        for ind in individuals:
            map_fit_ind[ind.fitness].append(ind)
        fits = map_fit_ind.keys()

        maxValues = []
        for i, fit_i in enumerate(fits):
            if i == 0:
                maxValues = list(fit_i.values)
            else:
                for i in range(len(fit_i.values)):
                    if maxValues[i] < fit_i.values[i]:
                        maxValues[i] = fit_i.values[i]

        # print maxValues

        for i, fit_i in enumerate(fits):
            normalised_value = []
            for j in range(len(fit_i.values)):
                if maxValues[j] != 0:
                    normalised_value.append(fit_i.wvalues[j] / maxValues[j])
                else:
                    normalised_value.append(fit_i.wvalues[j])
            fit_i.normalisedValue = normalised_value

        # end
        individuals_1 = random.sample(individuals, len(individuals))
        individuals_2 = random.sample(individuals, len(individuals))

        for ind in individuals_1:
            if len(ind.fitness.normalisedValue) == 0:
                for i in xrange(len(maxValues)):
                    if maxValues[i] != 0:
                        ind.fitness.normalisedValue.append(ind.fitness.wvalues[i] / maxValues[i])
                    else:
                        ind.fitness.normalisedValue.append(ind.fitness.wvalues[i])

        for ind in individuals_2:
            if len(ind.fitness.normalisedValue) == 0:
                for i in xrange(len(maxValues)):
                    if maxValues[i] != 0:
                        ind.fitness.normalisedValue.append(ind.fitness.wvalues[i] / maxValues[i])
                    else:
                        ind.fitness.normalisedValue.append(ind.fitness.wvalues[i])

        chosen = []
        for i in xrange(0, k, 4):
            chosen.append(tourn(individuals_1[i], individuals_1[i + 1]))
            chosen.append(tourn(individuals_1[i + 2], individuals_1[i + 3]))
            chosen.append(tourn(individuals_2[i], individuals_2[i + 1]))
            chosen.append(tourn(individuals_2[i + 2], individuals_2[i + 3]))

        return chosen


#######################################
# Generalized Reduced runtime ND sort #
#######################################

def identity(obj):
    """Returns directly the argument *obj*.
    """
    return obj

def isDominatedCdom(wvalues1, wvalues2):
    """Returns whether or not *wvalues1* dominates *wvalues2*.
    
    :param wvalues1: The weighted fitness values that would be dominated.
    :param wvalues2: The weighted fitness values of the dominant.
    :returns: :obj:`True` if wvalues2 dominates wvalues1, :obj:`False`
              otherwise. Dominates = Continuous Dominates
    """
    def expLoss(x1, y1, n):
       return -1*math.e**( (x1 - y1) / n )

    def loss(x, y):
        losses = []
        n = len(x)
        for self_wvalue, other_wvalue in zip(x, y):
            losses += [expLoss( self_wvalue, other_wvalue, n)]
        return sum(losses) / n

    l1 = loss(wvalues1, wvalues2)
    l2 = loss(wvalues2, wvalues1)
    
    return l1 < l2

def median(seq, key=identity):
    """Returns the median of *seq* - the numeric value separating the higher 
    half of a sample from the lower half. If there is an even number of 
    elements in *seq*, it returns the mean of the two middle values.
    """
    sseq = sorted(seq, key=key)
    length = len(seq)
    if length % 2 == 1:
        return key(sseq[(length - 1) // 2])
    else:
        return (key(sseq[(length - 1) // 2]) + key(sseq[length // 2])) / 2.0

def sortLogNondominated(individuals, k, first_front_only=False):
    """Sort *individuals* in pareto non-dominated fronts using the Generalized
    Reduced Run-Time Complexity Non-Dominated Sorting Algorithm presented by
    Fortin et al. (2013).
    
    :param individuals: A list of individuals to select from.
    :returns: A list of Pareto fronts (lists), with the first list being the
              true Pareto front.
    """
    if k == 0:
        return []
    
    #Separate individuals according to unique fitnesses
    unique_fits = defaultdict(list)
    for i, ind in enumerate(individuals):
        unique_fits[ind.fitness.wvalues].append(ind)
    
    #Launch the sorting algorithm
    obj = len(individuals[0].fitness.wvalues)-1
    fitnesses = unique_fits.keys()
    front = dict.fromkeys(fitnesses, 0)

    # Sort the fitnesses lexicographically.
    fitnesses.sort(reverse=True)
    sortNDHelperA(fitnesses, obj, front)    
    
    #Extract individuals from front list here
    nbfronts = max(front.values())+1
    pareto_fronts = [[] for i in range(nbfronts)]
    for fit in fitnesses:
        index = front[fit]
        pareto_fronts[index].extend(unique_fits[fit])

    # Keep only the fronts required to have k individuals.
    if not first_front_only:
        count = 0
        for i, front in enumerate(pareto_fronts):
            count += len(front)
            if count >= k:
                return pareto_fronts[:i+1]
        return pareto_fronts
    else:
        return pareto_fronts[0]

def sortNDHelperA(fitnesses, obj, front):
    """Create a non-dominated sorting of S on the first M objectives"""
    if len(fitnesses) < 2:
        return
    elif len(fitnesses) == 2:
        # Only two individuals, compare them and adjust front number
        s1, s2 = fitnesses[0], fitnesses[1]
        if isDominatedCdom(s2[:obj+1], s1[:obj+1]):
            front[s2] = max(front[s2], front[s1] + 1)
    elif obj == 1:
        sweepA(fitnesses, front)
    elif len(frozenset(map(itemgetter(obj), fitnesses))) == 1:
        #All individuals for objective M are equal: go to objective M-1
        sortNDHelperA(fitnesses, obj-1, front)
    else:
        # More than two individuals, split list and then apply recursion
        best, worst = splitA(fitnesses, obj)
        sortNDHelperA(best, obj, front)
        sortNDHelperB(best, worst, obj-1, front)
        sortNDHelperA(worst, obj, front)

def splitA(fitnesses, obj):
    """Partition the set of fitnesses in two according to the median of
    the objective index *obj*. The values equal to the median are put in
    the set containing the least elements.
    """
    median_ = median(fitnesses, itemgetter(obj))
    best_a, worst_a = [], []
    best_b, worst_b = [], []

    for fit in fitnesses:
        if fit[obj] > median_:
            best_a.append(fit)
            best_b.append(fit)
        elif fit[obj] < median_:
            worst_a.append(fit)
            worst_b.append(fit)
        else:
            best_a.append(fit)
            worst_b.append(fit)

    balance_a = abs(len(best_a) - len(worst_a))
    balance_b = abs(len(best_b) - len(worst_b))

    if balance_a <= balance_b:
        return best_a, worst_a
    else:
        return best_b, worst_b

def sweepA(fitnesses, front):
    """Update rank number associated to the fitnesses according
    to the first two objectives using a geometric sweep procedure.
    """
    stairs = [-fitnesses[0][1]]
    fstairs = [fitnesses[0]]  
    for fit in fitnesses[1:]:
        idx = bisect.bisect_right(stairs, -fit[1])
        if 0 < idx <= len(stairs):
            fstair = max(fstairs[:idx], key=front.__getitem__)
            front[fit] = max(front[fit], front[fstair]+1)
        for i, fstair in enumerate(fstairs[idx:], idx):
            if front[fstair] == front[fit]:
                del stairs[i]
                del fstairs[i]
                break
        stairs.insert(idx, -fit[1])
        fstairs.insert(idx, fit)

def sortNDHelperB(best, worst, obj, front):
    """Assign front numbers to the solutions in H according to the solutions 
    in L. The solutions in L are assumed to have correct front numbers and the 
    solutions in H are not compared with each other, as this is supposed to 
    happen after sortNDHelperB is called."""
    key = itemgetter(obj)    
    if len(worst) == 0 or len(best) == 0:
        #One of the lists is empty: nothing to do
        return
    elif len(best) == 1 or len(worst) == 1:
        #One of the lists has one individual: compare directly
        for hi in worst:
            for li in best:
                if isDominatedCdom(hi[:obj+1], li[:obj+1]) or hi[:obj+1] == li[:obj+1]:
                    front[hi] = max(front[hi], front[li] + 1)
    elif obj == 1:
        sweepB(best, worst, front)
    elif key(min(best, key=key)) >= key(max(worst, key=key)):
        #All individuals from L dominate H for objective M:
        #Also supports the case where every individuals in L and H 
        #has the same value for the current objective
        #Skip to objective M-1
        sortNDHelperB(best, worst, obj-1, front)
    elif key(max(best, key=key)) >= key(min(worst, key=key)):
        best1, best2, worst1, worst2 = splitB(best, worst, obj)
        sortNDHelperB(best1, worst1, obj, front)
        sortNDHelperB(best1, worst2, obj-1, front)
        sortNDHelperB(best2, worst2, obj, front)

def splitB(best, worst, obj):
    """Split both best individual and worst sets of fitnesses according
    to the median of objective *obj* computed on the set containing the
    most elements. The values equal to the median are attributed so as 
    to balance the four resulting sets as much as possible.
    """
    median_ = median(best if len(best) > len(worst) else worst, itemgetter(obj))
    best1_a, best2_a, best1_b, best2_b = [], [], [], []
    for fit in best:
        if fit[obj] > median_:
            best1_a.append(fit)
            best1_b.append(fit)
        elif fit[obj] < median_:
            best2_a.append(fit)
            best2_b.append(fit)
        else:
            best1_a.append(fit)
            best2_b.append(fit)
    
    worst1_a, worst2_a, worst1_b, worst2_b = [], [], [], []        
    for fit in worst:
        if fit[obj] > median_:
            worst1_a.append(fit)
            worst1_b.append(fit)
        elif fit[obj] < median_:
            worst2_a.append(fit)
            worst2_b.append(fit)
        else:
            worst1_a.append(fit)
            worst2_b.append(fit)
    
    balance_a = abs(len(best1_a) - len(best2_a) + len(worst1_a) - len(worst2_a))
    balance_b = abs(len(best1_b) - len(best2_b) + len(worst1_b) - len(worst2_b))

    if balance_a <= balance_b:
        return best1_a, best2_a, worst1_a, worst2_a
    else:
        return best1_b, best2_b, worst1_b, worst2_b

def sweepB(best, worst, front):
    """Adjust the rank number of the worst fitnesses according to
    the best fitnesses on the first two objectives using a sweep
    procedure.
    """
    stairs, fstairs = [], []
    iter_best = iter(best)
    next_best = next(iter_best, False)
    for h in worst:
        while next_best and h[:2] <= next_best[:2]:
            insert = True
            for i, fstair in enumerate(fstairs):
                if front[fstair] == front[next_best]:
                    if fstair[1] > next_best[1]:
                        insert = False
                    else:
                        del stairs[i], fstairs[i]
                    break
            if insert:
                idx = bisect.bisect_right(stairs, -next_best[1])
                stairs.insert(idx, -next_best[1])
                fstairs.insert(idx, next_best)
            next_best = next(iter_best, False)

        idx = bisect.bisect_right(stairs, -h[1])
        if 0 < idx <= len(stairs):
            fstair = max(fstairs[:idx], key=front.__getitem__)
            front[h] = max(front[h], front[fstair]+1)

__all__ = ['selNSGA2Cdom', 'sortNondominated', 'sortLogNondominated', 'selTournamentDCDCdom', ]