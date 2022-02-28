from aae.extention.base import TrainingMethod, GradientOptimizationTask
from aae.core.optimizer import AdamOptimizer, UnitLRScheduler
from aae.core.gradient_cost import MMDGradientCost
from aae.core.exact_cost import MMDCost, KLCost
from aae.core.mapper import CoefficientMapperPositive
from aae.core.encoder import Encoder
from aae.core.task import TaskWatcher

NAIVE_KEY = "naive-key"


class NaiveMapper(CoefficientMapperPositive):
    def map(self, coefficient):
        return self._do_map(coefficient)


class NaiveTrainingMethod(TrainingMethod):
    def __init__(self, lr=0.1, n_shot=400, iteration=200, lr_scheduler=None):
        super(NaiveTrainingMethod, self).__init__()
        if lr_scheduler is None:
            self.scheduler = UnitLRScheduler(lr=lr)
        else:
            self.scheduler = lr_scheduler
        self.cost = None
        self.iter = iteration
        self.n_shot = n_shot

    def build(self, data_sampler, coefficients, n_qubit, factory) -> GradientOptimizationTask:
        probability = self.get_mapper(data_sampler, n_qubit).map(coefficients)
        encoder = Encoder(n_qubit)
        gradient_cost = MMDGradientCost(probability, encoder)
        self.cost = MMDCost(probability, encoder)
        task_watcher = TaskWatcher([], [self.cost, KLCost(probability, encoder)])
        self.task_watcher = task_watcher
        optimizer = AdamOptimizer(scheduler=self.scheduler, maxiter=self.iter)
        return GradientOptimizationTask(data_sampler,
                                        factory,
                                        gradient_cost,
                                        task_watcher,
                                        self.n_shot, optimizer)

    def get_cost(self, data_sampler):
        return self.cost.value(data_sampler)

    def get_mapper(self, data_sampler, n):
        return NaiveMapper(n, data_sampler.encoder)

    @classmethod
    def get_name(cls):
        return NAIVE_KEY
