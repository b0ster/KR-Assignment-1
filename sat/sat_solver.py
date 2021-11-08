from util.dimacs import DIMACS
import copy


class SatSolver:
    @staticmethod
    def assert_is_dimacs(x):
        if x is None or not isinstance(x, DIMACS):
            raise Exception("Type must be DIMACS.")

    def __init__(self, rules, heuristics=None) -> None:
        self.assert_is_dimacs(rules)
        self.rules = rules
        self.heuristics = heuristics
        pass

    @staticmethod
    def is_satisfied(problem):
        if len(problem.get_clauses()) == 0:
            return True
        if len(list(filter(lambda x: len(x) == 0, problem.get_clauses()))) > 0:
            return False
        return None

    @staticmethod
    def choose_next_var(vars, var_assignments) -> int:
        # todo: determine here to use heuristics
        for v in vars:
            if abs(v) not in var_assignments.keys():
                return abs(v)

        return -1

    def solve(self, problem, vars, var_assignments) -> tuple:
        self.assert_is_dimacs(problem)
        satisfied = self.is_satisfied(problem)
        if satisfied is not None:
            return satisfied, var_assignments

        previous_clauses = copy.deepcopy(problem.get_clauses())
        non_assigned_var = self.choose_next_var(vars, var_assignments)
        if non_assigned_var == -1:
            return False, var_assignments
        var_assignments[non_assigned_var] = False
        problem.remove_clause_containing(-non_assigned_var)
        problem.remove_literal_from_clauses(non_assigned_var)
        satisfied, var_assignments = self.solve(problem, vars, var_assignments)
        if satisfied:
            return satisfied, var_assignments

        problem.set_clauses(previous_clauses)
        var_assignments[non_assigned_var] = True
        problem.remove_clause_containing(non_assigned_var)
        problem.remove_literal_from_clauses(-non_assigned_var)
        return self.solve(problem, vars, var_assignments)
