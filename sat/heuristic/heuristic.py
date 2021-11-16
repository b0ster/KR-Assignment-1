import abc

from util.sat_problem import SATProblem


class Heuristic:
    no_var_left_exception = Exception("No variables left to assign.")

    def __init__(self) -> None:
        pass

    def name(self) -> str:
        return "default_dpll"

    def select(self, problem: SATProblem, var_assignments: {}):
        for v in problem.get_unit_variables():
            if v not in var_assignments.keys():
                return abs(v), False
        for v in problem.get_all_variables():
            if v not in var_assignments.keys():
                return abs(v), False
        raise Heuristic.no_var_left_exception
