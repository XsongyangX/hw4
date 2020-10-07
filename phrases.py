"""
Finds the most salient bigrams and trigrams
"""
from typing import Iterator
from gensim.models.phrases import Phrases, Phraser, npmi_scorer

from input_output import read_corpus, read_slice, get_args

def main():
    
    args = get_args()

    phrases: Phrases = None

    for slice in read_corpus():
        if phrases is None:
            phrases = Phrases(read_slice(slice))
        else:
            phrases.add_vocab(read_slice(slice))

        for phrase, score in phrases.export_phrases(read_slice(slice)):
            print(phrase, score)
        

if __name__ == "__main__":
    main()