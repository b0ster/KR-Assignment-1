from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem


class OneSidedJeroslowWangHeuristic(Heuristic):

    def select(self, problem: SATProblem, var_assignments: {}):
        for v in problem.get_unit_variables():
            if v not in var_assignments.keys():
                return abs(v), False
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
        vc_list = sorted(var_counts.items(), key=lambda x: max(x[1][x[0]], x[1][-x[0]]), reverse=True)
        for i in vc_list:
            if i[0] not in var_assignments.keys():
                return i[0], i[1][i[0]] > i[1][-i[0]]
        raise Heuristic.no_var_left_exception
