from sat.heuristic.heuristic import Heuristic
from util.satproblem import SATProblem


class DPLLImprovedHeuristic(Heuristic):

    def select(self, problem: SATProblem, var_assignments: {}):
        for v in problem.get_unit_variables():
            if v not in var_assignments.keys():
                return abs(v), False
        for v in problem.get_all_variables():
            if v not in var_assignments.keys():
                return abs(v), False
        raise Heuristic.no_var_left_exception
