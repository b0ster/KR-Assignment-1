from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem


class OneSidedJeroslowWangHeuristic(Heuristic):
    lit_weights = {}

    def name(self) -> str:
        return "1_sided_jw"

    def select(self, problem: SATProblem, var_assignments: {}):
        for v in problem.get_unit_literals():
            if abs(v) not in var_assignments:
                return abs(v), v > 0
        for c in problem.get_clauses().values():
            c_weight = 2 ** -len(c)
            for lit in c:
                if lit in self.lit_weights:
                    self.lit_weights[lit] += c_weight
                else:
                    self.lit_weights[lit] = c_weight
        if len(self.lit_weights):
            l = max(self.lit_weights, key=lambda x: self.lit_weights.get(x) if abs(x) not in var_assignments else 0)
            return abs(l), l > 0
        raise Heuristic.no_var_left_exception
