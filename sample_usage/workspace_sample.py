from moga.optimizer import ParetoOptimizer
from moga.chromosome import BinaryChromosome
from moga.generic import BinaryLocalAlgorithm
from moga.generation import MultiObjectiveGenerator, MultiObjGenericEnum
from moga.generation import Fronting
from module_factory.optimization.optimizer import Optimizer
from module_factory.component.production_line import ProductionLine
from module_factory.optimization import utils
from module_factory.optimization.analysis import MultiObjectiveAnalyzer
import numpy as np


# set BinaryChromosome from production line file
production_line = ProductionLine('sample_data/production_line_200903.csv')
geno_shape = utils.production_line_to_geno_shape(production_line)
BinaryChromosome.set_geno_shape(**geno_shape)


# set fitness check function
def factory_build_check(chromosome):
    pheno_type = BinaryChromosome.get_phenotype(chromosome)
    buildable, factory = utils.create_factory_from_pheno_type(pheno_type, production_line, False)
    return buildable


BinaryChromosome.fitted_in_geno_func_list.append(factory_build_check)

# optimization configuration
optimizer_parameter_dict = {
    'num_chromosome_in_generation': 100,
    'max_generation': 1000,
    'num_objective': 2,
}

generic_parameter_dict = {
    MultiObjGenericEnum.SUPERIOR: 0.2,
    MultiObjGenericEnum.ONE_POINT_CROSSOVER: 0.4,
    MultiObjGenericEnum.LOCAL_MUTATION: 0.2,
    MultiObjGenericEnum.GLOBAL_MUTATION: 0.2
}

simulation_time = 10000


# set objective function
def objective_functions(chro_str):
    pheno_type = BinaryChromosome.get_phenotype(chro_str)
    buildable, factory = utils.create_factory_from_pheno_type(pheno_type, production_line, False)
    factory.simulate(simulation_time)
    labor = factory.num_labor
    num_unit = factory.num_unit
    return np.array([-labor, num_unit])

# adjust configuration
optimizer = Optimizer()
optimizer.setting(
    objective_functions=objective_functions,
    generic_parameter_dict=generic_parameter_dict,
    optimizer_parameter_dict=optimizer_parameter_dict
)

# optimization
optimizer.optimize()

# result analysis
generation_list = optimizer.generation_list
first_fronts = MultiObjectiveAnalyzer.first_fronts_from_generations(generation_list, interval=10)
for front in first_fronts:
    print(front)
# check = optimizer.get_generation_dict()
# for num, generation, time in check.values():
#     print(num, time)




