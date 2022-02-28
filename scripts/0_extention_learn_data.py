# %%

import sys, os

sys.path.append("../")
sys.path.append("../venv/lib/python3.8/site-packages")

from aae.extention.data_learning import DataLearning
from aae.extention.aae import AAETrainingMethod
from aae.core.optimizer import TransformingLRScheduler
from core.finance.context import Context
from scripts.util import extract_best
import random, numpy as np

# %%

nqubit = 6
layer = 0
TIME_SPAN = 5
START = 1
FINISH = 7
ticks = ["XOM", "WMT", "PG", "MSFT",
         "GE", "T", "JNJ", "CVX"]
MODEL_FORMAT = "../models/{}data_{}_{}_{}_{}.json"
ENERGY_FORMAT = "../reports/energy/{}data_{}_{}_{}_{}.json"
OVERLAP_FORMAT = "../reports/overlap/{}data_{}_{}_{}_{}.json"

scheduler = TransformingLRScheduler(lr=0.01)
scheduler.schedule(200, 0.01)

context = Context()
repository = context.get_coefficient_repository()
context.get_history_repository()
for iter in [50, 100, 150]:
    for index in [1]:
        data_learning = DataLearning(nqubit, layer, type="qulacs")
        filename = extract_best("../reports/overlap/", {"data"})[str(index)]
        filename = "data_5_1_13_1.json"
        data_learning.load("../models/" + filename)
        prefix, span, ind, layer, seed = filename.split("_")
        seed = int(seed.replace(".json", ""))
        training_method = AAETrainingMethod(iteration=iter, lr_scheduler=scheduler, idblock=False)
        date = repository.get_date(index)
        print("start_learning {}".format(date))
        # if os.path.exists(MODEL_FORMAT.format(iter + 200, span, index, layer, seed)):
        #     print("model file exists. skip.")
        #     continue
        matrix = repository.load(TIME_SPAN, index, ticks)
        array = matrix.flatten()
        random.seed(seed)
        np.random.seed(seed)
        vector = data_learning.learn(array, training_method=training_method)
        overlap = abs(np.array(array).dot(np.array(vector)))
        print("overlap", overlap)
        print(training_method.get_cost(data_learning.sampler))
        with open(OVERLAP_FORMAT.format(iter + 200, TIME_SPAN, index, layer, seed), "w") as w:
            w.write(str(overlap))
        data_learning.save_model(MODEL_FORMAT.format(iter + 200, TIME_SPAN, index, layer, seed))
        data_learning.save_cost_transition(ENERGY_FORMAT.format(iter + 200, TIME_SPAN, index, layer, seed))
