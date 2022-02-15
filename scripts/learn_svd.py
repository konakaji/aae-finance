import sys
from aae.extention.data_learning import DataLearning
from aae.core.optimizer import AdamOptimizer, UnitLRScheduler
from aae.core.task import AdamOptimizationTask
from aae.core.task import TaskWatcher
from qwrapper.encoder import Encoder
from core.svd.sampler import SVDSamplerFactory
from core.svd.exact_cost import SVDExactCost
import random, os

sys.path.append("../")
sys.path.append("../venv/lib/python3.8/site-packages")

DATA_FILE = "../data/processed/datafiles.txt"
MODEL_PREFIX = "../models/"
ENERGY_PREFIX = "../reports/energy/"
dl = DataLearning(n_qubit=6, type="qulacs")
N_A = 3
N_B = 2
with open(DATA_FILE) as f:
    for l in f.readlines():
        random.seed(0)
        datafile = l.rstrip()
        output_file = datafile.replace("data", "svd")
        if os.path.exists(MODEL_PREFIX + output_file):
            print("model file exists, skip.")
            continue
        dl.load(MODEL_PREFIX + datafile)
        factory = SVDSamplerFactory(8, dl, "qulacs")
        sampler = factory.generate_ten(N_A, N_B)
        sampler.add_post_select(0, 1)
        optimizer = AdamOptimizer(scheduler=UnitLRScheduler(0.1), maxiter=200)
        cost = SVDExactCost(N_A, N_B, Encoder(5))
        task_watcher = TaskWatcher([], [cost])
        task = AdamOptimizationTask(sampler, cost, optimizer, task_watcher)
        task.optimize()
        task_watcher.save_energy(ENERGY_PREFIX + output_file)
        factory.save(MODEL_PREFIX + output_file, sampler)
