from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem


class MOMHeuristic(Heuristic):

    def name(self) -> str:
        return "mom"

    def select(self, problem: SATProblem, var_assignments: dict[int, bool]):
        var_counts = {}
        k = 1
        formula = lambda x, y: (x + y) * 2 ** k + x * y
        shortest_clause = min([len(x) for x in problem.get_clauses().values()])
        smallest_clauses = list(filter(lambda x: len(x) == shortest_clause, problem.get_clauses().values()))
        for c in smallest_clauses:
            for lit in c:
                var = abs(lit)
                if var not in var_assignments:
                    if var in var_counts:
                        var_counts[var][lit] += 1
                    else:
                        var_counts[var] = {}
                        var_counts[var][lit] = 1
                        var_counts[var][-lit] = 0
        if len(var_counts):
            l = max(var_counts,
                    key=lambda x: formula(var_counts[x][x],
                                          var_counts[x][-x]))
            return abs(l), var_counts[abs(l)][abs(l)] > var_counts[abs(l)][-abs(l)]
        raise Heuristic.no_var_left_exception
