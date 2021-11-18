from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem


class TwoSidedJeroslowWangHeuristic(Heuristic):
    var_counts = {}

    def name(self) -> str:
        return "2_sided_jw"

    def select(self, problem: SATProblem, var_assignments: dict[int, bool]):
        for v in problem.get_unit_literals():
            if abs(v) not in var_assignments:
                return abs(v), v > 0
        for c in problem.get_clauses().values():
            c_weight = 2 ** -len(c)
            for lit in c:
                var = abs(lit)
                if var in self.var_counts:
                    self.var_counts[var][lit] += c_weight
                else:
                    self.var_counts[var] = {}
                    self.var_counts[var][lit] = c_weight
                    self.var_counts[var][-lit] = 0
        if len(self.var_counts):
            l = max(self.var_counts, key=lambda x: sum(self.var_counts[x].values()) if x not in var_assignments else 0)
            return abs(l), max(self.var_counts[l], key=self.var_counts[abs(l)].get) > 0
        raise Heuristic.no_var_left_exception
