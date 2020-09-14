from module_factory.component.production_line import ProductionLine
from module_factory.optimization import utils
from moga.generation import Fronting
from moga.chromosome import BinaryChromosome
from copy import deepcopy
from pandas import DataFrame, ExcelWriter
from matplotlib import pyplot as plt
import os
import pickle


class MultiObjectiveAnalyzer(object):

    basic_save_info_row = ['generation', 'time', 'chromosome']

    # function for basic value
    @staticmethod
    def chromosome_to_factory(chromosome, production_line, initialize):
        return utils.create_factory_from_chromosome(chromosome, production_line, initialize=initialize)

    @staticmethod
    def get_objective_column(num_objectives=2):
        columns= []
        for i in range(1, num_objectives + 1):
            columns.append('objective'+str(i))
        return columns

    @staticmethod
    def get_num_objective(generation_info):
        num, generation, time = generation_info
        return len(generation[1])

    @staticmethod
    def chromosome_result_to_pandas(chromosome_list, num_objective):
        result_row = []
        for chromosome, objectives in chromosome_list:
            result_row.append(objectives)
        return DataFrame(data=result_row, columns=MultiObjectiveAnalyzer.get_objective_column(num_objective))

    # front data from generation
    @staticmethod
    def front_list_from_generation(generation):
        Fronting.fronting(generation)
        front_list = Fronting.front_list
        return front_list

    @staticmethod
    def nth_front_from_generation(generation, idx):
        Fronting.fronting(generation)
        front_list = Fronting.front_list
        return front_list[idx]

    @staticmethod
    def first_fronts_from_generations(generation_dict, interval=1):
        first_front_list = []
        for num, generation, time in generation_dict.values():
            if num % interval == 0:
                first_front = MultiObjectiveAnalyzer.nth_front_from_generation(generation, 0)
                first_front_list.append((num, first_front))
        return first_front_list

    # saving total evolution result

    @staticmethod
    def save_evolution_process_to_fig(generation_dict, file_path, interval=1, milestone=0):
        first_front_list = MultiObjectiveAnalyzer.first_fronts_from_generations(generation_dict, interval=interval)
        num_objective = MultiObjectiveAnalyzer.get_num_objective(generation_dict[1])
        figure_front_list = MultiObjectiveAnalyzer.chromosome_list_to_fig_format(first_front_list, num_objective)
        MultiObjectiveAnalyzer.to_figure(file_path, figure_front_list, [-1, 1])

    @staticmethod
    def save_generation_info_to_excel(generation_dict, production_line, file_path, intialize=False):
        num_objective = MultiObjectiveAnalyzer.get_num_objective(generation_dict[1])
        row_list = []
        for num, generation, time in generation_dict.values():
            for chromosome_info in generation:
                chro_list = []
                chro_list.extend([num, time, chromosome_info[0]])
                for idx in range(0, num_objective):
                    chro_list.append(chromosome_info[1][idx])
                pheno_info = BinaryChromosome.get_phenotye(chromosome_info[0])
                cycle_time = utils.cycle_time_from_pheno_type(pheno_info)
                chro_list.append(cycle_time)
                row_list.append(chro_list)
        save_info_row = deepcopy(MultiObjectiveAnalyzer.basic_save_info_row)
        for idx in range(0, num_objective):
            save_info_row.append('objectvie' + str(idx + 1))
        save_info_row.append('cycle_time')
        df = DataFrame(row_list, columns=save_info_row)

        with ExcelWriter(file_path, engine='xlsxwriter') as writer:
            df.to_excel(
                excel_writer=writer, sheet_name='result', header=True, index=False
            )
        return

    @staticmethod
    def save_generation_dict_as_file(generation_dict, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(generation_dict, f, pickle.HIGHEST_PROTOCOL)

    # detail analysis
    @staticmethod
    def save_factory_information_to_excel(chromosome, production_line, file_path, initialize=False):
        buildable, factory = utils.create_factory_from_chromosome(chromosome, production_line, initialize=initialize)
        factory.save(file_path)
        return buildable

    @staticmethod
    def chromosome_list_to_fig_format(chromosome_list_with_set_name, num_objective):
        transferred_list = []
        for name, chromosome_set in chromosome_list_with_set_name:
            df = MultiObjectiveAnalyzer.chromosome_result_to_pandas(chromosome_set, num_objective=num_objective)
            transferred_list.append((name, df))
        return transferred_list

    @staticmethod
    def to_figure(file_path, chromosome_set_list, sign_list):
        fig, ax = plt.subplots()
        for name, chromosome_set in chromosome_set_list:
            ax.scatter(
                sign_list[0] * chromosome_set.objective1,
                sign_list[1] * chromosome_set.objective2,
                alpha=0.5,
                label=name,
                s=10
            )
        ax.legend(fontsize=8, loc='upper left')
        plt.title('ScatterPlot of all chromosomes in the generation', fontsize=10)
        plt.xlabel('objective1')
        plt.ylabel('objective2')
        plt.savefig(file_path)
        return


class MultiObjectiveAnalysis(object):
    def __init__(self, optimizer, folder_path='.'):
        self.optimizer = optimizer
        self.folder_path = os.path.abspath(folder_path)

    @property
    def generation_list(self):
        return self.optimizer.generation_list

    @property
    def generation_dict(self, milestone=0):
        return self.optimizer.get_generation_dict(milestone=milestone)

    # -1 due to initialization
    @property
    def max_generation(self):
        return len(self.generation_list) - 1

    def save_all_generation_as_file(self, file_name, milestone=0):
        generation_dict = self.optimizer.get_generation_dict(milestone=milestone)
        file_path = os.path.join(self.folder_path, file_name)
        with open(file_path, 'wb') as f:
            pickle.dump(generation_dict, f, pickle.HIGHEST_PROTOCOL)
        return

    def save_evolution_process_to_fig(self, interval=1, milestone=0):
        generation_dict = self.optimizer.get_generation_dict(milestone=milestone)
        generation_list = []
        for num, generation, time in generation_dict.values():
            generation_list.append(generation[0])

        first_front_list = MultiObjectiveAnalyzer.first_fronts_from_generations(generation_list, interval=interval)
        print(first_front_list)

    def save_experiment_config(self):
        pass

    def save_best_result_as_figure(self):
        pass

    def save_compare_front(self, front_list):
        pass