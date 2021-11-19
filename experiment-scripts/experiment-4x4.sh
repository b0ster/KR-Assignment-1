#!/bin/bash
rules="../data/rules/sudoku-rules-4x4.txt"
heuristics=("1" "2" "3" "4" "5")
dt=$(date '+%Y_%m_%d_%H_%M_%S')
output_folder="../results/experiment/4x4/${dt}/"

for path in ../data/sudoku/dimacs/4x4/*.txt; do
  filename=$(basename -- $path)
  filename="${filename%.*}"
  for heur in ${heuristics[@]}; do
      dir="$output_folder$filename/${heur}"
      python ../sat_solver.py -S ${heur} -O ${dir} -ID ${filename} ${rules} ${path}
  done
done
