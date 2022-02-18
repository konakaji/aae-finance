from core.finance.context import Context
import numpy as np, math
import matplotlib.pyplot as plt


def do_compute_classical(a, s_dim, t_dim):
    c = np.diag(np.zeros(s_dim, dtype=np.complex))
    for j in range(0, s_dim):
        for k in range(0, s_dim):
            for t in range(0, t_dim):
                c[j][k] = c[j][k] + a[j][t] * a[k][t]
    r = 0
    eigens = []
    for v in np.linalg.eigvalsh(c):
        if v < 0:
            continue
        eigens.append(v)
        r = r - v * math.log(v)
    return r, sorted(eigens, reverse=True)


# %%

c = Context()
usecase = c.get_coefficient_usecase()
repository = c.get_coefficient_repository()
plt.figure(figsize=(10, 4))
plt.title("computation of SVD entropy")
plt.grid()
plt.ylim([0.5, 1.2])

ticks = ["XOM", "WMT", "PG", "MSFT",
         "GE", "T", "JNJ", "CVX"]
dates = []
indices = []
values = []
with open("../reports/classical.txt", "w") as f:
    for index in range(0, 8):
        coefficient = usecase.load(5, index, ticks)
        date = repository.get_date(index)
        value, eigens = do_compute_classical(coefficient, len(ticks), 4)
        f.write("{}\t{}\t{}\n".format(date, value, eigens))
