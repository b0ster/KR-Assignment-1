from util.dimacs import DIMACS

if __name__ == '__main__':
    dimacs = DIMACS(file="data/sudoku-rules.txt")
    for l in dimacs.get_clauses():
        print(l)
