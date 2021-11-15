<<<<<<< HEAD:util/dimacs.py
<<<<<<< HEAD
class DIMACS:
    """
        Reads DIMACS format from a file, and puts the clauses into memory
    """

    def __init__(self, file: str = None) -> None:
        self.clauses = {}
        self.literal_indices = {}
        if file is not None:
            with open(file, 'r') as f:
                lines = f.readlines()
                for l in lines:
                    if not l.startswith("c") and not l.startswith("p"):
                        split_l = l.split(" ")
                        clause = split_l[:-1]
                        clause = list(map(lambda x: int(x), clause))
                        self.add_clause(clause)

    def set_clauses(self, clauses: dict(int, list(int))) -> None:
        self.clauses = clauses

    def get_clauses(self) -> dict(int, list(int)):
        return self.clauses

    def add_clause(self, clause: list(int)) -> None:
        clause.sort()
        clause_idx = ''.join(str(e) + "_" for e in clause)
        # ignore duplicate clauses
        if clause_idx not in self.clauses:
            self.clauses[clause_idx] = clause
            for lit in clause:
                if lit in self.literal_indices:
                    self.literal_indices[lit].append(clause_idx)
                else:
                    self.literal_indices[lit] = [clause_idx]

    def remove_clause_containing(self, literal: int) -> None:
        for c_idx in self.literal_indices[literal]:
            if c_idx in self.clauses:
                del self.clauses[c_idx]

    def remove_literal_from_clauses(self, literal: int) -> None:
        if literal in self.literal_indices:
            for c_idx in self.literal_indices[literal]:
                if c_idx in self.clauses:
                    self.clauses[c_idx].remove(literal)
        if -literal in self.literal_indices:
            for c_idx in self.literal_indices[-literal]:
                if c_idx in self.clauses:
                    self.clauses[c_idx].remove(-literal)

    @staticmethod
    def is_unit_clause(clause: list(int)) -> bool:
        return len(clause) == 1

    def get_unit_clauses(self) -> list(list(int)):
        return list(filter(lambda x: self.is_unit_clause(x), self.clauses.values()))

    def get_all_variables(self) -> list(int):
        return list(set((map(lambda x: abs(x), self.get_all_literals()))))

    def get_all_literals(self) -> list(int):
        return self.literal_indices.keys()

    @staticmethod
    def literal_is_negated(literal: int) -> bool:
        return literal < 0
=======
class DIMACS:
=======
from typing import List, Tuple


class SATProblem:
>>>>>>> master:util/sat_problem.py
    """
        Reads DIMACS format from a file, and puts the clauses into memory
    """

    def __init__(self, file: str = None, file_type: str = 'DIMACS') -> None:
        if file_type != 'DIMACS':
            raise Exception("Only DIMACS files are supported currently.")
        self.clauses = {}
        self.literal_indices = {}
        if file is not None:
            with open(file, 'r') as f:
                lines = f.readlines()
                for l in lines:
                    if not l.startswith("c") and not l.startswith("p"):
                        split_l = l.split(" ")
                        clause = split_l[:-1]
                        clause = list(map(lambda x: int(x), clause))
                        self.add_clause(clause)

    def set_clauses(self, clauses: Tuple[str, List[int]]) -> None:
        self.clauses = clauses

    def get_clauses(self) -> Tuple[str, List[int]]:
        return self.clauses

    def add_clause(self, clause: List[int]) -> None:
        clause.sort()
        clause_idx = ''.join(str(e) + "_" for e in clause)
        # ignore duplicate clauses
        if clause_idx not in self.clauses:
            self.clauses[clause_idx] = clause
            for lit in clause:
                if lit in self.literal_indices:
                    self.literal_indices[lit].append(clause_idx)
                else:
                    self.literal_indices[lit] = [clause_idx]

    def remove_clause_containing(self, literal: int) -> None:
        for c_idx in self.literal_indices[literal]:
            if c_idx in self.clauses:
                del self.clauses[c_idx]

    def remove_literal_from_clauses(self, literal: int) -> None:
        if literal in self.literal_indices:
            for c_idx in self.literal_indices[literal]:
                if c_idx in self.clauses:
                    self.clauses[c_idx].remove(literal)
        if -literal in self.literal_indices:
            for c_idx in self.literal_indices[-literal]:
                if c_idx in self.clauses:
                    self.clauses[c_idx].remove(-literal)

    @staticmethod
    def is_unit_clause(clause: List[int]) -> bool:
        return len(clause) == 1

    def get_unit_clauses(self) -> List[List[int]]:
        return list(filter(lambda x: self.is_unit_clause(x), self.clauses.values()))

    def get_all_variables(self) -> List[int]:
        return list(set((map(lambda x: abs(x), self.get_all_literals()))))

    def get_unit_variables(self) -> List[int]:
        return list(set(map(lambda x: abs(x[0]), self.get_unit_clauses())))

    def get_all_literals(self) -> List[int]:
        return list(self.literal_indices.keys())

    @staticmethod
    def literal_is_negated(literal: int) -> bool:
        return literal < 0
>>>>>>> master
