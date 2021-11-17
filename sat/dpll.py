from typing import List, Tuple

from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem
import copy


class DPLL:

    def __init__(self, problem: SATProblem, heuristic: Heuristic = Heuristic) -> None:
        self.problem = problem
        self.heuristic = heuristic
        self.num_evaluations = 0
        self.variable_history = []
        self.initial_unit_variables = problem.get_unit_variables()
        pass

    @staticmethod
    def __is_satisfied__(problem: SATProblem):
        """
        Checks whether the given problem is satisfied.
        :param problem: a SATProblem instance.
        :return: None if still not satisfied (more evaluations required), True if satisfied, False if non-satisfied.
        """
        # check if all clauses are solved currently, then a model has been found
        if len(problem.get_clauses().keys()) == 0:
            return True
        # check if there are empty clauses, then the rules are violated
        if len(list(filter(lambda x: len(x) == 0, problem.get_clauses().values()))) > 0:
            return False
        # if nothing is violated and there are still clauses, then we must reason further
        return None

    def __choose_next_var__(self, problem: SATProblem, var_assignments: {}) -> Tuple[int, bool]:
        """
        Selects a new variable and a starting value based on given heuristics.
        :param problem: a SATProblem instance.
        :param var_assignments: tuple of currently assigned vars {111: True, 121: False, 122, False, ...}.
        :return: a new variable with a starting value to try.
        """
        return self.heuristic.select(problem, var_assignments)

    def __print_progress__(self, problem: SATProblem, var_assignments: Tuple[int, bool]) -> None:
        """
        Prints the current progress of the DPLL algorithm.
        :param problem: a SATProblem instance.
        :param var_assignments: the currently assigned variables.
        """
        n = self.num_evaluations
        c = len(problem.clauses.keys())
        v = len(var_assignments.keys())
        va = len(problem.get_all_variables())
        print("\rDPLL: evaluation #{}, left clauses #{}, assigned vars {}/{}".format(n, c, v, va), flush=True, end='')

    def solve(self, var_assignments: {}) -> Tuple[bool, Tuple[int, bool]]:
        """
        Solved the SATProblem using a DPLL-procedure recursively.
        :param var_assignments: the currently assigned vars, needed to choose a new one.
        :return: a Tuple with a boolean representing the satisfiability, and a Tuple of variable assignments.
        """
        self.num_evaluations += 1
        self.__print_progress__(self.problem, var_assignments)

        satisfied = DPLL.__is_satisfied__(self.problem)
        if satisfied is not None:
            return satisfied, var_assignments

        # deepcopy the the state as this method is recursive
        previous_clauses = copy.deepcopy(self.problem.get_clauses())
        copy_assign = copy.deepcopy(var_assignments)

        # find a variable and a starting value
        non_assigned_var, init_value = self.__choose_next_var__(self.problem, var_assignments)
        self.variable_history.append((non_assigned_var, init_value))
        var_assignments[non_assigned_var] = init_value

        # CNF, so any truth value makes the statement true
        self.problem.remove_clause_containing(non_assigned_var if init_value else -non_assigned_var)

        # Removes the opposite from other clauses
        self.problem.remove_literal_from_clauses(non_assigned_var if not init_value else -non_assigned_var)
        satisfied, var_assignments = self.solve(var_assignments)
        if satisfied:
            return satisfied, var_assignments

        self.variable_history.append((non_assigned_var, not init_value))
        # try the opposite of the init value
        self.problem.set_clauses(previous_clauses)
        copy_assign[non_assigned_var] = not init_value

        # CNF, so any truth value makes the statement true
        self.problem.remove_clause_containing(non_assigned_var if not init_value else -non_assigned_var)

        # Removes the opposite from other clauses
        self.problem.remove_literal_from_clauses(non_assigned_var if init_value else -non_assigned_var)
        return self.solve(copy_assign)

    def get_variable_assignment_history(self) -> List[tuple]:
        """
        Gets a list of variable assignments that has been tried.
        [(111, True), (122, False), (111, False), ..., (..)]
        :return: list of tuples in assignment order, first one is the first variable tried.
        """
        return self.variable_history

    def get_initial_unit_variables(self) -> List[int]:
        """
        Gets a list of unit variables before the solving had began.
        :return: list of initial unit variables.
        """
        return self.initial_unit_variables
