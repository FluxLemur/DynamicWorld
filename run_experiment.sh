#! /bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: run_experiment.sh [file for survival] [file for timeseries]"
  exit
fi

touch $1
touch $2

echo "Progress..."
str="0%"
for i in `seq 1 3`
do
    python main.py --no_display >/dev/null
    cat data/temp.txt >> $1
    cat data/temp_timeseries.txt >> $2
    echo "$i$str"
done
