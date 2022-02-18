import os, numpy as np
from core.finance.context import Context
from aae.extention.data_learning import DataLearning

context = Context()
repo = context.get_coefficient_repository()

for filename in os.listdir("../reports/depr/model"):
    items = filename.split("_")
    if len(items) != 5:
        continue
    dl = DataLearning(6)
    dl.load("../reports/depr/model/{}".format(filename))
    _, span, d_index, layer, seed = items
    d_index = int(d_index)
    vector = repo.load(5, d_index, ["XOM", "WMT", "PG", "MSFT",
                                    "GE", "T", "JNJ", "CVX"]).flatten()
    overlap = abs(np.array(dl.get_state_vector()).dot(np.array(vector)))
    file = filename.replace("data", "fdata")
    with open("../reports/overlap/{}".format(file), "w") as f:
        f.write(str(overlap))
    with open("../reports/depr/model/{}".format(filename)) as f:
        with open("../models/{}".format(file), "w") as w:
            for l in f.readlines():
                w.write(l)
