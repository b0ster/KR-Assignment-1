from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem


class LengthPriorityHeuristic(Heuristic):

    def name(self) -> str:
        return "length_priority_max"

    def select(self, problem: SATProblem, var_assignments: {}):
        for v in problem.get_unit_variables():
            if v not in var_assignments.keys():
                return abs(v), False
        lit_lengths = {}
        for c in problem.get_clauses().values():
            for lit in c:
                if lit in lit_lengths:
                    if 1 / len(c) > lit_lengths[lit]:
                        lit_lengths[lit] = 1 / len(c)
                else:
                    lit_lengths[lit] = 1 / len(c)
        if len(lit_lengths):
            l = max(lit_lengths, key=lit_lengths.get)
            return abs(l), l > 0
        raise Heuristic.no_var_left_exception
