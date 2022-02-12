from core.finance.context import Context
import numpy as np, math


def do_compute_classical(coefficient):
    result = np.diag(np.zeros(4, dtype=np.complex))
    for i in range(0, 4):
        for j in range(0, 4):
            for t, c in enumerate(coefficient[i]):
                result[i][j] = result[i][j] + c * coefficient[j][t]
    r = 0
    for v in np.linalg.eigvalsh(result):
        if v < 0:
            continue
        r = r - v * math.log(v)
    return r


# %
ticks = ["XOM", "WMT", "PG", "MSFT",
         "GE", "T", "JNJ", "CVX"]
c = Context()
usecase = c.get_coefficient_usecase()
repository = c.get_coefficient_repository()
for index in range(0, 8):
    coefficient = usecase.load(5, index, ticks)
    date = repository.get_date(index)
    print(do_compute_classical(coefficient))
