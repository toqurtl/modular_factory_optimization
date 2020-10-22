from moga.chromosome import BinaryChromosome
from moga.generic import BinaryLocalAlgorithm
from moga.generation import MultiObjectiveGenerator, MultiObjGenericEnum
from module_factory.optimization.optimizer import Optimizer
from module_factory.component.production_line import ProductionLine
from module_factory.optimization import utils
from module_factory.optimization.analysis import MultiObjectiveAnalyzer, MultiObjectiveAnalysis
import numpy as np


# set BinaryChromosome from production line file
production_line = ProductionLine('sample_data/production_line_200903.csv')
cycle_time_min = 60
cycle_time_max = 90
cycle_dict = {0: 30, 1:60, 2: 90}
# production_line.set_cycle_dict_with_min_max(cycle_time_min, cycle_time_max)
production_line.set_cycle_dict(cycle_dict)
geno_shape = utils.production_line_to_geno_shape(production_line)

BinaryChromosome.set_geno_shape(**geno_shape)


# set fitness check function
def factory_build_check(chromosome, new_generation):
    pheno_type = BinaryChromosome.get_phenotype(chromosome)
    buildable, factory = utils.create_factory_from_pheno_type(pheno_type, production_line, False)
    return buildable


def factory_build_check_2(chromosome, new_generation):
    check = True
    pheno_type = BinaryChromosome.get_phenotype(chromosome)
    cycle_time_idx = pheno_type['cycle_time']
    if cycle_time_idx >= len(production_line.cycle_dict):
        return False
    buildable, factory = utils.create_factory_from_pheno_type(pheno_type, production_line, False)
    if not buildable:
        return buildable
    for chromosome_info in new_generation:
        chro_2 = chromosome_info[0]
        pheno_type_2 = BinaryChromosome.get_phenotype(chro_2)
        buildable, factory_2 = utils.create_factory_from_pheno_type(pheno_type_2, production_line, False)
        if factory == factory_2:
            check = False
            break
    return check


# BinaryChromosome.fitted_in_geno_func_list.append(factory_build_check)
BinaryChromosome.fitted_in_geno_func_list.append(factory_build_check_2)

# optimization configuration
optimizer_parameter_dict = {
    'num_chromosome_in_generation': 20,
    'max_generation': 5,
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
optimizer.set_local_algorithm(BinaryLocalAlgorithm.NONE)

# optimization
optimizer.optimize()


# result analysis
generation_list = optimizer.get_generation_dict()
first_fronts = MultiObjectiveAnalyzer.first_fronts_from_generations(generation_list)
for front in first_fronts:
    print(front)

moa = MultiObjectiveAnalysis(optimizer=optimizer, folder_path='experiment')
moa.save_all_generation_as_file('test.ge')


# check = optimizer.get_generation_dict()
# for num, generation, time in check.values():
#     print(num, time)




