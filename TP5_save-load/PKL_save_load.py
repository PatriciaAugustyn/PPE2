import pickle
from datastructures import Corpus
from pathlib import Path

# R3 pickle : https://docs.python.org/fr/3/library/pickle.html#examples
def save_pickle(corpus: Corpus, output_file: Path) -> None:
    with open(output_file, 'wb') as pickle_file:
        pickle.dump(corpus, pickle_file)

def load_pickle(input_file: Path) -> Corpus:
    with open(input_file, 'rb') as pickle_file:
        corpus = pickle.load(pickle_file)
    return corpus
