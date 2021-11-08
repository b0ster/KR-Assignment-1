from sat.sat_solver import SatSolver
from util.dimacs import DIMACS

if __name__ == '__main__':
    d = DIMACS(file="data/test-rules.txt")
    ss = SatSolver(rules=d)
    satisfied, assignments = ss.solve(d, d.get_all_variables(), {})
    print("Satisfied: {}, Assignments: {}".format(satisfied, assignments))

