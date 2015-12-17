#! /bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: run_experiment.sh [file_to_append_results_to]"
  exit
fi

echo "Progress..."
str="0%"
for i in `seq 1 10`
do
    python main.py --no_display >/dev/null
    cat data/temp.txt >> $1
    echo "$i$str"
done
