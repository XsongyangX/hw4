"""
Finds the most salient bigrams and trigrams
"""

from typing import Iterator
from gensim.test.utils import datapath
from gensim.models.phrases import Phrases, Phraser

def read_corpus(path: str) -> Iterator[Iterator[str]]:
    with open(path, 'r') as corpus:
        for line in corpus:
            yield get_sentence(line)

def get_sentence(line: str) -> Iterator[str]:
    for word in line.split():
        yield word

phrases = Phrases(read_corpus("testcorpus.txt"), min_count=1, threshold=1)

bigram = Phraser(phrases)
