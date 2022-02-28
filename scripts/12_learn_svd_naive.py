import sys
from aae.extention.data_learning import DataLearning
from aae.core.optimizer import AdamOptimizer, UnitLRScheduler
from aae.core.task import AdamOptimizationTask
from aae.core.task import TaskWatcher
from qwrapper.encoder import Encoder
from core.svd.sampler import SVDSamplerFactory
from core.svd.exact_cost import SVDExactCost, V2SVDExactCost
from core.finance.context import Context
import random, os

context = Context()
repo = context.get_coefficient_repository()

sys.path.append("../")
sys.path.append("../venv/lib/python3.8/site-packages")

DATA_FILE = "../data/processed/datafiles-naive.txt"
MODEL_PREFIX = "../models/"
ENERGY_PREFIX = "../reports/energy/"
dl = DataLearning(n_qubit=5, type="qulacs")

N_A = 3
N_B = 2
use_cache = True
with open(DATA_FILE) as f:
    for index, l in enumerate(f.readlines()):
        seed = 3
        random.seed(seed)
        datafile = l.rstrip()
        output_file = datafile.replace("naive", "naivesvd")
        if use_cache and os.path.exists(MODEL_PREFIX + output_file):
            print("model file exists, skip: {}".format(index))
            continue
        dl.load(MODEL_PREFIX + datafile)
        factory = SVDSamplerFactory(12, dl, "qulacs")
        sampler = factory.generate_ten(N_A, N_B)
        optimizer = AdamOptimizer(scheduler=UnitLRScheduler(0.01), maxiter=500)
        cost = V2SVDExactCost(N_A, N_B, Encoder(5))
        task_watcher = TaskWatcher([], [cost])
        task = AdamOptimizationTask(sampler, cost, optimizer, task_watcher)
        task.optimize()
        task_watcher.save_energy(ENERGY_PREFIX + output_file)
        factory.save(MODEL_PREFIX + output_file, sampler, extra={"seed": seed})
