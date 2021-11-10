## (SUDOKU) DPLL SAT SOLVER

A generic DPLL SAT solver implementation, which can solve any DIMACS-formatted problem.\
This repository contains a variety of DIMACS-formatted sudoku SAT problems.

### Usage:

To solve a sudoku, `sat_solver.py` can be used.

An example:

```bash
 python sat_solver.py -S 1 data/rules/sudoku-rules-4x4.txt data/sudoku/dimacs/4x4/sudoku-4x4-3.txt
```

Where `data/rules/sudoku-rules-4x4.txt` are the rules for a 4x4 sudoku, `data/sudoku/dimacs/4x4/sudoku-4x4-3.txt` is an
example partially filled 4x4 sudoku to be solved and `-S 1` is the identifier of the SAT solver (DPLL procedure) to be
used.

Note: for a problems with different dimensions different rules and example should obviously be used.

### Utilities:

Here is a list of handy utilities.

**dotted_to_dimacs.py**\
Sometimes sudokus are being represented in a "dotted" format. As this SAT solver only eats DIMACS
format, `dotted_to_dimacs.py` may be handy to use.

An example:

```Bash
python dotted_to_dimacs.py -infile data/sudoku/dotted/9x9sudokus.txt -outdir data/sudoku/dimacs/9x9/
```

Where `infile` represents the input file with "dotted" format (each line is being interpreted as a new sudoku) and
`outdir` is the directory to individually save every DIMACS formatted sudoku to.