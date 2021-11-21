# from typing import List, Tuple, Dict

class SATState:
    def __init__(self, clause_list: list[list[int]], assigned_vars: dict[int, bool]) -> None:
        self.clause_list: list[list[int]] = clause_list
        self.assigned_variables: dict[int, bool] = assigned_vars

        # make a set of all unassigned variables
        self.unassigned_variables: set[int] = set()
        for clause in clause_list:
            # get all the unique variables in the clause
            vars: set[int] = set(map(lambda x: abs(x), clause))
            if len(vars) > 0:
                # iterate through the variables if there are any
                for var in vars:
                    # check if the variable has been assigned
                    if var in self.assigned_variables.keys():
                        # skip this variable
                        continue
                    # not assigned, so add to set
                    self.unassigned_variables.add(var)


class DPLL_Loic:
    def __init__(self, clause_list: list[list[int]], init_vars: dict[int, bool]) -> None:
        # initial variable assignments
        self.init_vars: dict[int, bool] = init_vars
        # history of the problem states (for backtracking)
        self.state_history: list[SATState] = [SATState(clause_list, init_vars)]
        # current problem state
        self.current_state: SATState = self.state_history[0]
        # number of evaluations
        self.num_eval: int = 0
        # number of backtracks
        self.num_backtrack: int = 0

    def __print_progress__(self) -> None:
        """
        Prints the current progress of the DPLL algorithm.
        :param problem: a SATProblem instance.
        :param var_assignments: the currently assigned variables.
        """
        n = self.num_eval
        c = len(self.current_state.clause_list)
        v = len(self.current_state.assigned_variables)
        va = v + len(self.current_state.unassigned_variables)
        b = self.num_backtrack
        i = len(self.init_vars)
        msg = "\rDPLL: evaluation #{}, backtrackings #{}, left clauses #{}, assigned vars {}/{} (initial vars: {})".format(n,b, c, v, va, i)
        print(msg, flush=True, end='')

    def solve(self) -> bool:
        self.__print_progress__()

        # increment the number of evaluations
        self.num_eval += 1

        # check if there are any paths left to discover
        if len(self.state_history) == 0:
            # no paths left to discover to satisfy CNF
            return False
        
        self.current_state: SATState = self.state_history[-1]

        # check if the clause list is empty
        if len(self.current_state.clause_list) == 0:
            # empty clause list means CNF is satisfied
            return True
        
        # any empty clause in list -> unsatisfiable
        for clause in self.current_state.clause_list:
            if len(clause) == 0:
                # empty clause means CNF is not satisfied
                # backtrack one evaluation and try again
                self.num_backtrack += 1
                self.state_history = self.state_history[:-1]
                return self.solve()

        # check for tautologies
        # iterate over a copy of the list so we can delete elements
        for clause in list(self.current_state.clause_list):
            # get all the literals in the clause as unique absolute values
            literals: set[int] = set(map(lambda x: abs(x), clause))
            for lit in literals:
                # if it occurs as positive and negative, the clause can be removed
                if lit in clause and -lit in clause:
                    self.current_state.clause_list.remove(clause)

        # check for unit clauses
        for clause in self.current_state.clause_list:
            # unit clauses will have a lenght of one
            if len(clause) == 1:
                # get the value of the unit clause
                unit_var: int = clause[0]
                if unit_var > 0:
                    # if it's positive, assign it to true
                    if not self.assign_var(unit_var, True):
                        # try assigning it and see if this assignment has been done before
                        # if it has, raise an exception
                        # raise Exception("Cannot assign unit clause, assignment has already been tried")
                        pass
                    # then move on to the next evaluation
                    return self.solve()
                elif unit_var < 0:
                    # if it's negative, assign it to false
                    if not self.assign_var(abs(unit_var), False):
                        # try assigning it and see if this assignment has been done before
                        # if it has, raise an exception
                        # raise Exception("Cannot assign unit clause, assignment has already been tried")
                        pass
                    # then move on to the next evaluation
                    return self.solve()
                else:
                    raise Exception("Something went wrong with unit clauses")

        # remove clauses that evaluate to true
        for clause in list(self.current_state.clause_list):
            for lit in clause:
                if abs(lit) in self.current_state.assigned_variables:
                    if (lit > 0 and self.current_state.assigned_variables[lit]) or (lit < 0 and not self.current_state.assigned_variables[abs(lit)]):
                        self.current_state.clause_list.remove(clause)
                        break

        # now we can pick a variable to assign
        self.choose_var()

        return self.solve()

    def assign_var(self, var: int, value: bool) -> bool:
        # create a new state that is a copy of the current state
        new_state: SATState = SATState(self.current_state.clause_list, self.current_state.assigned_variables)
        # assign the variable
        new_state.assigned_variables[var] = value
        
        # cycle through all the previous states (except for the initial state and the current state)
        for state in self.state_history[1:-1]:
            # check if there has been a state with the same assignments
            if new_state.assigned_variables == state.assigned_variables:
                # # if there has, revert to the previous assignments
                # self.current_state.assigned_variables = previous_assignments

                # if there has, return false
                return False
        # these assignments haven't been tried before

        # now also remove the variable from unassigned variables (if it is in there)
        new_state.unassigned_variables.discard(var)

        # now add the new state to the state history
        self.state_history.append(new_state)

        return True

    def choose_var(self) -> None:
        # check if there are no variables left to assign
        if len(self.current_state.unassigned_variables) == 0:
            # raise an exception if this happens
            raise Exception("No variables left to assign")
        
        # iterate through all unassigned variables
        for var in self.current_state.unassigned_variables:
            # try assigning to true
            if self.assign_var(var, True):
                # combination has not been tried, so return
                return
            # try assigning to false
            elif self.assign_var(var, False):
                # combination has not been tried, so return
                return

        # no combination found that has not been tried before
        raise Exception("No new variable assignment found that has not been tried before")



        