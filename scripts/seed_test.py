# %%

import sys, os

sys.path.append("../")
sys.path.append("../venv/lib/python3.8/site-packages")

from aae.extention.data_learning import DataLearning
from aae.extention.aae import AAETrainingMethod
from aae.core.optimizer import TransformingLRScheduler
from core.finance.context import Context
import random, numpy as np

# %%

nqubit = 6
layer = 5
TIME_SPAN = 5
START = 1
FINISH = 7
ticks = ["XOM", "WMT", "PG", "MSFT",
         "GE", "T", "JNJ", "CVX"]
MODEL_FORMAT = "../models/rdata_{}_{}_{}_{}.json"
ENERGY_FORMAT = "../reports/energy/rdata_{}_{}_{}_{}.json"
OVERLAP_FORMAT = "../reports/overlap/rdata_{}_{}_{}_{}.json"

scheduler = TransformingLRScheduler(lr=0.1)
scheduler.schedule(100, 0.01)

context = Context()
repository = context.get_coefficient_repository()
context.get_history_repository()

watchers = []
for j in range(2):
    for index in [0]:
        data_learning = DataLearning(nqubit, layer, type="qulacs")
        # data_learning.load("../models/" + extract_best("../reports/overlap/")['0'])
        training_method = AAETrainingMethod(iteration=3, lr_scheduler=scheduler, idblock=False)
        date = repository.get_date(index)
        print("start_learning {}".format(date))
        seed = 0
        random.seed(seed)
        np.random.seed(seed)
        matrix = repository.load(TIME_SPAN, index, ticks)
        array = matrix.flatten()
        vector = data_learning.learn(array, training_method=training_method)
        overlap = abs(np.array(array).dot(np.array(vector)))
        print("overlap", overlap)
        watchers.append(training_method.task_watcher)