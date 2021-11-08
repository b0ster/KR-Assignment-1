# a trivial (sudoku) line looks like ".94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8"
# here, a '.' is an empty sudoku square
# this class may convert such sudoku format to DIMAC format
class TrivialToDIMACConverter:
    def __init__(self, trivial_txt_line) -> None:
        if not isinstance(trivial_txt_line, str):
            raise Exception("Trivial text should be a string.")
        if "\n" or "\r" in trivial_txt_line:
            raise Exception("Only one trivial text line may be given at once.")
        self.trivial_txt_line = trivial_txt_line

    def get_trivial_txt(self) -> str:
        return self.trivial_txt_line

    def get_dimac_txt(self):
        # todo, convert the trivial text line to a dimac line
        return ""
