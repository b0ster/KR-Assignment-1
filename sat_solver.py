import argparse

from sat.dpll import DPLL
from util.dimacs import DIMACS

arg_parser = argparse.ArgumentParser(description="SAT solve using DPLL")
arg_parser.add_argument('-S', choices=["1", "2", "3"], default="1", required=True, help='SAT version')
arg_parser.add_argument('rest', nargs=argparse.REMAINDER)

dplls = {
    "1": DPLL(heuristics=None),
    "2": DPLL(heuristics=DPLL.heuristic_unit_prioritize)
    # todo: add more DPLLs with heuristics here
}

# usage: python sat_solver.py -S{1,2,3} [dimacs-file-1] [dimacs-file-2] [....]
if __name__ == '__main__':
    args = arg_parser.parse_args()
    if len(args.rest) == 0:
        raise Exception("Please give at least one DIMACS file...")

    total_problem = DIMACS()
    # merge the different DIMACS files as this is a CNF
    for problem in args.rest:
        d = DIMACS(file=problem)
        for c in d.get_clauses().values():
            total_problem.add_clause(c)

    if args.S not in dplls:
        raise Exception("DPLL with id '{}' has not been implemented yet.".format(args.S))
    # solve the merged SAT problems using the DPLL algorithm
    satisfied, assignments = dplls[args.S].solve(total_problem, {})
    # make a printable solution if there is one
    items = list(assignments.items())
    items.sort()
    solution = [(k, j) for k, j in items if j] if satisfied else "-"
    print("Satisfied: {}, Assignments: {}".format(satisfied, solution))
    # todo, save found solution to a new DIMACS file
