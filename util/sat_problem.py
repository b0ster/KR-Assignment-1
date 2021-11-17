import math
from typing import List, Tuple, Dict


class SATProblem:
    """
        Reads DIMACS format from a file, and puts the clauses into memory
    """

    def __init__(self, file: str = None, file_type: str = 'DIMACS') -> None:
        if file_type != 'DIMACS':
            raise Exception("Only DIMACS files are supported currently.")
        self.clauses = {}
        self.state_counter = 0
        self.previous_clauses = {}
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

    def set_clauses(self, clauses: Dict[str, List[int]]) -> None:
        self.clauses = clauses

    def get_clauses(self) -> Dict[str, List[int]]:
        return self.clauses

    def get_previous_clauses(self, state_counter) -> Dict[str, List[int]]:
        return self.previous_clauses[state_counter]

    def add_clause(self, clause: List[int]) -> None:
        clause_idx = ''.join(str(e) + "_" for e in sorted(clause))
        # ignore duplicate clauses
        if clause_idx not in self.clauses:
            self.clauses[clause_idx] = clause
            for lit in clause:
                if lit in self.literal_indices:
                    self.literal_indices[lit].append(clause_idx)
                else:
                    self.literal_indices[lit] = [clause_idx]

    def solve_literal(self, literal: int) -> None:
        self.previous_clauses[self.state_counter] = {}
        for c_idx, clauses in self.get_clauses().items():
            self.previous_clauses[self.state_counter][c_idx] = []
            self.previous_clauses[self.state_counter][c_idx] = [lit for lit in clauses]

        for c_idx in self.literal_indices[literal]:
            if c_idx in self.clauses:
                del self.clauses[c_idx]
        if -literal in self.literal_indices:
            for c_idx in self.literal_indices[-literal]:
                if c_idx in self.clauses:
                    if -literal in self.clauses[c_idx]:
                        self.clauses[c_idx].remove(-literal)
        self.state_counter += 1

    @staticmethod
    def is_unit_clause(clause: List[int]) -> bool:
        return len(clause) == 1

    def get_unit_clauses(self) -> List[List[int]]:
        return list(filter(lambda x: self.is_unit_clause(x), self.clauses.values()))

    def get_all_variables(self) -> List[int]:
        return list(set((map(lambda x: abs(x), self.get_all_literals()))))

    def get_unit_variables(self) -> List[int]:
        return list(set(map(lambda x: abs(x[0]), self.get_unit_clauses())))

    def get_unit_literals(self) -> List[int]:
        return list(set(map(lambda x: x[0], self.get_unit_clauses())))

    def get_all_literals(self) -> List[int]:
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
