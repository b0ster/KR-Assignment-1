from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem


class OneSidedJeroslowWangHeuristic(Heuristic):

    def name(self) -> str:
        return "1_sided_jw"

    def select(self, problem: SATProblem, var_assignments: dict[int, bool]):
        lit_weights = {}
        for c in problem.get_clauses().values():
            c_weight = 2 ** -len(c)
            for lit in c:
                if abs(lit) not in var_assignments:
                    if lit in lit_weights:
                        lit_weights[lit] += c_weight
                    else:
                        lit_weights[lit] = c_weight
        if len(lit_weights):
            l = max(lit_weights, key=lambda x: lit_weights.get(x))
            return abs(l), l > 0
        raise Heuristic.no_var_left_exception
