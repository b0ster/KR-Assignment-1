import math

from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem


class MinOccurrencesHeuristic(Heuristic):
    previous_occurrences = {}

    def name(self) -> str:
        return "weighted_occurrences"

    def select(self, problem: SATProblem, var_assignments: dict[int, bool]):
        for c in problem.get_clauses().values():
            for lit in c:
                if lit not in self.previous_occurrences:
                    self.previous_occurrences[lit] = 1
                else:
                    self.previous_occurrences[lit] += 1
        l = min(self.previous_occurrences,
                key=lambda x: self.previous_occurrences[x] if abs(x) not in var_assignments else math.inf)
        return abs(l), l > 0
