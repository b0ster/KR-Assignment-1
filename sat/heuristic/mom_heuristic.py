from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem


class MOMHeuristic(Heuristic):

    def name(self) -> str:
        return "mom"

    def select(self, problem: SATProblem, var_assignments: {}):
        for v in problem.get_unit_variables():
            if v not in var_assignments.keys():
                return abs(v), False
        k = 1
        formula = lambda x, y: (x + y) * 2 ** k + x * y
        shortest_clause = min([len(x) for x in problem.get_clauses().values()])
        smallest_clauses = list(filter(lambda x: len(x) == shortest_clause, problem.get_clauses().values()))
        var_counts = {}
        for c in smallest_clauses:
            for lit in c:
                var = abs(lit)
                if var in var_counts:
                    var_counts[var][lit] += 1
                else:
                    var_counts[var] = {}
                    var_counts[var][lit] = 1
                    var_counts[var][-lit] = 0
        vc_list = sorted(var_counts.items(), key=lambda x: formula(x[1][x[0]], x[1][-x[0]]), reverse=True)
        for i in vc_list:
            if i[0] not in var_assignments.keys():
                return i[0], i[1][i[0]] > i[1][-i[0]]
        raise Heuristic.no_var_left_exception
