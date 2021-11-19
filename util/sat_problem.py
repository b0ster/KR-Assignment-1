import math
# from typing import List, Tuple, Dict
from typing import Optional


class SATProblem:
    """
        Reads DIMACS format from a file, and puts the clauses into memory
    """

    def __init__(self, file: Optional[str] = None, file_type: str = 'DIMACS') -> None:
        if file_type != 'DIMACS':
            raise Exception("Only DIMACS files are supported currently.")
        self.clauses: dict[str, list[int]] = {}
        self.literal_indices: dict[int, list[str]] = {}
        if file is not None:
            with open(file, 'r') as f:
                lines = f.readlines()
                for l in lines:
                    if not l.startswith("c") and not l.startswith("p"):
                        split_l = l.split(" ")
                        clause = split_l[:-1]
                        clause = list(map(lambda x: int(x), clause))
                        self.add_clause(clause)

    def set_clauses(self, clauses: dict[str, list[int]]) -> None:
        self.clauses = clauses

    def get_clauses(self) -> dict[str, list[int]]:
        return self.clauses

    def get_copied_clauses(self) -> dict[str, list[int]]:
        p_clauses: dict[str, list[int]] = {}
        for c_idx, clauses in self.get_clauses().items():
            p_clauses[c_idx] = [lit for lit in clauses]
        return p_clauses

    def add_clause(self, clause: list[int]) -> None:
        clause_idx = ''.join(str(e) + "_" for e in sorted(clause))
        # ignore duplicate clauses
        if clause_idx not in self.clauses:
            self.clauses[clause_idx] = clause
            for lit in clause:
                if lit in self.literal_indices:
                    self.literal_indices[lit].append(clause_idx)
                else:
                    self.literal_indices[lit] = [clause_idx]

    def solve_literal(self, *literals: int) -> None:
        for literal in literals:
            for c_idx in self.literal_indices[literal]:
                if c_idx in self.clauses:
                    del self.clauses[c_idx]
            if -literal in self.literal_indices:
                for c_idx in self.literal_indices[-literal]:
                    if c_idx in self.clauses.keys():
                        if -literal in self.clauses[c_idx]:
                            self.clauses[c_idx].remove(-literal)

    @staticmethod
    def is_unit_clause(clause: list[int]) -> bool:
        return len(clause) == 1

    def get_unit_clauses(self) -> list[list[int]]:
        return list(filter(lambda x: self.is_unit_clause(x), self.clauses.values()))

    def get_all_variables(self) -> list[int]:
        return list(set((map(lambda x: abs(x), self.get_all_literals()))))

    def get_unit_variables(self) -> list[int]:
        return list(set(map(lambda x: abs(x[0]), self.get_unit_clauses())))

    def get_pure_literals(self) -> list[int]:
        literals = self.get_all_literals()
        return [l for l in literals if -l not in literals]

    def get_unit_literals(self) -> list[int]:
        return list(set(map(lambda x: x[0], self.get_unit_clauses())))

    def get_all_literals(self) -> list[int]:
        return list(self.literal_indices.keys())

    @staticmethod
    def literal_is_negated(literal: int) -> bool:
        return literal < 0

    def save_to_file_dimacs(self, name: str, location: str) -> None:
        if location is None:
            raise Exception("Location must be specified.")
        if name is None:
            raise Exception("Name must be specified.")
        dimacs = ["c " + name + ".cnf"]
        dim = round(math.sqrt(len(self.get_clauses())))
        for c in self.get_clauses().values():
            str_clause = ""
            for l in c:
                str_clause += str(l) + " "
            str_clause += "0"
            dimacs.append(str_clause)
        dimacs.insert(1, "p cnf {}{}{} {}".format(dim, dim, dim, len(dimacs) - 1))
        with open(location, "w") as output:
            for l in dimacs:
                output.write(l + "\n")
