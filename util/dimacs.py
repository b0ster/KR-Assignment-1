class DIMACS:
    """
        Reads DIMACS format from a file, and puts the clauses into memory
    """

    def __init__(self, file: str) -> None:
        if not isinstance(file, str):
            raise Exception("file should be a string path.")
        self.clauses = []
        with open(file, 'r') as f:
            lines = f.readlines()
            for l in lines:
                if not l.startswith("c") and not l.startswith("p"):
                    split_l = l.split(" ")
                    clause = split_l[:-1]
                    clause = list(map(lambda x: int(x), clause))
                    self.clauses.append(clause)

    def set_clauses(self, clauses: []) -> None:
        self.clauses = clauses

    def get_clauses(self) -> []:
        return self.clauses

    def add_clause(self, clause: []) -> None:
        self.clauses.append(clause)

    def remove_clause_containing(self, literal: int) -> None:
        self.clauses = list(filter(lambda x: literal not in x, self.clauses))

    def remove_literal_from_clauses(self, literal: int) -> None:
        for c in self.clauses:
            if literal in c:
                c.remove(literal)
            elif -literal in c:
                c.remove(-literal)

    @staticmethod
    def is_unit_clause(clause: []) -> bool:
        return len(clause) == 1

    def get_unit_clauses(self) -> []:
        return list(filter(lambda x: self.is_unit_clause(x), self.clauses))

    def get_all_variables(self) -> []:
        return list(set((map(lambda x: abs(x), self.get_all_literals()))))

    def get_all_literals(self) -> []:
        literals = []
        for c in self.clauses:
            for lit in c:
                if lit not in literals:
                    literals.append(lit)
        return literals

    @staticmethod
    def literal_is_negated(literal: int) -> bool:
        return literal < 0
