import numpy as np, os
from core.finance.context import Context
from qulacs import QuantumState, QuantumCircuit
from qulacs.gate import DenseMatrix


def build_state(j):
    context = Context()
    repo = context.get_coefficient_repository()
    array = repo.load(5, j, ["XOM", "WMT", "PG", "MSFT",
                             "GE", "T", "JNJ", "CVX"]).flatten()
    matrix = np.diag(np.zeros(len(array)))
    for j, a in enumerate(array):
        matrix[j][0] = a
    gate = DenseMatrix([1, 2, 3, 4, 5], matrix)
    state = QuantumState(6)
    circuit = QuantumCircuit(6)
    state.set_zero_state()
    circuit.add_X_gate(0)
    circuit.update_quantum_state(state)
    gate.update_quantum_state(state)
    return state


def extract_best(dir, prefix=None):
    DIR = dir
    max_map = {}
    maxfile_map = {}
    for filename in os.listdir(DIR):
        item = filename.split("_")
        if len(item) != 5:
            continue
        p, span, d_index, l_count, seed = item
        if prefix is not None and p not in prefix:
            continue
        with open("{}{}".format(DIR, filename)) as f:
            v = float(f.readlines()[0])
            if d_index not in max_map or v > max_map[d_index]:
                max_map[d_index] = v
                maxfile_map[d_index] = filename
    return maxfile_map
