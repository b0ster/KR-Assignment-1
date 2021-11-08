class DIMACS:
    def __init__(self, file) -> None:
        if not isinstance(file, str):
            raise Exception("file should be a string path.")
        self.clauses = []
        with open(file, 'r') as f:
            lines = f.readlines()
            for l in lines:
                if not l.startswith("c") and not l.startswith("p"):
                    split_l = l.split(" ")
                    clause = split_l[:-1]
                    self.clauses.append(clause)

    def get_clauses(self):
        return self.clauses

