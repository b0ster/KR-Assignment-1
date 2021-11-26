import argparse
# import math
import math
import os
import csv
# from typing import tuple, list
from typing import Any

from sat.dpll import DPLL
from sat.heuristic.heuristic import Heuristic
from sat.heuristic.length_priority_heuristic import LengthPriorityHeuristic
from sat.heuristic.min_occurances_heuristic import MinOccurrencesHeuristic
from sat.heuristic.one_sided_jeroslow_wang_heuristic import OneSidedJeroslowWangHeuristic
from sat.heuristic.mom_heuristic import MOMHeuristic
from sat.heuristic.two_sided_jeroslow_wang_heuristic import TwoSidedJeroslowWangHeuristic
from util.sat_problem import SATProblem

from util.visualizer import Visualizer

dplls = {
    "1": lambda p: DPLL(p, heuristic=Heuristic()),
    "2": lambda p: DPLL(p, heuristic=MOMHeuristic()),
    "3": lambda p: DPLL(p, heuristic=OneSidedJeroslowWangHeuristic()),
    "4": lambda p: DPLL(p, heuristic=TwoSidedJeroslowWangHeuristic()),
    "5": lambda p: DPLL(p, heuristic=LengthPriorityHeuristic()),
    "6": lambda p: DPLL(p, heuristic=MinOccurrencesHeuristic())
    # todo: add more DPLLs with heuristics here
}

# these are the arguments available
arg_parser = argparse.ArgumentParser(description="SAT solve using DPLL")
arg_parser.add_argument('-S', choices=list(dplls.keys()), default="1", required=True, help='SAT version')
arg_parser.add_argument('--is-sudoku', choices=['yes', 'no'], default='yes', help='If the target problem is a sudoku')
arg_parser.add_argument('-O', help='Output folder for results (default current directory)')
arg_parser.add_argument('-V', choices=["yes", "no"], help='Enable visualization (currently only when --is-sudoku=yes)')
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


def __save_results__(assignments: dict[int, bool], dpll: DPLL, output_dir: str,
                     id: object = None) -> None:
    """
    Saves the results of the SAT solving to disk.
    :param assignments: assignments of all variables.
    """
    # save model to DIMACS format
    list_a = sorted(assignments.items(), key=lambda _x: abs(_x[0]))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    dm = SATProblem()

    for x, y in list_a:
        if y:
            dm.add_clause(([abs(x)]))
        else:
            dm.add_clause([-abs(x)])
    out_name = output_dir + "/" + str(id) + ".out"
    print("Saving result to {}".format(out_name))
    dm.save_to_file_dimacs("sat_result", out_name)

    # save the stats
    stats = dpll.get_stats_map()
    stats["id"] = id
    stats_name = output_dir + "/" + str(id) + "-stats.csv"
    with open(stats_name, 'w') as stats_csv:
        print("Writing stats to {}".format(stats_name))
        keys = list(stats.keys())
        keys.sort()
        writer = csv.DictWriter(stats_csv, fieldnames=keys)
        writer.writeheader()
        writer.writerow(stats)


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
    init_vars = dpll.get_initial_unit_variables()
    var_history = dpll.get_variable_assignment_history()

    print("\nSatisfied: {}".format(satisfied))
    if satisfied:
        # make a printable solution if there is one
        items = list(assignments.items())
        items.sort()
        print("Solution: {}".format([(k, j) for k, j in items if j]))
        output_dir = args.O if args.O else '.'
        id = args.ID or args.rest[0]
        is_sudoku = '--is-sudoku' not in args or args['--is-sudoku'] == 'yes'
        __save_results__(assignments, dpll, output_dir, id)
        if args.V == 'yes' and is_sudoku and round((len(assignments) ** (1 / 3))) == 9:
            dir = 'plots/sudoku_9x9_' + args.S + '/'
            print("Saving visualizations to {}".format(dir))
            vis = Visualizer(init_vars, var_history, out_path=dir)
            vis.run_images()
        print("Done.")
