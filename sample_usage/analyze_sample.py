from moga.chromosome import BinaryChromosome
from module_factory.optimization.analysis import MultiObjectiveAnalyzer
from module_factory.component.production_line import ProductionLine
from module_factory.optimization import utils
from pandas import ExcelWriter, DataFrame
import pickle


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


with open('experiment/test.ge', 'rb') as f:
    generation_dict = pickle.load(f)


## evolution process to fig
# MultiObjectiveAnalyzer.save_generation_info_to_excel(generation_dict, 'test_1.xlsx')
# MultiObjectiveAnalyzer.save_evolution_process_to_fig(generation_dict, 'test.png')

## compare process to fig
# a, b, c = generation_dict[1]
# d, e, f = generation_dict[2]
# chromosome_list_with_set_name = []
# chromosome_list_with_set_name.append(('a', b))
# chromosome_list_with_set_name.append(('b', e))
#
# test = MultiObjectiveAnalyzer.chromosome_list_to_fig_format(chromosome_list_with_set_name, 2)
# MultiObjectiveAnalyzer.to_figure('test_2.png', test, [-1,1])

## create_factory and save
# a, generation, b = generation_dict[1]
# chromosome = generation[0][0]
# MultiObjectiveAnalyzer.save_factory_information_to_excel(chromosome, production_line, 'taa.xlsx')

