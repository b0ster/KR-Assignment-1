## (SUDOKU) DPLL SAT SOLVER

A generic DPLL SAT solver implementation, which can solve any DIMACS-formatted problem.\
This repository contains a variety of DIMACS-formatted sudoku SAT problems.

### Prerequisites:
- **Python 3.9**
- Packages (Numpy, MatPlotLib)

#### Installing packages:

**Numpy**
```Bash
pip install numpy
```

**MatPlotLib**
```Bash
pip install matplotlib
```

### Usage:

To solve a DIMACS SAT-problem, `SAT.sh` or `sat_solver.py` can be used.

#### Examples:
Multiple DIMACS files can be given simultaneously to the SAT-solver. These problems will then 
be merged to a single one.

First example (two files separately (will be merged)):
```bash
 /bin/bash SAT.sh -S 1 data/rules/sudoku-rules-4x4.txt data/sudoku/dimacs/4x4/sudoku-4x4-3.txt
```

or

```bash
 python sat_solver.py -S 1 data/rules/sudoku-rules-4x4.txt data/sudoku/dimacs/4x4/sudoku-4x4-3.txt
```

Second example (single file **merged beforehand**):
```bash
 /bin/bash SAT.sh -S 1 data/rules/sudoku-rules-4x4_and_sudoku-4x4-3.txt
```

or

```bash
 python sat_solver.py -S 1 data/rules/sudoku-rules-4x4_and_sudoku-4x4-3.txt
```

#### Options:

| Argument  | Options| Default| Required  | Goal
|---|---|---|---|---|
| -S  | [1,2,3,4,5,6] | - | Yes  | Define which heuristic to use (_see heuristics table_).  |
| --is-sudoku  | [yes,no]  | Yes  | No  | Give a hint whether problem is sudoku (for visualizations)|
| -O  | _\<Any path>_  | CWD  | No  | Where to save the results. |
| -V  | [yes,no] | No  | No  | If visualizations should be made (only for sudoku currently).|
| -ID  | _\<Any id>_  | Name of first DIMACS argument  | No  | Give a prefix to the desired output results. |

#### Heuristics:

|ID|Heuristics|
|---|---|
|1|None (default DPLL)|
|2|MOM's Heuristic|
|3|Jeroslow-Wang (1-Sided)|
|4|Jeroslow-Wang (2-Sided)|
|5|Length Priority Heuristic (_see paper_)|
|6|Minimum Occurrences Heuristic (_see paper_)|


### Utilities (for sudoku specifically):

Here is a list of handy utilities.

**dotted_to_dimacs.py**\
Sometimes sudokus are being represented in a "dotted" format. As this SAT solver only eats DIMACS
format, `dotted_to_dimacs.py` may be handy to use.

An example:

```Bash
python util/dotted_to_dimacs.py -infile data/sudoku/dotted/9x9sudokus.txt -outdir data/sudoku/dimacs/9x9/
```

Where `infile` represents the input file with "dotted" format (each line is being interpreted as a new sudoku) and
`outdir` is the directory to individually save every DIMACS formatted problem to.
