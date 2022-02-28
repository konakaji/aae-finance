import random, math
from qwrapper.encoder import Encoder
from aae.extention.data_learning import DataLearning
from core.svd.sampler import SVDSamplerFactory
from core.finance.context import Context
from scripts.util import build_state
from core.svd.exact_cost import SVDExactCost

DATA_FILE = "../data/processed/datafiles-naive.txt"
MODEL_PREFIX = "../models/"
dl = DataLearning(n_qubit=5, type="qulacs")
N_A = 3
N_B = 2
context = Context()
repo = context.get_coefficient_repository()

def compute(prefix, entropy_file):
    with open(entropy_file, "w") as w:
        with open(DATA_FILE) as f:
            for j, l in enumerate(f.readlines()):
                random.seed(0)
                datafile = l.rstrip()
                svd_file = datafile.replace("naive", prefix)
                dl.load(MODEL_PREFIX + datafile)
                factory = SVDSamplerFactory(layer_count=12, data_learning=dl, type="qulacs")
                sampler = factory.load(MODEL_PREFIX + svd_file, type="qulacs")
                if prefix == "svd-ideal":
                    sampler.cache = build_state(j)
                encoder = Encoder(5)
                map = {}
                for i, p in enumerate(sampler.exact_probabilities()):
                    bit_array = encoder.encode(i)
                    if bit_array[0] == bit_array[3] and bit_array[1] == bit_array[4] and bit_array[2] == 0 and p > 0:
                        bit_str = "{}{}{}{}".format(bit_array[0], bit_array[1], bit_array[3], bit_array[4])
                        if bit_str not in map:
                            map[bit_str] = 0
                        map[bit_str] = map[bit_str] + p
                result = 0
                prob = 0
                eigens = []
                for key, p in map.items():
                    result = result - p * math.log(p)
                    eigens.append(p)
                    prob = prob + p
                print(result, prob)
                w.write("{}\t{}\t{}\n".format(repo.get_date(j + 4), result, sorted(eigens, reverse=True)))
            print("---------------")



compute("naivesvd", "../reports/quantum-naive.txt")
# compute("svd-ideal", "../reports/quantum-ideal.txt")
