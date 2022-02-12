import json
from aae.core.sampler import ParametrizedDefaultSampler, ParametrizedQiskitSamplerFactory, TENCircuitFactory, QISKIT, \
    QULACS
from aae.core.circuit import QiskitCircuit, QulacsCircuit
from aae.core.exception import IllegalArgumentException
from aae.core.circuit import RandomGates, TENCircuit


class SVDSampler(ParametrizedDefaultSampler):
    def __init__(self, data_circuit: RandomGates, svd_circuit: TENCircuit, type=QISKIT):
        super().__init__(svd_circuit, data_circuit.n_qubit)
        self.data_circuit = data_circuit
        self.n_qubit = data_circuit.n_qubit
        self.type = type

    def name(self):
        return "CompositeSampler"

    def _build_circuit(self):
        if self.type == QISKIT:
            qc = QiskitCircuit(self.n_qubit)
        elif self.type == QULACS:
            qc = QulacsCircuit(self.n_qubit)
        else:
            raise IllegalArgumentException("The type of the circuit is not supported.")
        qc = self.data_circuit.merge(qc)
        qc, q_register = self.circuit.merge(qc)
        return qc


class SVDQiskitSamplerFactory(ParametrizedQiskitSamplerFactory):
    def __init__(self, layer_count, data_circuit: RandomGates, type):
        super().__init__(layer_count, data_circuit.n_qubit, type)
        self.data_circuit = data_circuit

    def _create_instance(self, circuit: TENCircuit, type=None):
        return SVDSampler(self.data_circuit, circuit)

    def save(self, filename, sampler: SVDSampler, extra={}):
        with open(filename, "w") as f:
            directions = []
            parameters = []
            for i, p in enumerate(sampler.circuit.parameters):
                directions.append(sampler.circuit.directions[i])
                parameters.append(p)
            data_directions = []
            data_parameters = []
            for i, p in enumerate(sampler.data_circuit.parameters):
                data_directions.append(sampler.circuit.directions[i])
                data_parameters.append(p)
            result = {"name": sampler.name(),
                      "svd-circuit": {
                          "directions": directions,
                          "parameters": parameters,
                          "extra": extra,
                          "n-a": sampler.circuit.n_a,
                          "n-qubit": sampler.circuit.n_qubit
                      }, "data-circuit": {
                    "directions": data_directions,
                    "data_parameters": data_parameters,
                    "n-qubit": sampler.data_circuit.n_qubit,
                    "extra": extra
                }}
            f.write(json.dumps(result))

    def load(self, filename):
        with open(filename) as f:
            map = json.loads(f.read())
            c = map["svd-circuit"]
            directions = c["directions"]
            parameters = c["parameters"]
            n_a = c["n-a"]
            if "layer_count" in c["extra"]:
                self.layer_count = int(c["extra"]["layer_count"])
            circuit = TENCircuitFactory.do_generate(parameters, directions, self.n_qubit, n_a, n_a)
            return self._create_instance(circuit)
