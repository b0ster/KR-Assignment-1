import argparse

from sat.dpll import DPLL
from sat.heuristic.heuristic import Heuristic
from sat.heuristic.one_sided_jeroslow_wang_heuristic import OneSidedJeroslowWangHeuristic
from sat.heuristic.mom_heuristic import MOMHeuristic
from sat.heuristic.two_sided_jeroslow_wang_heuristic import TwoSidedJeroslowWangHeuristic
from util.sat_problem import SATProblem

from visualizer import Visualizer

dplls = {
    "1": lambda p: DPLL(p, heuristic=Heuristic()),
    "2": lambda p: DPLL(p, heuristic=MOMHeuristic()),
    "3": lambda p: DPLL(p, heuristic=OneSidedJeroslowWangHeuristic()),
    "4": lambda p: DPLL(p, heuristic=TwoSidedJeroslowWangHeuristic())

    # todo: add more DPLLs with heuristics here
}

arg_parser = argparse.ArgumentParser(description="SAT solve using DPLL")
arg_parser.add_argument('-S', choices=list(dplls.keys()), default="1", required=True, help='SAT version')
arg_parser.add_argument('rest', nargs=argparse.REMAINDER)

# usage: python sat_solver.py -S{1,2,3} [dimacs-file-1] [dimacs-file-2] [....]
if __name__ == '__main__':
    args = arg_parser.parse_args()
    if len(args.rest) == 0:
        raise Exception("Please give at least one DIMACS file...")

    total_problem = SATProblem()
    # merge the different DIMACS files as this is a CNF
    for problem in args.rest:
        d = SATProblem(file=problem)
        for c in d.get_clauses().values():
            total_problem.add_clause(c)

    if args.S not in dplls:
        raise Exception("DPLL with id '{}' has not been implemented yet.".format(args.S))
    # solve the merged SAT problems using the DPLL algorithm
    dpll = dplls[args.S](total_problem)
    satisfied, assignments = dpll.solve({})

    # make a printable solution if there is one
    items = list(assignments.items())
    items.sort()
    solution = [(k, j) for k, j in items if j] if satisfied else "-"
    print("\nSatisfied: {}, Assignments: {}".format(satisfied, solution))
    # todo, save found solution to a new DIMACS file

    # variable assignment history
    variable_assignment_history = dpll.get_variable_assignment_history()

    # original unit clauses
    original_unit_variables = dpll.get_initial_unit_variables()

    viz = Visualizer(original_unit_variables, variable_assignment_history, out_path=None)
    viz.run()
