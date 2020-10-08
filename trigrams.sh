#!/bin/bash

# Get salient bigrams from the corpus
if [ $# -gt 1 ]; then
	echo "Usage: ./trigrams.sh [number-of-slices-from-1B-corpus]"
	echo "No slice count means the entire corpus"
	exit 1
fi
TIMEFORMAT=%R
if [ $# -eq 1 ]; then
	echo "Looking on $1 slice(s)"
	time python get_trigrams.py --slices $1 /u/demorali/corpora/1g-word-lm-benchmark-r13output/training-monolingual.tokenized.shuffled output/trigrams
else
	echo "Looking on all slices"
	time python get_trigrams.py /u/demorali/corpora/1g-word-lm-benchmark-r13output/training-monolingual.tokenized.shuffled output/trigrams
fi
