#!/bin/bash
rules="../data/rules/sudoku-rules-9x9.txt"
heuristics=("1" "2" "3" "4" "5" "6")
dt=$(date '+%Y_%m_%d_%H_%M_%S')
output_folder="../results/experiment/top91-9x9/${dt}/"

for path in ../data/sudoku/dimacs/top91-9x9/*.txt; do
  filename=$(basename -- $path)
  filename="${filename%.*}"
  for heur in ${heuristics[@]}; do
      dir="$output_folder$filename/${heur}"
      python ../sat_solver.py -S ${heur} -O ${dir} -ID ${filename} ${rules} ${path}
  done
done
