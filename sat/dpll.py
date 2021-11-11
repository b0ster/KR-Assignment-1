from util.dimacs import DIMACS
import copy


class DPLL:
    heuristic_unit_class_prioritize = "unit_clause_prioritize"

    def __init__(self, heuristics=None) -> None:
        self.heuristics = heuristics
        self.num_evaluations = 0
        pass

    @staticmethod
    def is_satisfied(problem: DIMACS):
        # check if all clauses are solved currently, then a model has been found
        if len(problem.get_clauses().keys()) == 0:
            return True
        # check if there are empty clauses, then the rules are violated
        if len(list(filter(lambda x: len(x) == 0, problem.get_clauses().values()))) > 0:
            return False
        # if nothing is violated and there are still clauses, then we must reason further
        return None

    def choose_next_var(self, problem: DIMACS, var_assignments: {}) -> int:
        if self.heuristics is None:
            for v in problem.get_all_variables():
                # search for a non-used parameter to be assigned
                if abs(v) not in var_assignments.keys():
                    return abs(v)
        elif self.heuristics == DPLL.heuristic_unit_class_prioritize:
            for v in problem.get_unit_variables():
                # search for a non-used parameter to be assigned
                if abs(v) not in var_assignments.keys():
                    return abs(v)
            for v in problem.get_all_variables():
                # search for a non-used parameter to be assigned
                if abs(v) not in var_assignments.keys():
                    return abs(v)

        raise Exception("No new variables to assign.")

    def solve(self, problem: DIMACS, var_assignments: {}) -> {}:
        self.num_evaluations += 1
        print("DPLL: evaluation #{}, left clauses #{}, assigned vars #{}".format(self.num_evaluations,
                                                                                 len(problem.clauses.keys()),
                                                                                 len(var_assignments.keys())))
        satisfied = self.is_satisfied(problem)
        if satisfied is not None:
            return satisfied, var_assignments

        # deepcopy the the state as this method is recursive
        previous_clauses = copy.deepcopy(problem.get_clauses())
        copy_assign = copy.deepcopy(var_assignments)

        # find a variable
        non_assigned_var = self.choose_next_var(problem, var_assignments)
        # first, assign it with False, if that is not working, later on True will be assigned
        var_assignments[non_assigned_var] = False

        # CNF, so any truth value makes the statement true
        problem.remove_clause_containing(-non_assigned_var)

        # Removes the opposite from other clauses
        problem.remove_literal_from_clauses(non_assigned_var)
        satisfied, var_assignments = self.solve(problem, var_assignments)
        if satisfied:
            return satisfied, var_assignments

        # if false does not satisfy, we must start assigning True values
        problem.set_clauses(previous_clauses)
        copy_assign[non_assigned_var] = True

        # CNF, so any truth value makes the statement true
        problem.remove_clause_containing(non_assigned_var)

        # Removes the opposite from other clauses
        problem.remove_literal_from_clauses(-non_assigned_var)
        return self.solve(problem, copy_assign)
