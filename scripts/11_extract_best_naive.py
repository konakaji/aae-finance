from scripts.util import extract_best

OUTPUT_FILE = '../data/processed/datafiles-naive.txt'

maxfile_map = extract_best('../reports/overlap/', {'naive'})
with open("{}".format(OUTPUT_FILE), "w") as w:
    for span, filename in sorted(maxfile_map.items(), key=lambda v: v[0]):
        w.write("{}\n".format(filename))
