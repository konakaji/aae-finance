from flask import Flask, render_template
from scripts.util import extract_best

FOLDER = "reports"
OVERLAP = FOLDER + "/overlap/"
ENERGY = FOLDER + "/energy/"

app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/')
def index():
    results = []
    for d_index, filename in extract_best(OVERLAP, "rdata").items():
        items = filename.split("_")
        if len(items) != 5:
            continue
        data_index = int(items[2])
        layer = int(items[3])
        with open("{}{}".format(OVERLAP, filename)) as f:
            overlap = float(f.readlines()[0])
            results.append((filename, filename.replace("data", "svd"), data_index, layer, round(overlap, 2)))
    results = sorted(results, key=lambda r: 31 * r[2] + r[3] + (1 - overlap) * 100)
    return render_template('index.html', results=results)


@app.route('/energy/<filename>')
def energy(filename):
    with open(ENERGY + filename) as f:
        lines = []
        for l in f.readlines():
            lines.append(l.rstrip())
    return render_template('energy.html', lines=lines)


app.run(port=4000, debug=True)
