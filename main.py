import sys
import os
from sklearn.metrics.cluster import adjusted_mutual_info_score
from itertools import compress


def main():
    pred_label_file = sys.argv[1]
    true_label_file = sys.argv[2]
    assert sys.argv[3] == "-o"
    out_dir = sys.argv[4]
    out_file = pred_label_file.split("/")[-1][:-4]

    try:
        with open(true_label_file, "r") as f:
            true_label = f.read()
    except:
        true_label = "-\n-"

    COL = int(os.environ.get('CITYCOL', '5'))  # city
    true_label = true_label.split("\n")[1:]  # ignore header
    true_label = [l.split("\t") for l in true_label]
    true_label = list(filter(lambda l: len(l) >= COL, true_label))
    true_label = [l[COL - 1] for l in true_label]

    try:
        with open(pred_label_file, "r") as f:
            pred_label = f.read()
    except:
        pred_label = "-\n-"

    COL = 2  # prediction
    pred_label = pred_label.split("\n")[1:]  # ignore header
    pred_label = [l.split(" ") for l in pred_label]
    pred_label = list(filter(lambda l: len(l) >= COL, pred_label))
    pred_label = [l[COL - 1] for l in pred_label]

    mask = [
        label != "REMOVE" for label in true_label
    ]
    true_label = list(compress(true_label, mask))
    pred_label = list(compress(pred_label, mask))

    try:
        score = adjusted_mutual_info_score(true_label, pred_label)
    except:
        score = 0.0

    with open("%s/%s" % (out_dir, out_file), "w") as f:
        print(score, file=f)


if __name__ == "__main__":
    main()
