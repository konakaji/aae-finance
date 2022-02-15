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
layer = 13
TIME_SPAN = 5
START = 1
FINISH = 7
ticks = ["XOM", "WMT", "PG", "MSFT",
         "GE", "T", "JNJ", "CVX"]
MODEL_FORMAT = "../models/data_{}_{}_{}_{}.json"
ENERGY_FORMAT = "../reports/energy/data_{}_{}_{}_{}.json"
OVERLAP_FORMAT = "../reports/overlap/data_{}_{}_{}_{}.json"

scheduler = TransformingLRScheduler(lr=0.1)
scheduler.schedule(100, 0.01)

context = Context()
repository = context.get_coefficient_repository()
context.get_history_repository()
for loop in [1]:
    for index in [5]:
        data_learning = DataLearning(nqubit, layer, type="qulacs")
        training_method = AAETrainingMethod(iteration=200, lr_scheduler=scheduler, idblock=False)
        date = repository.get_date(index)
        print("start_learning {}".format(date))
        seed = index + 31 * loop
        if os.path.exists(MODEL_FORMAT.format(TIME_SPAN, index, layer, seed)):
            print("model file exists. skip.")
            continue
        random.seed(seed)
        matrix = repository.load(TIME_SPAN, index, ticks)
        array = matrix.flatten()
        vector = data_learning.learn(array, training_method=training_method)
        overlap = abs(np.array(array).dot(np.array(vector)))
        print("overlap", overlap)
        print(training_method.get_cost(data_learning.sampler))
        with open(OVERLAP_FORMAT.format(TIME_SPAN, index, layer, seed), "w") as w:
            w.write(str(overlap))
        data_learning.save_model(MODEL_FORMAT.format(TIME_SPAN, index, layer, seed))
        data_learning.save_cost_transition(ENERGY_FORMAT.format(TIME_SPAN, index, layer, seed))
