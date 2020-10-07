"""
Finds the most salient bigrams and trigrams
"""
from typing import Iterator
from gensim.models.phrases import Phrases, Phraser, npmi_scorer

from input_output import Timer, output, read_corpus, read_slice, get_args

def main():
    
    args = get_args()

    phrases = Phrases()

    for slice in read_corpus():
        phrases.add_vocab(read_slice(slice))

        found = set(((phrase, score) for phrase, score in phrases.export_phrases(read_slice(slice))))
        found = sorted(found, key=lambda element: element[1], reverse=True)
            
        for phrase, score in found:
            output(slice, "{phrase}, {score}".format(phrase=phrase, score=score))

        # will log a time if command line args were enabled
        Timer.try_to_time()

if __name__ == "__main__":
    main()