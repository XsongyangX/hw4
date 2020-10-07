#!/bin/bash

# Get salient bigrams from the corpus
if [ $# -gt 1 ]; then
	echo "Usage: ./bigrams.sh [number-of-slices-from-1B-corpus]"
	echo "No slice count means the entire corpus"
	exit 1
fi

if [ $# -eq 1 ]; then
	echo "Looking on $1 slice(s)"
	python phrases.py --slices $1 --time /u/demorali/corpora/1g-word-lm-benchmark-r13output/training-monolingual.tokenized.shuffled output/bigrams
else
	echo "Looking on all slices"
	python phrases.py --time /u/demorali/corpora/1g-word-lm-benchmark-r13output/training-monolingual.tokenized.shuffled output/bigrams
fi
