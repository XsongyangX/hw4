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

    bigram = Phrases(sentences(), min_count=1, threshold=1)
    bigram_phraser = Phraser(bigram)

    bigrammed = map(lambda x: bigram_phraser[x], sentences())

    trigram = Phrases(bigrammed, min_count=1, threshold=1)
    trigram_phraser = Phraser(trigram)

    for key, value in sorted(trigram_phraser.phrasegrams.items(), key=lambda item: item[1], reverse=True)[:10]:
        print(b"_".join(key), value)

    scores = list(trigram_phraser.phrasegrams.values())
    print(
        """
    Unique trigrams: {unique}
    Mean score:{mean}
    Max score:{max}
    Min score:{min}
    """.format(unique=len(trigram_phraser.phrasegrams),
               mean=mean(scores),
               max=max(scores),
               min=min(scores)))


if __name__ == "__main__":
    main()
