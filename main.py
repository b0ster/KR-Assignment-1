from sat.sat_solver import SatSolver
from util.dimacs import DIMACS

if __name__ == '__main__':
    d = DIMACS(file="data/sudoku-rules.txt")
    ss = SatSolver(rules=d)

    # this, for now, finds any satisfying sudoku, as only the rules need to be satisfied.
    # todo, here, the sudoku models must be given as a parameter
    satisfied, assignments = ss.solve(d, d.get_all_variables(), {})
    print("Satisfied: {}, Assignments: {}".format(satisfied,
                                                  [(k, j) for k, j in assignments.items() if j] if satisfied else "-"))
