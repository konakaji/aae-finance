import json
from aae.core.sampler import ParametrizedDefaultSampler, ParametrizedDefaultSamplerFactory, TENCircuitFactory, QISKIT, \
    QULACS
from aae.core.circuit import QiskitCircuit, QulacsCircuit
from aae.core.exception import IllegalArgumentException
from aae.core.circuit import TENCircuit
from aae.extention.data_learning import DataLearning


class SVDSampler(ParametrizedDefaultSampler):
    def __init__(self, data_learning: DataLearning, svd_circuit: TENCircuit, type=QISKIT):
        super().__init__(svd_circuit, data_learning.n)
        self.data_learning = data_learning
        self.n_qubit = data_learning.n
        self.type = type
        self.cache = None

    def name(self):
        return "CompositeSampler"

    def _build_circuit(self):
        if self.type == QISKIT:
            qc = QiskitCircuit(self.n_qubit)
        elif self.type == QULACS:
            qc = QulacsCircuit(self.n_qubit)
        else:
            raise IllegalArgumentException("The type of the circuit is not supported.")
        if self.type == QULACS:
            if self.cache is None:
                self.data_learning.add_data_gates(qc)
                self.cache = qc.get_state()
            else:
                qc.state = self.cache
        else:
            self.data_learning.add_data_gates(qc)
        qc = self.circuit.merge(qc)
        return qc


class SVDSamplerFactory(ParametrizedDefaultSamplerFactory):
    def __init__(self, layer_count, data_learning: DataLearning, type):
        super().__init__(layer_count, data_learning.n, type)
        self.data_learning = data_learning

    def _create_instance(self, circuit: TENCircuit, type=None):
        if type is None:
            type = self.type
        return SVDSampler(self.data_learning, circuit, type)

    def save(self, filename, sampler: SVDSampler, extra={}):
        with open(filename, "w") as f:
            directions = []
            parameters = []
            for i, p in enumerate(sampler.circuit.parameters):
                directions.append(sampler.circuit.directions[i])
                parameters.append(p)
            data_directions = []
            data_parameters = []
            for i, p in enumerate(self.data_learning.sampler.circuit.parameters):
                data_directions.append(self.data_learning.sampler.circuit.directions[i])
                data_parameters.append(p)
            result = {"name": sampler.name(),
                      "svd-circuit": {
                          "directions": directions,
                          "parameters": parameters,
                          "extra": extra,
                          "n-a": sampler.circuit.n_a,
                          "n-b": sampler.circuit.n_b,
                          "n-qubit": sampler.circuit.n_qubit
                      }, "data-circuit": {
                    "directions": data_directions,
                    "data_parameters": data_parameters,
                    "n-qubit": self.data_learning.n,
                    "extra": extra
                }}
            f.write(json.dumps(result, indent=2))

    def load(self, filename, type):
        with open(filename) as f:
            map = json.loads(f.read())
            c = map["svd-circuit"]
            directions = c["directions"]
            parameters = c["parameters"]
            n_a = c["n-a"]
            n_b = c["n-b"]
            if "layer_count" in c["extra"]:
                self.layer_count = int(c["extra"]["layer_count"])
            circuit = TENCircuitFactory.do_generate(parameters, directions, self.n_qubit, n_a, n_b)
            return self._create_instance(circuit, type)
