from moga.generation import MultiObjectiveGenerator, MultiObjGenericEnum
from moga.optimizer import ParetoOptimizer


class Optimizer(object):
    def __init__(self):
        self.multi_obj_generator = MultiObjectiveGenerator()
        self.optimizer = ParetoOptimizer()
        self.setting_complete = False

    def setting(self, objective_functions, generic_parameter_dict, optimizer_parameter_dict):
        self.__set_objective_function(objective_functions)
        self.__set_generic_parameter_dict(generic_parameter_dict)
        self.__set_optimizer_parameter_dict(optimizer_parameter_dict)
        self.__setting()
        self.setting_complete = True

    def set_local_algorithm(self, local_enum):
        self.multi_obj_generator.local_algorithm_enum = local_enum

    # input of func: chro_str, output of func: np_array
    def __set_objective_function(self, func):
        self.multi_obj_generator.set_fitness_func(func)

    def __set_generic_parameter_dict(self, generic_parameter_dict):
        self.multi_obj_generator.set_generic_parameter_dict(generic_parameter_dict)

    def __setting(self):
        self.optimizer.set_generation_generator(self.multi_obj_generator)

    def __set_optimizer_parameter_dict(self, optimizer_parameter_dict):
        self.optimizer.setting(
            num_chromosome_in_generation=optimizer_parameter_dict['num_chromosome_in_generation'],
            max_generation=optimizer_parameter_dict['max_generation'],
            num_objective=optimizer_parameter_dict['num_objective']
        )

    def initialization(self):
        if self.setting_complete:
            self.optimizer.initialization()
        return self.setting_complete

    def optimize(self, file_path=None):
        if self.setting_complete:
            self.optimizer.optimize(file_path)
        return self.setting_complete

    def to_analyzer(self):
        pass

    @property
    def generation_list(self):
        return self.optimizer.generation_list

    def get_generation_dict(self, milestone=0):
        generation_dict = {}
        generation_list = self.generation_list
        for idx, generation in enumerate(generation_list):
            if idx != 0:
                num = idx + milestone
                time = self.optimizer.time_measure_list[idx-1]
                generation_dict[num] = (num, generation, time)
        return generation_dict

