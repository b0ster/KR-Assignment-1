import math, argparse
import os

arg_parser = argparse.ArgumentParser(description="Sudoku dotted format to DIMACS format converter")

arg_parser.add_argument('-infile',
                        required=True,
                        help='Input file of dotted Sudoku(s)')

arg_parser.add_argument('-outdir',
                        required=True,
                        help='Output directory to save the sudoku(s)')

if __name__ == "__main__":
    args = arg_parser.parse_args()
    if not os.path.exists(args.outdir):
        raise Exception("Directory {} should be created first".format(args.outdir))
    with open(args.infile) as sudokus_raw:
        sudokus = sudokus_raw.read()
        sudokus = sudokus.split("\n")
        s_count = 0
        for sudoku in sudokus:
            s_count += 1
            n_dim = round(math.sqrt(len(sudoku)))
            name = "sudoku-{}x{}-{}".format(n_dim, n_dim, s_count)
            loc = args.outdir + "/" + name + ".txt"
            dimacs = []
            dimacs.append("c " + name + ".cnf")
            total = 0
            for i in range(n_dim):
                for j in range(n_dim):
                    c = sudoku[total]
                    if c != ".":
                        clause = str(i + 1) + str(j + 1) + c + " 0"
                        dimacs.append(clause)
                    total += 1
            dimacs.insert(1, "p cnf {}{}{} {}".format(n_dim, n_dim, 9, len(dimacs) - 1))
            with open(loc, "w") as output:
                for l in dimacs:
                    output.write(l + "\n")
