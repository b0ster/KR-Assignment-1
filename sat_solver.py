import argparse

from sat.dpll import DPLL
from util.dimacs import DIMACS

arg_parser = argparse.ArgumentParser(description="SAT solve using DPLL")

arg_parser.add_argument('-S',
                        choices=["1", "2", "3"],
                        default="1",
                        required=True,
                        help='SAT version')

arg_parser.add_argument('rest', nargs=argparse.REMAINDER)

# usage: python sat_solver.py -S{1,2,3} [dimacs-file-1] [dimacs-file-2] [....]
# note: dimacs files are merged, hence the CNF increases
if __name__ == '__main__':
    args = arg_parser.parse_args()
    total_problem = DIMACS()
    if len(args.rest) == 0:
        raise Exception("Please give at least one DIMACS file...")
    for problem in args.rest:
        d = DIMACS(file=problem)
        for c in d.get_clauses().values():
            total_problem.add_clause(c)
    dppl = DPLL()

    # this, for now, finds any satisfying sudoku, as only the rules need to be satisfied.
    # todo, here, the sudoku models must be given as a parameter
    satisfied, assignments = dppl.solve(total_problem, total_problem.get_all_variables(), {})
    print("Satisfied: {}, Assignments: {}".format(satisfied,
                                                  [(k, j) for k, j in assignments.items() if j] if satisfied else "-"))
