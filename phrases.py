"""
Finds the most salient bigrams and trigrams
"""
from typing import Iterator
from gensim.models.phrases import Phrases, Phraser, npmi_scorer

from input_output import Timer, output, read_corpus, read_slice, get_args


def salient_bigrams(phrases: Phrases):
    """Finds the most salient bigrams

    Args:
        phrases (Phrases): Phrases class set up for bigram search
    """
    for slice in read_corpus():
        phrases.add_vocab(read_slice(slice))

        # evaluate all previous corpus slices
        found = set()
        total_bigrams_encountered = 0
        for previous_slice in read_corpus():
            for phrase, score in phrases.export_phrases(read_slice(previous_slice)):
                found.add((phrase, score))
                total_bigrams_encountered += 1
            if previous_slice == slice:
                break

        found = sorted(found, key=lambda element: element[1], reverse=True)

        # no bigrams found?
        if len(found) == 0:
            output(slice, "")

        # log the top ten bigrams
        for phrase, score in found[:10]:
            output(slice, "{phrase}, {score}".format(
                phrase=phrase, score=score))

        # log the total counts
        output(slice,
"""
Total bigrams: {total}
Unique bigrams: {unique}
Median score:{median}
Max score:{max}
Min score:{min}
"""
               .format(total=total_bigrams_encountered,
                       unique=len(found),
                       median=found[len(found)//2] if len(found) != 0 else 0,
                       max=found[0] if len(found) != 0 else 0,
                       min=found[-1]) if len(found) != 0 else 0)

        # will log a time if command line args were enabled
        Timer.try_to_time()


def salient_trigrams(phrases: Phrases):
    """Finds the most salient trigrams

    Args:
        phrases (Phrases): Phrases class set up for bigram search
    """
    trigram = Phrases()

    for slice in read_corpus():
        # prepare the bigram
        for previous_slice in read_corpus():
            phrases.add_vocab(read_slice(slice))
            if previous_slice == slice:
                break
        
        # transform sentences into possible bigrams
        trigram.add_vocab((phrases[sentence] for sentence in read_slice(slice)))

        # evaluate all previous corpus slices
        found = set()
        total_trigrams_encountered = 0
        for previous_slice in read_corpus():
            for phrase, score in trigram.export_phrases(read_slice(previous_slice)):
                if phrase.count(b' ') == 2:
                    found.add((phrase, score))
                    total_trigrams_encountered += 1
            if previous_slice == slice:
                break

        found = sorted(found, key=lambda element: element[1], reverse=True)

        # no trigrams found?
        if len(found) == 0:
            output(slice, "")

        # log the top ten trigrams
        for phrase, score in found[:10]:
            output(slice, "{phrase}, {score}".format(
                phrase=phrase, score=score))

        # log the total counts
        output(slice,
"""
Total trigrams: {total}
Unique trigrams: {unique}
Mean score:{median}
Max score:{max}
Min score:{min}
"""
               .format(total=total_trigrams_encountered,
                       unique=len(found),
                       median=found[len(found)//2] if len(found) != 0 else 0,
                       max=found[0] if len(found) != 0 else 0,
                       min=found[-1] if len(found) != 0 else 0))

        # will log a time if command line args were enabled
        Timer.try_to_time()

def main():

    args = get_args()

    phrases = Phrases()

    if args['ngram'] == "bigram":
        salient_bigrams(phrases)
    elif args['ngram'] == "trigram":
        salient_trigrams(phrases)


if __name__ == "__main__":
    main()
