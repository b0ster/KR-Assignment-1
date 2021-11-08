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
        # check if all clauses are solved currently, then a model has been found
        if len(problem.get_clauses()) == 0:
            return True
        # check if there are empty clauses, then the rules are violated
        if len(list(filter(lambda x: len(x) == 0, problem.get_clauses()))) > 0:
            return False
        # if nothing is violated and there are still clauses, then we must reason further
        return None

    @staticmethod
    def choose_next_var(vars, var_assignments) -> int:
        # todo: determine here to use heuristics
        for v in vars:
            # search for a non-used parameter to be assigned
            if abs(v) not in var_assignments.keys():
                return abs(v)

        raise Exception("No new variables to assign.")

    def solve(self, problem, vars, var_assignments) -> tuple:
        self.assert_is_dimacs(problem)
        satisfied = self.is_satisfied(problem)
        if satisfied is not None:
            return satisfied, var_assignments

        # deepcopy the the state as this method is recursive
        previous_clauses = copy.deepcopy(problem.get_clauses())
        copy_vars = copy.deepcopy(vars)
        copy_assign = copy.deepcopy(var_assignments)

        # find a variable
        non_assigned_var = self.choose_next_var(vars, var_assignments)
        # first, assign it with False, if that is not working, later on True will be assigned
        var_assignments[non_assigned_var] = False

        # CNF, so any truth value makes the statement true
        problem.remove_clause_containing(-non_assigned_var)

        # Removes the opposite from other clauses
        problem.remove_literal_from_clauses(non_assigned_var)
        satisfied, var_assignments = self.solve(problem, vars, var_assignments)
        if satisfied:
            return satisfied, var_assignments

        # if false does not satisfy, we must start assigning True values
        problem.set_clauses(previous_clauses)
        copy_assign[non_assigned_var] = True

        # CNF, so any truth value makes the statement true
        problem.remove_clause_containing(non_assigned_var)

        # Removes the opposite from other clauses
        problem.remove_literal_from_clauses(-non_assigned_var)
        return self.solve(problem, copy_vars, copy_assign)
