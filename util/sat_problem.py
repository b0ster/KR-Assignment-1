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

    def set_clauses(self, clauses: dict[str, list[int]]) -> None:
        """
        Sets the clauses of the problem (overwrites).
        :param clauses: dict of str key and list of disjunctions
        """
        self.clauses = clauses

    def get_clauses(self) -> dict[str, list[int]]:
        """
        Gets all the clauses of the problem.
        :return: dict with clause_idx as key and list of disjunctions as value.
        """
        return self.clauses

    def get_copied_clauses(self) -> dict[str, list[int]]:
        """
        Gets a copy instance of current clauses.
        :return: copied dict with clause_idx as key and list of disjunctions as value.
        """
        p_clauses = {}
        for c_idx, clauses in self.get_clauses().items():
            p_clauses[c_idx] = [lit for lit in clauses]
        return p_clauses

    def add_clause(self, clause: list[int]) -> None:
        """
        Adds a clause to the current clauses.
        :param clause: list of disjunctions, as a clause.
        """
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
        """
        Solves one (or multiple vararg) literals, meaning all clauses containing the literal will be removed and
        all clauses containing the negated literal will be reduced.
        :param literals: one or more literals to "solve".
        """
        for literal in literals:
            for c_idx in self.literal_indices[literal]:
                if c_idx in self.clauses:
                    if literal in self.clauses[c_idx]:
                        del self.clauses[c_idx]
            if -literal in self.literal_indices:
                for c_idx in self.literal_indices[-literal]:
                    if c_idx in self.clauses.keys():
                        if -literal in self.clauses[c_idx]:
                            self.clauses[c_idx].remove(-literal)

    @staticmethod
    def is_unit_clause(clause: list[int]) -> bool:
        """
        Checks whether given clause is a unit clause (length=1)
        :param clause: list of disjunctions.
        :return: bool whether is a unit clause.
        """
        return len(clause) == 1

    def get_unit_clauses(self) -> list[list[int]]:
        """
        Gets all the unit clauses from all clauses.
        :return: list of unit clauses.
        """
        return list(filter(lambda x: self.is_unit_clause(x), self.clauses.values()))

    def get_all_variables(self) -> list[int]:
        """
        Gets all unique variables from current clauses.
        :return: list of unique variables.
        """
        return list(set(map(lambda x: abs(x), self.get_all_literals())))

    def get_unit_variables(self) -> list[int]:
        """
        Gets all the unit variables, i.e. variables that only occur in unit clauses.
        :return: list of unit variables.
        """
        return list(set(map(lambda x: abs(x[0]), self.get_unit_clauses())))

    def get_pure_literals(self) -> list[int]:
        """
        Gets a list of pure literals, i.e. literals that only occur negated on non-negated in all current clauses.
        Note: this is computational expensive, worst O(n)^2.
        :return: list of pure literals.
        """
        literals = self.get_all_literals()
        return [l for l in literals if -l not in literals]

    def get_unit_literals(self) -> list[int]:
        """
        Gets all unit literals, i.e. literals that only occur in unit clauses.
        :return: list of unit literals.
        """
        return list(set(map(lambda x: x[0], self.get_unit_clauses())))

    def get_all_literals(self) -> list[int]:
        """
        Gets all literals from the current left clauses.
        :return: list of literals.
        """
        return list(self.literal_indices.keys())

    @staticmethod
    def literal_is_negated(literal: int) -> bool:
        """
        Checks whether given literal is negated (<0)
        :param literal: an int literal.
        :return: bool whether is negated or not.
        """
        return literal < 0

    def save_to_file_dimacs(self, name: str, location: str) -> None:
        """
        Saves the current instance to DIMACS format on file system.
        :param name: name of the knowledge base.
        :param location: location to save the DIMACS file.
        """
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
