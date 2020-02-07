import sys


def usage():
    print(
        """
Usage:
 %s inputfile.csv -o outputfile.nbclustconfig
    """
        % sys.argv[0]
    )

    return 1


def main():
    if len(sys.argv) != 4:
        return usage()
    if sys.argv[2] != "-o":
        return usage()

    in_file_name = sys.argv[1]
    out_file_name = sys.argv[3]

    with open(out_file_name, "w") as out_file:
        with open(in_file_name, "r") as in_file:
            rows = in_file.read()[:-2].replace("\r", "").split("\n")
            rows = [row.split(";") for row in rows]
        rows.sort(key=lambda row: float(row[2]))

        best = rows[-1]
        params = best[1].split("_")
        out_file.write("\n".join(params))


if __name__ == "__main__":
    if main() == 1:
        exit(1)
    else:
        exit(0)
