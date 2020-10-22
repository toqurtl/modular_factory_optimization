from moga.chromosome import BinaryChromosome
from module_factory.optimization import utils
import math


def get_digit(min_value, max_value):
    idx, num_value = 1, max_value - min_value + 1
    while True:
        if num_value <= math.pow(2, idx):
            break
        idx += 1
    return idx


def cycle_time_from_pheno_type(pheno_type: type(dict)):
    return pheno_type['cycle_time']


def cycle_time_idx_from_pheno_type(pheno_type: type(dict)):
    return pheno_type['cycle_time']


def labor_num_list_from_pheno_type(pheno_type: type(dict)):
    labor_num_list = []
    for key, value in pheno_type.items():
        if key != 'cycle_time':
            labor_num_list.append(value[0])
    return labor_num_list


def create_factory_from_pheno_type_2(pheno_type: type(dict), production_line, initialize=False):
    cycle_time = cycle_time_from_pheno_type(pheno_type)[0]
    labor_num_list = labor_num_list_from_pheno_type(pheno_type)
    buildable, factory = production_line.create_factory(cycle_time=cycle_time, labor_num_list=labor_num_list, initialize=initialize)
    return buildable, factory


def create_factory_from_pheno_type(pheno_type: type(dict), production_line, initialize=False):
    cycle_time_idx = cycle_time_from_pheno_type(pheno_type)[0]
    print(cycle_time_idx, len(production_line.cycle_dict))
    cycle_time = production_line.cycle_dict[cycle_time_idx]
    labor_num_list = labor_num_list_from_pheno_type(pheno_type)
    buildable, factory = production_line.create_factory(cycle_time=cycle_time, labor_num_list=labor_num_list, initialize=initialize)
    return buildable, factory


def create_factory_from_chromosome(chromosome, production_line, initialize=False):
    pheno_type = BinaryChromosome.get_phenotype(chromosome)
    buildable, factory = utils.create_factory_from_pheno_type(pheno_type, production_line, initialize=initialize)
    return buildable, factory


def production_line_to_geno_shape(production_line):
    geno_shape = {}
    # cycle_content = {
    #     'num': 1,
    #     'min': production_line.min_cycle,
    #     'max': production_line.max_cycle,
    #     'digit': 8,
    #     'offspring': -32
    # }
    cycle_content = {
        'num': 1,
        'min': 0,
        'max': len(production_line.cycle_dict),
        'digit': get_digit(0, len(production_line.cycle_dict)),
        'offspring': 0
    }

    geno_shape['cycle_time'] = cycle_content
    for activity in production_line:
        activity_content = {'num': 1,
                            'min': activity.min_labor,
                            'max': activity.max_labor,
                            'digit': 2,
                            'offspring': -1
                            }
        geno_shape[str(activity.id)] = activity_content
    return geno_shape
