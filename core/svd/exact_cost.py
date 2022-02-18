from aae.core.sampler import DefaultSampler
from aae.core.exact_cost import Cost
from aae.core.encoder import Encoder


class SVDExactCost(Cost):
    def __init__(self, n_a, n_b, encoder: Encoder):
        self.n_a = n_a
        self.n_b = n_b
        self.encoder = encoder

    def name(self):
        return "SVDCost"

    def value(self, sampler: DefaultSampler):
        n = min(self.n_a, self.n_b)
        result = 0
        for i, p in enumerate(sampler.exact_probabilities()):
            bit_array = self.encoder.encode(i)
            for k in range(n):
                b = bit_array[k]
                b2 = bit_array[self.n_a + k]
                v = -1
                if b == b2:
                    v = 1
                result = result + p * (1 - v) / 2
        return result


class V2SVDExactCost(Cost):
    def __init__(self, n_a, n_b, encoder: Encoder):
        self.n_a = n_a
        self.n_b = n_b
        self.encoder = encoder

    def name(self):
        return "SVDCost"

    def value(self, sampler: DefaultSampler):
        n = min(self.n_a, self.n_b)
        result = 0
        for i, p in enumerate(sampler.exact_probabilities()):
            qubits = set([j for j in range(self.n_a + self.n_b)])
            bit_array = self.encoder.encode(i)
            for k in range(n):
                b = bit_array[k]
                b2 = bit_array[self.n_a + k]
                qubits.remove(k)
                qubits.remove(self.n_a + k)
                v = -1
                if b == b2:
                    v = 1
                result = result + p * (1 - v) / 2
            for q in qubits:
                result = result + p * bit_array[q] / 2
        return result
