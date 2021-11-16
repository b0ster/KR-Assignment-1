import argparse
import math
import os
from time import time, strftime, localtime
from typing import Tuple

from sat.dpll import DPLL
from sat.heuristic.heuristic import Heuristic
from sat.heuristic.length_priority_heuristic import LengthPriorityHeuristic
from sat.heuristic.one_sided_jeroslow_wang_heuristic import OneSidedJeroslowWangHeuristic
from sat.heuristic.mom_heuristic import MOMHeuristic
from sat.heuristic.two_sided_jeroslow_wang_heuristic import TwoSidedJeroslowWangHeuristic
from util.sat_problem import SATProblem

result_dir = "results/"
dplls = {
    "1": lambda p: DPLL(p, heuristic=Heuristic()),
    "2": lambda p: DPLL(p, heuristic=MOMHeuristic()),
    "3": lambda p: DPLL(p, heuristic=OneSidedJeroslowWangHeuristic()),
    "4": lambda p: DPLL(p, heuristic=TwoSidedJeroslowWangHeuristic()),
    "5": lambda p: DPLL(p, heuristic=LengthPriorityHeuristic())

    # todo: add more DPLLs with heuristics here
}

arg_parser = argparse.ArgumentParser(description="SAT solve using DPLL")
arg_parser.add_argument('-S', choices=list(dplls.keys()), default="1", required=True, help='SAT version')
arg_parser.add_argument('--is-sudoku', choices=['yes', 'no'], default='yes')
arg_parser.add_argument('rest', nargs=argparse.REMAINDER)


def save_results(assignments: Tuple[int, bool], is_sudoku: bool):
    list_a = list(assignments.items())
    dir_name = result_dir + strftime("%d_%m_%Y_%H_%M_%S", localtime(time()))
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    dm = SATProblem()
    for x, y in list_a:
        if y:
            dm.add_clause([x])
    dm.save_to_file_dimacs("sat_result", dir_name + "/dimacs.txt")
    if is_sudoku:
        vars = dm.get_all_variables()
        dim = round(math.sqrt(len(dm.get_clauses().values())))
        sudoku_str = ""
        for i in range(dim):
            for j in range(dim):
                result = [v for v in vars if str(v).startswith(str(i + 1) + str(j + 1))]
                sudoku_str += str(result[0])[2:] + " "
            sudoku_str += "\n"
            with open(dir_name + "/sudoku.txt", 'w') as file:
                file.write(sudoku_str)
    print("Saved results to directory '{}'".format(dir_name))


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
    save_results(assignments, '--is-sudoku' not in args or args['--is-sudoku'] == 'yes')

    # variable assignment history
    variable_assignment_history = dpll.get_variable_assignment_history()

    # original unit clauses
    original_unit_variables = dpll.get_initial_unit_variables()
