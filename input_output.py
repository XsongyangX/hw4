"""
Handles the io of the correction program
"""
import argparse
from argparse import Namespace
import os
from typing import Dict, Iterator
import time

parsed_args: Namespace

class Timer:
    __instance = None
    is_timing = False

    @staticmethod
    def try_to_time():
        if Timer.is_timing:
            Timer.__instance.log()

    @staticmethod
    def get_current_timer():
        """
        Get a singleton instance of the timer
        """
        if Timer.__instance is None:
            raise Exception("No timer")
        return Timer.__instance

    def __init__(self, path: str):
        """Creates a timer instance

        Args:
            path (str): Path to the file where to put the time
        """
        self.start = time.time()
        self.path_to_log = path

        # clean up the log file
        open(self.path_to_log, 'w').close()

        Timer.is_timing = True
        Timer.__instance = self

    def log(self):
        """
        Logs the elapsed time since instantiation
        """
        with open(self.path_to_log, 'a') as time_log:
            time_log.write("{}\n".format(time.time() - self.start))


def get_args() -> Dict[str, str]:
    """Gathers command line arguments and prepares output file if needed

    Returns:
        Dict[str, str]: Argument values, keys: [input_folder, output_folder, ngram]
    """
    parser = argparse.ArgumentParser(
        description="Finds the most salient bigrams or trigrams in a corpus. Bigrams by default.")

    parser.add_argument('input',
                        help="Corpus folder to read slices from.")

    parser.add_argument('output',
                        help="Output folder of the most salient collocations (bigrams or trigrams). Exported in slices.")

    parser.add_argument('--slices', type=int, default='-1', metavar='n',\
                        help="How many slices of the corpus to use. Default is all slices.")

    parser.add_argument('--time', dest='is_timing', action='store_const', const=True,
                        default=False,
                        help="Whether to time the execution of the script into a file called time_(bigrams|trigrams).csv")

    # choose one ngram target
    distance_choices = parser.add_mutually_exclusive_group()

    distance_choices.add_argument('--bigram', dest='ngram', action='store_const',
                                  const='bigram', default='bigram',
                                  help="Looks for bigrams. Default.")

    distance_choices.add_argument('--trigram', dest='ngram', action='store_const',
                                  const='trigram',
                                  help="Looks for trigrams")

    # parse the args
    args = parser.parse_args()

    arg_dict = {"input_folder":args.input, "output_folder":args.output,\
        "ngram":args.ngram}

    # input folder does not exist
    if not os.path.exists(args.input):
        raise Exception("Input folder does not exist")

    # output folder does not exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    else:
        for file in os.listdir(args.output):
            os.remove(os.path.join(args.output, file))

    # assign arguments to global
    global parsed_args
    parsed_args = args

    # start timer if needed
    if args.is_timing:
        _ = Timer("time_{}.csv".format(args.ngram))

    return arg_dict

def read_corpus() -> Iterator[str]:
    """Reads from the corpus folder

    Yields:
        Iterator[Iterator[str]]: Iterator of over slice names
    """
    path = parsed_args.input

    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    onlyfiles = [os.path.join(path, file) for file in onlyfiles]
    onlyfiles.sort()

    # limited slices
    if parsed_args.slices != -1:
        onlyfiles = onlyfiles[:parsed_args.slices]

    for slice in onlyfiles:
        yield slice

def read_line(line: str) -> Iterator[str]:
    for word in line.split():
        yield word

def read_slice(path: str) -> Iterator[Iterator[str]]:
    """Reads line by line the slice, lines are turned into iterable str lists

    Args:
        path (str): Path to the corpus slice

    Yields:
        Iterator[Iterator[str]]: Iterator of sentences, which are also iterators
    """
    with open(path, 'r') as slice:
        for line in slice:
            yield read_line(line)

def output(slice: str, message: str):
    """Creates files at the output directory
    Logs the time, if enabled in the command line.

    Args:
        slice (str): Name of the slice of read so far
        message (str): String to output
    """
    out_folder = parsed_args.output


    with open(os.path.join(out_folder, os.path.basename(slice)), 'a') as collocations:
        collocations.write("{}\n".format(message))
