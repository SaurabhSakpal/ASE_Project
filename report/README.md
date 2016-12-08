# Software Product Line Optimization 
## 1. Overview

A software product line is a set of software-intensive systems that share a common, managed set of features satisfying the specific needs of a particular market segment or mission and that are developed from a common set of core assets in a prescribed way [1]. They are emerging as an important development paradigm because they help companies in modelling their solutions and offerings. It provides a structured way to quantify market, cost, productivity, quality, and other business drivers. A fundamental problem in software product line engineering is that a product line of industrial size can easily incorporate several thousand variable features. Such variability leads to heterogeneous goals and contradicting requirements. This motivated us to use the optimization techniques studied in CSC 591 Automated Software Engineering for finding sound and optimum configurations of very large variability models.
sadsad

## 2. Background

Many results in the automated analysis of software product lines were validated using feature models published in online feature model repositories such as SPLOT [2]. Some of these works are Sayyad et al. [3] [4], Pohl et al. [5], Lopez-Herrejon and Egyed [6], Johansen et al. [7], Mendonca et al. [8].  Most of the feature models in SPLOT were produced for academic purposes without representing actual systems. SPLOT models are small and less constrained with lower branching factors, but they also have higher ratios of feature groups and deep leaves [9]. This is how they differ from the actual software product lines in the industry. But nonetheless, they have been significant academically to analyze and compare optimization techniques. 
In this project we have done a 5-objective optimization of Software Product Line using different optimizers on three different models of varied size (mentioned in 3.1). There are five conflicting objectives further explained in section 3.1. Optimizers used and compared in this work include a naive Genetic Algorithm (GA) with random select operator, Nondominated Sorting Genetic Algorithm-II (NSGA-II) [10], Strength Pareto Evolutionary Algorithm SPEA2 [12], and a variation of NSGA2 using continuous domination (CDOM) instead of binary domination (BDOM). Three different performance measure Hypervolume, Spread and Inter Generational Distance (IGD) are used to analyze the performance of these optimizers on the three models. 

## 3. Implementation
The workflow of this project is illustrated in Fig 1. The model consist of an XML file obtained from SPLOT. The file is parsed to obtain a feature tree in Python. The parsed tree is traversed from top to bottom to generate a point.  A point is an instance of the population. Several points meeting the model constraints are generated to make up Generation 0 population that is an input to the optimizers. Optimizers run until the specified generations and give a set of points that are meta heuristically best satisfy the given objectives. This set of solution is pareto optimal and hence called the pareto frontier. These pareto frontiers are then analyzed on Hypervolume, Spread and IGD to rank the optimizers.

<img src="https://raw.githubusercontent.com/SaurabhSakpal/fss16SmallThinExpert/master/project/data/ASE%20Architecture%20Diagram.png" width="800" height="300"> 

### 3.1 Models
A feature is an end-user-visible behavior of a software product that is of interest to some stakeholder. A feature model represents the information of all possible products of a software product line in terms of features and relationships among them. A feature model is represented as a hierarchically arranged set of features composed by: (1) Relationships between a parent feature and its child features (or subfeatures). (2) Cross-tree constraints that are typically inclusion or exclusion statements. All constraints are represented as CNF clauses. An example of a SPLOT model XML is given below:

<img src="https://github.com/SaurabhSakpal/fss16SmallThinExpert/blob/master/project/data/SplotParserXMLCode.png" width="500" height="500">   

The summary of the three models used is given below:

| Model        | Number of Features           | Number of Cross Tree Constraints  |
| ------------- |:-------------:| :-----:|
| Home Automation     | 48 | 5 |
| Computadores      | 45      |   9 |
| Database Tools | 70      |    2 |


#### 3.1.1 Decisions
For a feature model, decisions are the various features in the model. All decisions are boolean, indicating whether a feature is selected or not. 
#### 3.1.2 Objectives
This project attempts multi objective optimization. For each model we have five conflicting objectives, as summarized below. Some of the objectives have been taken from this prior work [4].


| Objective        | Maximize/ Minimize           | Description  |
| ------------- |:-------------:| :-----|
| Cost     | Minimize |Each feature is associated with a cost to company. Cost of a product is sum of cost of all features it has. |
| Feature Richness      | Maximize      |   Number of features in the model |
| Violations      | Minimize      |   Number of cross tree constraints violated by the product.* |
| Benefits   | Maximize      |    Each feature has a benefit value, indicating how profitable it is for the company. Sum of all feature benefits in the product is the objective. |
| Defects   | Minimize      |    Each feature has a defect value, indicating how often this feature shows a defect. Sum of all feature defects in the product is the objective. |

*we generate products with 0 violations at the start, mutations introduced in our optimizers introduce minors violations in the later generations. 


### 3.2 Parser
The SPLOT models are in form of an XML as shown below. We wrote a parser to convert XML models into a tree. Extracting out the explicitly stated cross tree constraints and also the implicit tree structure constraint. 
Example of a feature model:
</p align="center">
![alt text](https://github.com/SaurabhSakpal/fss16SmallThinExpert/blob/master/project/data/image2.jpg)
</p>
### 3.3 SAT Solver
Though we have minimum constraint violations as one of our objectives. On Dr. Menzie’s suggestion we realized, we can SAT solve our generation 0 for all Optimizers (all optimizers we have are GA variations). This will give us 100% valid solutions right in the beginning. But still as the population evolves, mutations are introduced and we get some violations in cross tree constraints (tree structure constraints are not violated as our mutate operator takes care of that). Hence variance for this objective is very low (almost nil). All objectives are given equal weight. This means a single violation will greatly penalize the point fitness. This is desirable as we aim to achieve solutions with zero violations (not just minimum).

### 3.4 Optimisers
Genetic Algorithms have been one of the most common evolutionary algorithms in use for optimization. We have used following variants of Genetic Algorithms for the comparison. Each of them differ in just there select operator which decides what all points (equal to population size, k) will survive till the next generation. 

**Naive Genetic Algorithms:** Random points k are picked and taken over to the next generation. 

**NSGA2:** A primary ranking method (like BDOM) based on number of points that dominate a point is used to generate frontiers then a secondary sorting method is used for non-dominating sorting. This is mostly done with a motive of crowd pruning to preserve the diversity. Details can be studied in this work by Deb et al [10].

**SPEA2:** Unlike NSGA2, all individuals are scored by the number of other people they dominate. Two data structures population and archive are maintained. Population is a space for current mutants while archive is a space for good ideas. Population is built partially from archive. Details can be studied in this work by zitzler et al [11].

**NSGA2Cdom:** In a multiple objective problem binary domination is not the best way to go. As seen in work by Sayyad et al [3], continuous domination performs better for multi objective optimizations. This optimizer is a variant of NSGA2 with domination function replaced by CDOM. Now we can compare on how much a point is better or worse than the other.  

We have used DEAP library [12] for our implementation of these algorithms. We had to provide our own our own cross-over and mutate operators and also a select operator for NSGA2Cdom. A point is represented as a feature tree with boolean values for each node. The cross-over and mutate operator works as shown below. 

**Mutate :** To mutate each node is decided to be changed or not by flipping a coin biased as the mutation probability. If we decide not to mutate the node remains same, but if decide to mutate the whole subtree is generated again (highlighted in blue) following the tree structure constraints (not necessarily cross tree constraint).

**Cross-over :** For each node in a group a fair coin is tossed to select if the node would be taken from mom or dad. The whole subtree from that node is copied exactly into the child.

### 3.5 Performance Measures
Following performance measures were used to evaluate optimizers against each other

**Hypervolume (maximize):** The volume inside the pareto frontier is called hypervolume. The more the hypervolume the better it is, since then we have more number of feasible solution for the problem at hand.

**Spread (maximize):** This measure calculates how well the points are spread out on the pareto frontier. More spread indicates diversity of solutions and hence it is desired. The measure was introduced by Deb et al [13]. And is calculated as illustrated below

**Inter Generational Distance (Minimize) :** IGD measure compares, how good is a given pareto frontier according to the best known.The best known frontier is known as true pareto frontier. True pareto frontier is calculated by combining points obtained from all optimisers and selecting best of the lot. We have used CDOM again in this comparison to generate true pareto frontiers. The less the distance from the true pareto frontier, the better the optimizer is.  

## 4. Source Code
The source code for this project with the detailed instructions to run it can be found [here](https://github.com/SaurabhSakpal/ASE_Project).
## 5. Results
* HyperVolume - HomeAutomation  
nsga2 performs best, while hypervolume is minimum for msga2cdom
```

rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,    nsga2Cdom ,    2   ,    1 ( ---  *-       |              ), 1.39,  1.83,  2.14,  2.24,  2.50
   2 ,           ga ,    3   ,    1 (           -- *| ---          ), 3.13,  3.53,  3.70,  4.21,  4.84
   3 ,        spea2 ,    4   ,    1 (               |    *--       ), 3.94,  4.13,  4.69,  5.00,  5.34
   4 ,        nsga2 ,    5   ,    0 (               |       - *--  ), 5.37,  5.60,  5.76,  5.95,  6.27

```
* Spread - HomeAutomation  
Spread is maximum for nsga2cdom, ga and spea2 are ranked similar while nsga2 is the worst performer
```

rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,        nsga2 ,    0   ,    0 (-  *-          |              ), 0.43,  0.46,  0.48,  0.51,  0.54
   2 ,        spea2 ,    0   ,    0 (    *-         |              ), 0.46,  0.48,  0.51,  0.55,  0.56
   2 ,           ga ,    0   ,    0 (  - *-         |              ), 0.47,  0.49,  0.52,  0.53,  0.58
   3 ,    nsga2Cdom ,    0   ,    0 (    -- *-      |              ), 0.52,  0.57,  0.59,  0.60,  0.66

```
* IGD - HomeAutomation
nsga2Cdom performs the best with minimum IGD, followed by nsga2. While spea2 is even worse than a naive GA.
```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,    nsga2Cdom ,    0   ,    0 ( *-            |              ), 0.00,  0.01,  0.02,  0.02,  0.04
   2 ,        nsga2 ,    0   ,    0 (     - *       |              ), 0.05,  0.06,  0.07,  0.07,  0.08
   3 ,           ga ,    0   ,    0 (          -  * |----          ), 0.10,  0.11,  0.12,  0.16,  0.19
   4 ,        spea2 ,    0   ,    0 (             --|  * ----      ), 0.13,  0.16,  0.17,  0.20,  0.23

```
* Hypervolume - DatabaseTools  
The ranking is exactly same as that in homeautomation. nsga2cdom performs worst and nsga2 is best
```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,    nsga2Cdom ,    2   ,    1 ( --  *--       |              ), 1.33,  1.67,  2.03,  2.18,  2.50
   2 ,           ga ,    3   ,    0 (           - *-|---           ), 3.09,  3.40,  3.58,  3.70,  4.51
   3 ,        spea2 ,    4   ,    1 (             --|    *--       ), 3.52,  4.13,  4.69,  5.00,  5.29
   4 ,        nsga2 ,    5   ,    0 (               |       - *--  ), 5.32,  5.55,  5.79,  5.96,  6.27

```
* Spread - DatabaseTools
nsga2Cdom again performs worst for spread, while ga and nsga2 perform best and ar ealmost equal.
```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,    nsga2Cdom ,    0   ,    0 ( -- *--        |              ), 0.49,  0.52,  0.54,  0.56,  0.59
   2 ,        spea2 ,    0   ,    0 (    ---    *  -|----          ), 0.54,  0.60,  0.67,  0.73,  0.84
   3 ,           ga ,    0   ,    0 (            ---| *  -----     ), 0.70,  0.76,  0.79,  0.84,  0.94
   3 ,        nsga2 ,    0   ,    0 (               |-   *---      ), 0.76,  0.80,  0.85,  0.86,  0.92

```
* IGD - DatabaseTools
Surprisingly all optimizers are ranked equal. But as seen in the distribution nsga2cdom has more values in the lower ranges, so it again outperforms others (though slightly this time).
```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,    nsga2Cdom ,    0   ,    0 (---- *  -------|              ), 0.02,  0.04,  0.05,  0.06,  0.11
   1 ,        nsga2 ,    0   ,    0 (  -- * -       |              ), 0.03,  0.04,  0.05,  0.06,  0.06
   1 ,           ga ,    0   ,    0 (    -- * --    |              ), 0.04,  0.05,  0.06,  0.07,  0.08
   1 ,        spea2 ,    0   ,    0 (     -- * ---  |              ), 0.04,  0.06,  0.06,  0.07,  0.09

```
* Hypervolume - Computadores
The trend in Hypervolume repeats again as seen in previous models
```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,    nsga2Cdom ,    1   ,    0 (-- *--         |              ), 1.07,  1.35,  1.56,  1.75,  2.08
   2 ,           ga ,    2   ,    1 (    - *--      |              ), 1.67,  1.84,  2.01,  2.19,  2.45
   3 ,        spea2 ,    2   ,    0 (   ---- * -    |              ), 1.57,  2.13,  2.35,  2.55,  2.76
   4 ,        nsga2 ,    4   ,    0 (               |   - * -----  ), 3.89,  4.03,  4.23,  4.56,  5.24

```
* spread - Computadores
For this model spea2 and nsga2csom perform equally good. 
```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,        nsga2 ,    0   ,    0 (  -* --        |              ), 0.47,  0.49,  0.51,  0.54,  0.56
   2 ,           ga ,    0   ,    0 (          -  *-|              ), 0.62,  0.65,  0.69,  0.71,  0.73
   3 ,    nsga2Cdom ,    0   ,    0 (        -------| *      ----- ), 0.59,  0.72,  0.76,  0.89,  0.98
   3 ,        spea2 ,    0   ,    0 (               |---   * ----  ), 0.72,  0.80,  0.84,  0.88,  0.95

```
* IGD - Computadores
For a change nsga2 takes over nsga2Cdom in providing the minimum IGD. But ga and spea2 continue to be the worst performer. 
```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,        nsga2 ,    0   ,    0 ( *-            |              ), 0.03,  0.03,  0.04,  0.04,  0.05
   2 ,    nsga2Cdom ,    0   ,    0 (    - *  -     |              ), 0.06,  0.07,  0.08,  0.10,  0.12
   3 ,           ga ,    0   ,    0 (         ---* -|--            ), 0.11,  0.13,  0.13,  0.15,  0.18
   4 ,        spea2 ,    0   ,    0 (            ---| *  ----      ), 0.13,  0.16,  0.17,  0.20,  0.23

```
**Comparison of HV,Spread,IGD on three models**  
<img src="https://raw.githubusercontent.com/SaurabhSakpal/fss16SmallThinExpert/master/project/data/chart_ha.png" width="500" height="250">  

<img src="https://raw.githubusercontent.com/SaurabhSakpal/fss16SmallThinExpert/master/project/data/chart_db.png" width="500" height="250">  

<img src="https://raw.githubusercontent.com/SaurabhSakpal/fss16SmallThinExpert/master/project/data/chart_ca.png" width="500" height="250">  

## 6. Inference
We have provided inference based on the graphs in the previous section. 

For the following observations:
- Nsga2Cdom consistently performs better in IGD comparison, there is only one instance when it loses to NSGA2. 
- For spread, nsga2Cdom performs best for homeAutomation and Computadores while it loses to others in DatabaseTools. 
- Nsga2Cdom performs consitently worse when it comes to hypervolume.

Inference:
- As the number of objectives increase it becomes difficult for BDOM to say a point dominates others because for that the point has to be equal or better across all the objectives. Here we see that CDOM has an edge because it takes into account scenario if a point is considerably better on many objectives but slightly worse on few. The discrete nature of BDOM degrades it's performance over CDOM and hence we see considerable improvement in mostly all parameters with CDOM.

- As for the values of Spread, we accredit the values to crowd-pruning. We get better spread when crowd pruning is performed. 

- Hypervolume is good if we have more number of solutions closer to utopia. It might not be good for the cases were we have some point which performs really well on some objectives, but it is an average player ont he other fronts. CDOM has an advantage of selecting such points comapred to the all round average performers. This is the reason we consistenetly get low hypervolumes with Nsga2Cdom.

**We observed that BDOM is transitive(A dominates B and B dominates C means A dominates C) whereas CDOM is non transitive. It is quite straightforward to imagine why BDOM is transitive. But, we can easily find pairs of points where none of the points dominate each other in which case, we cannot consider them further and that's when Cdom takes over.
Cdom is not necessarily transitive. A dominates B and B dominates C doesn't necessarily mean A dominates C. This happens in the case of points where, there is no Binary Domination present. 
**

## 7. Conclusion
Though performance of an optimizer depends a lot on the model. Some optimizers are good at discovering the solutions which are average performer on all fronts (objectives), while others like Nsga2Cdom also discover the points which approach utopia not flying in the midway but from the corners. These solutions might be really really good on few objectives, but are just average or may also be poor than the others on the other fronts. Ultimately the question to decide is what kind of solutions does your client seek for. Afterall its the money that matters. 
## 8. References
[1] [Software Engineering Institute] (http://www.sei.cmu.edu/productlines/) , Carnegie Mellon University 

[2] Marcilio Mendonca, Moises Branco, Donald Cowan. 2009. S.P.L.O.T. - Software Product Lines Online Tools  

[3] Abdel Salam Sayyad, Joseph Ingram, Tim Menzies, Hany Ammar. 2013. Scalable Product Line Configuration: A Straw to Break the Camel’s Back  

[4]  Abdel Salam Sayyad, Tim Menzies, Hany Ammar. 2013. On the Value of User Preferences in Search-Based Software Engineering: A Case Study in Software Product Lines  

[5] Richard Pohl, Kim Lauenroth, Klaus Pohl. 2011. A Performance Comparison of Contemporary Algorithmic Approaches for Automated Analysis Operations on Feature Models  

[6]Roberto E. Lopez-Herrejon, Alexander Egyed. 2011. Searching the Variability Space to Fix Model Inconsistencies: A Preliminary Assessment  

[7] Martin Fagereng Johansen, Øystein Haugen, Franck Fleurey. 2011. Properties of Realistic Feature Models Make Combinatorial Testing of Product Lines Feasible  

[8] Marcilio Mendonca , Andrzej Wasowski , Krzysztof Czarnecki, Donald Cowan. 2008. Efficient Compilation Techniques for Large Scale Feature Models  

[9] Thorsten Berger, Steven She, Rafael Lotufo, Andrzej W ˛asowski, Krzysztof Czarnecki. 2013. Variability Modeling in the Systems Software Domain  

[10] Kalyanmoy Deb, Amrit Pratap, Sameer Agarwal, T. Meyarivan. 2002. A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II  

[11] Eckart Zitzler, Marco Laumanns, and Lothar Thiele. 2001. SPEA2: Improving the Strength Pareto Evolutionary Algorithm 
[12] Distributed Evolutionary Algorithms in Python (DEAP)  

[13] 2001. Deb, K.: Multi-Objective Optimization using Evolutionary Algorithms. John Wiley and Sons, Chichester  









