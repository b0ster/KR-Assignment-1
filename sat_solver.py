import argparse
import math
import os
import csv
from time import time, strftime, localtime
# from typing import tuple, list

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

# these are the arguments available
arg_parser = argparse.ArgumentParser(description="SAT solve using DPLL")
arg_parser.add_argument('-S', choices=list(dplls.keys()), default="1", required=True, help='SAT version')
arg_parser.add_argument('--is-sudoku', choices=['yes', 'no'], default='yes', help='If the target problem is a sudoku')
arg_parser.add_argument('-O', help='Output folder for results')
arg_parser.add_argument('-ID', help='ID of the problem to add to the results', required=False)
arg_parser.add_argument('rest', nargs=argparse.REMAINDER, help='DIMACS files (to be merged)')


def __merge_sat_problems__(sp: list[SATProblem]) -> SATProblem:
    """
    Merges a list of SATProblem into one single problem.
    :param sp: List of SATProblem instances.
    :return: a merged combined SATProblem.
    """
    total_problem = SATProblem()
    # merge the different DIMACS files as this is a CNF
    for problem in sp:
        for c in problem.get_clauses().values():
            total_problem.add_clause(c)
    return total_problem


def __save_results__(assignments: tuple[int, bool], is_sudoku: bool, dpll: DPLL, output_dir: str, id=None) -> None:
    """
    Saves the results of the SAT solving to disk.
    :param assignments: assignments of all variables.
    :param is_sudoku: whether the SAT problem is a sudoku, if so more results are saved.
    """
    # save model to DIMACS format
    list_a = list(assignments.items())
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    dm = SATProblem()

    for x, y in list_a:
        if y:
            dm.add_clause(([abs(x)]))
        else:
            dm.add_clause([-abs(x)])
    dm.save_to_file_dimacs("sat_result", output_dir + "/dimacs.txt")

    # save the stats
    stats = dpll.get_stats_map()
    stats["id"] = id
    with open(output_dir + "/stats.csv", 'w') as stats_csv:
        keys = list(stats.keys())
        keys.sort()
        writer = csv.DictWriter(stats_csv, fieldnames=keys)
        writer.writeheader()
        writer.writerow(stats)
    # save possibly sudoku specific data
    if is_sudoku:
        # todo: add the visualization here!
        variable_assignment_history = dpll.get_variable_assignment_history()
        map = {}
        for v in variable_assignment_history:
            k = list(v.keys())[0]
            if k not in map:
                map[k] = 1
            else:
                map[k] += 1

                # original_unit_variables = dpll.get_initial_unit_variables()

        vars = [x for x, y in list_a if y]
        vars.sort()
        dim = round((len(dm.get_clauses().values())) ** (1. / 3.))
        sudoku_str = ""
        for i in range(dim):
            for j in range(dim):
                result = [v for v in vars if str(v).startswith(str(i + 1) + str(j + 1))]
                sudoku_str += str(result[0])[2:] + " "
            sudoku_str += "\n"
            with open(output_dir + "/sudoku.txt", 'w') as file:
                file.write(sudoku_str)
    print("Saved results to directory '{}'".format(output_dir))


# usage: python sat_solver.py -S{1,2,3} [dimacs-file-1] [dimacs-file-2] [....]
if __name__ == '__main__':
    args = arg_parser.parse_args()
    if len(args.rest) == 0:
        raise Exception("Please give at least one DIMACS file...")
    if args.S not in dplls:
        raise Exception("DPLL with id '{}' has not been implemented yet.".format(args.S))

    # merge the SATProblems and solve it
    total_problem = __merge_sat_problems__([SATProblem(s) for s in args.rest])
    dpll = dplls[args.S](total_problem)
    satisfied, assignments = dpll.solve()

    print("\nSatisfied: {}".format(satisfied))
    if satisfied:
        # make a printable solution if there is one
        items = list(assignments.items())
        items.sort()
        print("Solution: {}".format([(k, j) for k, j in items if j]))
        output_dir = args.O if args.O else result_dir + strftime("%d_%m_%Y_%H_%M_%S", localtime(time()))
        id = args.ID
        __save_results__(assignments, '--is-sudoku' not in args or args['--is-sudoku'] == 'yes', dpll, output_dir, id)
