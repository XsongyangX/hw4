from typing import Iterator, Tuple

from numpy.core.fromnumeric import mean
from input_output import get_args, read_corpus, read_slice
from gensim.models import Phrases
from itertools import chain

from gensim.models.phrases import Phraser


def main():
    get_args()

    def sentences(): return chain.from_iterable(
        (read_slice(data) for data in read_corpus()))

    bigram = Phrases(sentences(), min_count=1, threshold=1, delimiter=b' ')
    bigram_phraser = Phraser(bigram)

    bigrammed = map(lambda x: bigram_phraser[x], sentences())

    trigram = Phrases(bigrammed, min_count=1, threshold=1, delimiter=b' ')
    trigram_phraser = Phraser(trigram)

    only_trigrams = {b' '.join(trigram_tuple): score for (trigram_tuple, score) in \
        trigram_phraser.phrasegrams.items() if b' '.join(trigram_tuple).count(b' ') == 2}

    for key, value in sorted(only_trigrams.items(), key=lambda item: item[1], reverse=True)[:10]:
        print(key, value)

    scores = list(only_trigrams.values())
    print(
        """
    Unique trigrams: {unique}
    Mean score:{mean}
    Max score:{max}
    Min score:{min}
    """.format(unique=len(only_trigrams),
               mean=mean(scores),
               max=max(scores),
               min=min(scores)))


if __name__ == "__main__":
    main()
