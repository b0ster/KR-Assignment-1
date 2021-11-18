# from typing import List, Tuple, Dict

from sat.heuristic.heuristic import Heuristic
from util.sat_problem import SATProblem
import copy
from time import time


class DPLL:

    def __init__(self, problem: SATProblem, heuristic: Heuristic = Heuristic()) -> None:
        self.problem = problem
        self.heuristic = heuristic
        self.num_evaluations = 0
        self.num_backtracking = 0
        self.variable_history: list[tuple[int, bool]] = []
        self.initial_unit_variables = problem.get_unit_variables()
        self.stats: dict[str, object] = {}
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
        for c in problem.get_clauses().values():
            if len(c) == 0:
                return False
        # if nothing is violated and there are still clauses, then we must reason further
        return None

    def __choose_next_var__(self, problem: SATProblem, var_assignments: dict[int, bool]) -> tuple[int, bool]:
        """
        Selects a new variable and a starting value based on given heuristics.
        :param problem: a SATProblem instance.
        :param var_assignments: tuple of currently assigned vars {111: True, 121: False, 122, False, ...}.
        :return: a new variable with a starting value to try.
        """
        return self.heuristic.select(problem, var_assignments)

    def __print_progress__(self, problem: SATProblem, var_assignments: dict[int, bool]) -> None:
        """
        Prints the current progress of the DPLL algorithm.
        :param problem: a SATProblem instance.
        :param var_assignments: the currently assigned variables.
        """
        n = self.num_evaluations
        c = len(problem.clauses.keys())
        v = len(var_assignments.keys())
        va = len(problem.get_all_variables())
        b = self.num_backtracking
        msg = "\rDPLL: evaluation #{}, backtrackings #{}, left clauses #{}, assigned vars {}/{}".format(n,b, c, v, va)
        print(msg, flush=True, end='')

    def __solve__(self, var_assignments: dict[int, bool]) -> tuple[bool, dict[int, bool]]:
        """
        Solves the SATProblem using a DPLL-procedure recursively.
        :param var_assignments: the currently assigned vars, needed to choose a new one.
        :return: a Tuple with a boolean representing the satisfiability, and a list of tuple of variable assignments.
        """
        self.num_evaluations += 1
        self.__print_progress__(self.problem, var_assignments)

        satisfied = DPLL.__is_satisfied__(self.problem)
        if satisfied is not None:
            return satisfied, var_assignments

        # deepcopy the state as this method is recursive
        # previous_clauses = copy.deepcopy(self.problem.get_clauses())
        copy_assign = copy.copy(var_assignments)
        counter = copy.copy(self.problem.state_counter)

        # find a variable and a starting value
        non_assigned_var, init_value = self.__choose_next_var__(self.problem, var_assignments)
        self.variable_history.append((non_assigned_var, init_value))
        var_assignments[non_assigned_var] = init_value

        self.problem.solve_literal(non_assigned_var if init_value else -non_assigned_var)

        satisfied, var_assignments = self.__solve__(var_assignments)
        if satisfied:
            del self.problem.previous_clauses[counter]
            return satisfied, var_assignments

        self.num_backtracking += 1
        self.variable_history.append((non_assigned_var, not init_value))
        # try the opposite of the init value
        self.problem.set_clauses(self.problem.get_previous_clauses(counter))
        copy_assign[non_assigned_var] = not init_value

        # CNF, so any truth value makes the statement true
        self.problem.solve_literal(non_assigned_var if not init_value else -non_assigned_var)

        return self.__solve__(copy_assign)

    def solve(self) -> tuple[bool, dict[int, bool]]:
        """
         Solves the SATProblem using a DPLL-procedure.
         :return: a Tuple with a boolean representing the satisfiability, and a Tuple of variable assignments.
        """
        print("Running DPLL with heuristic [{}]".format(self.heuristic.name()))
        self.stats["heuristic"] = self.heuristic.name()
        self.stats["n_initial_unit_variables"] = len(self.problem.get_unit_variables())
        self.stats["n_variables"] = len(self.problem.get_all_variables())
        self.stats["n_clauses"] = len(self.problem.get_clauses().keys())
        self.stats["n_literals"] = len(self.problem.get_all_literals())
        self.stats["time_start"] = time()
        result = self.__solve__({})
        self.stats["n_evaluations"] = self.num_evaluations
        self.stats["n_backtracking"] = self.num_backtracking
        self.stats["time_end"] = time()
        return result

    def get_stats_map(self) -> dict[str, object]:
        """
        Gets a map with tracked statistics.
        :return: map with tracked statistics.
        """
        return self.stats

    def get_variable_assignment_history(self) -> list[tuple[int, bool]]:
        """
        Gets a list of variable assignments that has been tried.
        [{111: True}, {122: False}, {111:False}, ..., {..}]
        :return: list of tuples in assignment order, first one is the first variable tried.
        """
        return self.variable_history

    def get_initial_unit_variables(self) -> list[int]:
        """
        Gets a list of unit variables before the solving had began.
        :return: list of initial unit variables.
        """
        return self.initial_unit_variables
