from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem


class TwoSidedJeroslowWangHeuristic(Heuristic):

    def name(self) -> str:
        return "2_sided_jw"

    def select(self, problem: SATProblem, var_assignments: dict[int, bool]) -> tuple[int, bool]:
        var_counts: dict[int, dict[int, int]] = {}
        for c in problem.get_clauses().values():
            c_weight = 2 ** -len(c)
            for lit in c:
                var = abs(lit)
                if var not in var_assignments:
                    if var in var_counts:
                        var_counts[var][lit] += c_weight
                    else:
                        var_counts[var] = {}
                        var_counts[var][lit] = c_weight
                        var_counts[var][-lit] = 0
        if len(var_counts):
            l = max(var_counts, key=lambda x: sum(var_counts[x].values()))
            return (abs(l), (max(var_counts[l], key=var_counts[abs(l)].get) > 0))
        raise Heuristic.no_var_left_exception
