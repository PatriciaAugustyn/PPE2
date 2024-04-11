import pickle
from datastructures import Token, Item, Corpus 

file_path = 'analyzed_corpus_trankit.pkl'

with open(file_path, 'rb') as file:
    data = pickle.load(file)

print(data)
