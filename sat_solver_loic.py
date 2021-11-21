from typing import Optional

from sat.dpll_loic import DPLL_Loic

import sys
x=10000
sys.setrecursionlimit(x)

class SATProblem_Loic:
    """
        Reads DIMACS format from a file, and puts the clauses into memory
    """

    def __init__(self, file: Optional[str] = None, file_type: str = 'DIMACS') -> None:
        if file_type != 'DIMACS':
            raise Exception("Only DIMACS files are supported currently.")
        self.clauses: dict[str, list[int]] = {}
        # self.state_counter: int = 0
        # self.previous_clauses: dict[int, dict[str, list[int]]] = {}
        # self.literal_indices: dict[int, list[str]] = {}
        self.init_vars: dict[int, bool] = dict()
        if file is not None:
            with open(file, 'r') as f:
                lines = f.readlines()
                for l in lines:
                    if not l.startswith("c") and not l.startswith("p"):
                        split_l = l.split(" ")
                        clause = split_l[:-1]
                        clause = list(map(lambda x: int(x), clause))
                        self.add_clause(clause)

    def add_clause(self, clause: list[int]) -> None:
        clause_idx = ''.join(str(e) + "_" for e in sorted(clause))
        # ignore duplicate clauses
        if clause_idx not in self.clauses:
            self.clauses[clause_idx] = clause
            if len(clause) == 1:
                lit: int = clause[0]
                if lit > 0:
                    self.init_vars[lit] = True
                elif lit < 0:
                    self.init_vars[abs(lit)] = False


            # for lit in clause:
            #     if lit in self.literal_indices:
            #         self.literal_indices[lit].append(clause_idx)
            #     else:
            #         self.literal_indices[lit] = [clause_idx]

    def get_clauses(self) -> list[list[int]]:
        return list(self.clauses.values())

    def get_init_vars(self) -> dict[int, bool]:
        return self.init_vars

def merge_sat_problems(sp: list[SATProblem_Loic]) -> SATProblem_Loic:
    """
    Merges a list of SATProblem into one single problem.
    :param sp: List of SATProblem instances.
    :return: a merged combined SATProblem.
    """
    total_problem = SATProblem_Loic()
    # merge the different DIMACS files as this is a CNF
    for problem in sp:
        for c in problem.get_clauses():
            total_problem.add_clause(c)
    return total_problem



if __name__ == '__main__':
    rules: SATProblem_Loic = SATProblem_Loic("data/rules/sudoku-rules-9x9.txt")
    problem: SATProblem_Loic = merge_sat_problems([rules, SATProblem_Loic("data/sudoku/dimacs/9x9/sudoku-9x9-1.txt")])

    dpll: DPLL_Loic = DPLL_Loic(problem.get_clauses(), problem.get_init_vars())
    dpll.solve()
