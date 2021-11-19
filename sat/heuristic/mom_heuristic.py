from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem


class MOMHeuristic(Heuristic):
    var_counts = {}

    def name(self) -> str:
        return "mom"

    def select(self, problem: SATProblem, var_assignments: dict[int, bool]):
        for v in problem.get_unit_literals():
            if abs(v) not in var_assignments:
                return abs(v), v > 0
        k = 1
        formula = lambda x, y: (x + y) * 2 ** k + x * y
        shortest_clause = min([len(x) for x in problem.get_clauses().values()])
        smallest_clauses = list(filter(lambda x: len(x) == shortest_clause, problem.get_clauses().values()))
        for c in smallest_clauses:
            for lit in c:
                var = abs(lit)
                if var in self.var_counts:
                    self.var_counts[var][lit] += 1
                else:
                    self.var_counts[var] = {}
                    self.var_counts[var][lit] = 1
                    self.var_counts[var][-lit] = 0
        if len(self.var_counts):
            l = max(self.var_counts,
                    key=lambda x: formula(self.var_counts[x][x],
                                          self.var_counts[x][-x]) if x not in var_assignments else 0)
            return abs(l), self.var_counts[abs(l)][abs(l)] > self.var_counts[abs(l)][-abs(l)]
        raise Heuristic.no_var_left_exception
