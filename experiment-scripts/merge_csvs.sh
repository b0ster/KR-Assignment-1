#!/bin/bash
read -p "Enter root directory to search csv files in: " rootdir
read -p "Enter output destination file: " dest
awk '(NR == 1) || (FNR > 1)' $(find ${rootdir} -type f -name "*.csv") > ${dest}