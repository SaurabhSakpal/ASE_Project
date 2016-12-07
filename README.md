# ASE_Project
## This is software product line optimization project
### Steps to run this code 
1. **Place your model file**  
All models present are taken form SPLOT. Make sure your model XML file is present in the folder  
``` <path_to_repo>/models/ ```  
Make sure model name does not contain any '_' character.
2. **Run optimizers**  
Run all optimizers (GA, NSGA2, SPEA2, NSGA2Cdom)against your model using command  
``` Usage: python testOptimizers <model_file> <run_id> <pop_size> <num_gen> <mutation_rate> ```    
  * model_file : Path to the XML model file
  * run_id : Any integer. To be used as an identifier for storing outputs corresponding to this run against your model
  * pop_size : Size of the population to be maintained by the optimizers
  * num_gen : Number of generations for which all optimizers will run
  * mutation_rate : Probability of how often the mutation will occur  
The output of the run will be stored on the below path  
``` <path_to_repo>/output_<modelname>/<run_id>/Pareto_Fronts/<optimizer_name>_<model_name> ```  
This corresponds to the normalized pareto fronts gnerated by each optimizer
3. **Generate True Pareto Fronts**    
To obtain true pareto frontiers for evaluation on performance measures like Spread and IGD run the following command  
``` python generate_normalized_true_pf.py <path_to_output_folder>```  
  * path_to_output_folder : This is path to the folder output_<modelname> generated in step 2  
4. **Calculate performace metric**  
Calculate Hypervolume, Spread, IGD using following commands  
``` cd <path_to_repo>/Performance/```  
```python ./HyperVolume/hypervolume_runner <path_to_output_folder>```  
```python ./Spread/spread_runner <path_to_output_folder>```  
```python ./Igd/igd_runner <path_to_output_folder> ```     
Output will be generate as  
``` <path_to_repo>/stats/<performance_measure>_<model_name> ```    
  * performance_measure : hv, spread or igd 
5. **Analyze performance**  
Each file generate above will have metric for all optimizers on the performance metric across different runs. These files canbe given as input to the stats.py for analysis.  
```cat spread_database | python stats.py```  




