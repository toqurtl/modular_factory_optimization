from moga.generation import Fronting
import os

class MultiObjectiveAnalyzer(object):

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
    def first_fronts_from_generations(generation_list, interval=1):
        first_front_list = []
        generation_list.reverse()
        for idx, generation in enumerate(generation_list):
            if idx % interval == 0:
                first_front = MultiObjectiveAnalyzer.nth_front_from_generation(generation, 0)
                first_front_list.append(first_front)
        return first_front_list

    @staticmethod
    def save_factory_information_to_excel(chromosome):
        pass

    @staticmethod
    def generation_list_to_excel(chromosome):
        pass


class MultiObjectiveAnalysis(object):
    def __init__(self, optimizer, folder_path):
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

    def save_all_generation_as_file(self):
        pass

    def save_evolution_process_to_excel(self):
        pass

    def save_experiment_config(self):
        pass

    def save_best_result_as_figure(self):
        pass

    def save_compare_front(self, front_list):
        pass