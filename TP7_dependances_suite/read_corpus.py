#Exemple d'appel de commande :
    #python3 read_corpus.py ../../Corpus/2024/01 -r etree -i glob -s 2024-01-26 -e 2024-01-29 | python3 analyzers.py -s pickle -o test_s9.pickle -a spacy

from datetime import datetime

from rss_reader import name2reader
from rss_parcours import name2iterator, filtre_categories, filtre_start_date, filtre_end_date, filtre, read_corpus

from datastructures import Corpus, name2loader, name2saver, save_json, save_xml, save_pickle

import pickle
import sys

'''
import sys
from datastructures import read_corpus

def load_corpus_from_stdin():
    corpus_input = sys.stdin.read()
    return read_corpus(corpus_input)

if __name__ == "__main__":
    corpus = load_corpus_from_stdin()
    print(corpus)
'''




def main(
    data_source,
    load_serialized=None, save_serialized=None, output_file=None,
    rss_reader=None, iterator=None,
    start_date=None, end_date=None, categories=None, sources=None
):



    if load_serialized is not None and rss_reader is not None:
        raise ValueError("Cannot provide value for both deserialization and RSS reader.")

    if load_serialized is not None:
        loader = name2loader[load_serialized]
        corpus: Corpus = loader(data_source)
    else:
        reader = name2reader[rss_reader or "feedparser"]
        iterator = name2iterator[iterator or "glob"]

        # inclure une timezone bidon permet d'avoir une comparaison qui marche
        # quand on fournit qu'une date. Attention à ne pas l'ajouter dans l'argument !
        # voir la doc : https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat
        #
        # point syntaxe sur "x and f(x)" : on s'assure d'avoir une valeur non nulle avant de lancer f, sinon on ne fait rien.
        # À tester dans un terminal :
        # >>> None and repr('a')
        # None
        # >>> 'a' and repr('a')
        # "'a'" # valeur de repr('a')
        # >>> print(1 and None) # attention quand même avec cette syntaxe !
        # None
        filters = []
        filters.append(filtre_start_date(start_date and datetime.fromisoformat(start_date + " 00:00:00+00:00")))
        filters.append(filtre_end_date(end_date and datetime.fromisoformat(end_date + " 00:00:00+00:00")))
        filters.append(filtre_categories(set(categories or [])))

        sources = sources or []

        corpus: Corpus = read_corpus(data_source, sources, iterator, reader, filters)


    save = None
    '''
    if save_serialized is None:
        if output_file is None:
            #raise ValueError("No output file provided for serialization!")
            #print(corpus)
            for item in corpus.items:
                print(item)

            # Sérialiser l'objet Corpus avec pickle
            serialized_corpus = pickle.dumps(corpus)
            # Envoyer le résultat sérialisé à la sortie standard
            #print(serialized_corpus.decode())
            sys.stdout.buffer.write(serialized_corpus)
    '''
    #elif save_serialized is not None:
    if save_serialized is not None:
        save = name2saver[save_serialized]
        if output_file is None:
            #raise ValueError("No output file provided for serialization!")
            #print(corpus)
            #for item in corpus.items:
                #print(item)
            if save_serialized == "pickle":
            # Sérialiser l'objet Corpus avec pickle
                serialized_corpus = save_pickle(corpus)
                sys.stdout.buffer.write(serialized_corpus)
            elif save_serialized == "json":
                serialized_corpus = save_json(corpus)
                #sys.stdout.buffer.write(serialized_corpus)
                sys.stdout.buffer.write(serialized_corpus.encode())
                #print(serialized_corpus)
            elif save_serialized == "xml":
                serialized_corpus = save_xml(corpus)

            # Envoyer le résultat sérialisé à la sortie standard
            #print(serialized_corpus.decode())
            #sys.stdout.buffer.write(serialized_corpus)

    if save is not None:
        save(corpus, output_file)
        #print(len(corpus.items))
    print(len(corpus.items))
    #else :
        #print(corpus)
        #for item in corpus.items:
            #print(item)
        #return corpus



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("data_source", help="input file may be a file or a directory depending on how we load data.")
    parser.add_argument("-l", "--load-serialized", choices = sorted(name2loader.keys()))
    parser.add_argument("-z", "--save-serialized", choices = sorted(name2saver.keys()))
    parser.add_argument("-o", "--output-file", help="Output file for serialization")
    parser.add_argument("-r", "--rss-reader", choices = sorted(name2reader.keys()))
    parser.add_argument("-i", "--iterator", choices = sorted(name2iterator.keys()))
    parser.add_argument("-s", "--start-date", help="date in ISO format YYYY-MM-DD")
    parser.add_argument("-e", "--end-date", help="date in ISO format YYYY-MM-DD")
    parser.add_argument("-c", "--categories", nargs="*", help="liste des catégories à considérer (article OK = une parmi la liste)")
    parser.add_argument("--sources", nargs="*", help="liste des sources à considérer (article OK = une parmi la liste)")

    args = parser.parse_args()
    main(
        args.data_source,
        load_serialized=args.load_serialized,
        save_serialized=args.save_serialized,
        output_file=args.output_file,
        rss_reader=args.rss_reader,
        iterator=args.iterator,
        start_date=args.start_date,
        end_date=args.end_date,
        categories=args.categories,
        sources=args.sources
    )
