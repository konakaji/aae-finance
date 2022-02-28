from qulacs import QuantumState, QuantumCircuit
import random
import numpy as np

for j in range(2):
    s = QuantumState(2)
    c = QuantumCircuit(2)
    c.add_H_gate(0)
    c.add_H_gate(1)

    c.update_quantum_state(s)
    print("-----------")
    for j in s.sampling(10, seed=1):
        print(j)