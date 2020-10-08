# HW 4 IFT 6285

# Installation
* `gensim` NLP package with pip
* 1B-wc corpus

# Running scripts
Runnable Bash scripts:
* `bigrams.sh`: Finds all salient bigrams on the 1B-wc corpus located on the DIRO servers. `bigrams.sh n`, with an argument, will only parse the first `n` slices of the corpus. Also times the execution and redirects output to a folder named `output/bigrams`.
* `trigrams.sh`: Finds all salient trigrams on the 1B-wc corpus located on the DIRO servers. `trigrams.sh n`, with an argument, will only parse the first `n` slices of the corpus. Does not redirect anything.

Runnable Python scripts:
* `phrases.py [-h] [--slices n] [--time] [--bigram | --trigram] input output`: Runs the `gensim` tool on the given amount of slices of a corpus located in the `input` folder. Partial results will be logged to the given `output` folder, such as bigram counts. Only the `--bigram` works. No slice count given means the entire corpus is to be parsed.
* `get_trigrams.py [-h] [--slices n] [--time] [--bigram | --trigram] input output`: Runs the `gensim` tool on the given amout of slices of a corpus located in the `input` folder. Does not log partial results, so `output` argument is actually useless, but still mandatory nonetheless. Found trigrams are displayed in `stdout`. No slice count given means the entire corpus is to be parsed.