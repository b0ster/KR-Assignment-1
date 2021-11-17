from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem


class TwoSidedJeroslowWangHeuristic(Heuristic):

    def name(self) -> str:
        return "2_sided_jw"

    def select(self, problem: SATProblem, var_assignments: {}):
        for v in problem.get_unit_literals():
            if abs(v) not in var_assignments.keys():
                return abs(v), v > 0
        var_counts = {}
        for c in problem.get_clauses().values():
            c_weight = 2 ** -len(c)
            for lit in c:
                var = abs(lit)
                if var in var_counts:
                    var_counts[var][lit] += c_weight
                else:
                    var_counts[var] = {}
                    var_counts[var][lit] = c_weight
                    var_counts[var][-lit] = 0
        if len(var_counts):
            l = max(var_counts, key=lambda x: sum(var_counts.get(x)))
            return abs(l), max(var_counts[l], key=var_counts[l].get) > 0
        raise Heuristic.no_var_left_exception
