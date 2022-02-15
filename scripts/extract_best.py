import os

DIR = '../reports/overlap/'
OUTPUT_FILE = '../data/processed/datafiles.txt'

max_map = {}
maxfile_map = {}
for filename in os.listdir(DIR):
    item = filename.split("_")
    if len(item) != 5:
        continue
    _, span, d_index, l_count, seed = item
    with open("{}{}".format(DIR, filename)) as f:
        v = float(f.readlines()[0])
        if d_index not in max_map or v > max_map[d_index]:
            max_map[d_index] = v
            maxfile_map[d_index] = filename

with open("{}".format(OUTPUT_FILE), "w") as w:
    for span, filename in sorted(maxfile_map.items(), key=lambda v: v[0]):
        w.write("{}\n".format(filename))
