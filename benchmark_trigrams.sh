#!/bin/bash

# Runs the long benchmarks on the trigrams scripts
> time_trigram.csv
mkdir -p "output/trigrams_data"
TIMEFORMAT=%R
for i in {1..9} 
do
    { ./trigrams.sh $i > output/trigrams_data/"trigrams_$i.txt" ; }\
        2>> time_trigram.csv
done