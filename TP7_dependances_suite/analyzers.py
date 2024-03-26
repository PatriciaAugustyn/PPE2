#analyzers.py test.pickle -l pickle -s pickle -o test_dep2.pickle -a spacy
from datastructures import *
import sys
import argparse
import fileinput
from pathlib import Path


def load_spacy():
    import spacy
    return spacy.load("fr_core_news_sm")


def load_stanza():
    import stanza
    stanza.download("fr")  # téléchargé qu'une fois, peut se commenter
    return stanza.Pipeline("fr", processors="tokenize,pos,lemma,depparse")


def load_trankit():
    import trankit
    return trankit.Pipeline('french', gpu=False)


def analyze_spacy(parser, article: Item) -> Item:
    result = parser( (article.title or "" ) + "\n" + (article.description or ""))
    output = []
    for sentence in result.sents:
        output.append([])
        for token in sentence:
            if token.text.strip():
                output[-1].append(Token(token.text, token.lemma_, token.pos_, token.dep_, token.head.i - sentence.start))
    article.analysis = output
    return article
    '''
    result = parser( (article.title or "" ) + "\n" + (article.description or ""))
    output = []
    for token in result:
        if token.text.strip():
            dependencies = [
                TestDependance(dep.text, dep.lemma_, dep.pos_, dep.dep_)
                for dep in token.children
            ]

            output.append(Token(token.text, token.lemma_, token.pos_, dependencies))
    article.analysis = output
    return article
    '''



def analyze_stanza(parser, article: Item) -> Item:
    result = parser((article.title or "") + "\n" + (article.description or ""))
    output = []
    for sentence in result.sentences:
        #output.append([])
        for word in sentence.words:
            output.append(Token(shape=word.text, lemma=word.lemma, pos=word.upos, dep=word.deprel, gov=word.head))
            #output.append(Token(shape=word.text, lemma=word.lemma, pos=word.upos, dep=word.deprel, gov=word.head - sentence.start))
            #output[-1].append(Token(shape=word.text, lemma=word.lemma, pos=word.upos, dep=word.deprel, gov=word.head.i - sentence.start))
    article.analysis = output
    return article
    '''
    result = parser((article.title or "") + "\n" + (article.description or ""))
    output = []
    for sent in result.sentences:
        for word in sent.words:
            dependencies = [TestDependance(text=dep.text, lemma=dep.lemma, pos=dep.pos, dependencies=dep.deprel) for dep in sent.words if dep.head == word.id]
            output.append(Token(shape=word.text, lemma=word.lemma, pos=word.upos, dependencies=dependencies))
    article.analysis = output
    return article
'''



def analyze_trankit(parser, article: Item) -> Item:
    result = parser((article.title or "") + "\n" + (article.description or ""))
    output = []

    for sentence in result['sentences']:
        #output.append([])
        for token in sentence['tokens']:
            shape = token.get('text', '')
            lemma = token.get('lemma', '')
            pos = token.get('upos', '')
            head = token.get('head', 0)
            deprel = token.get('deprel', '')

            token_obj = Token(shape=shape, lemma=lemma, pos=pos, dep=deprel, gov=head)
            #token_obj = Token(shape=shape, lemma=lemma, pos=pos, dep=deprel, gov=head - sentence.start)
            output.append(token_obj)
            #output[-1].append(token_obj)

    article.analysis = output
    return article
    '''
    result = parser((article.title or "") + "\n" + (article.description or ""))
    output = []

    for sentence in result['sentences']:
        for token in sentence['tokens']:
            shape = token.get('text', '')
            lemma = token.get('lemma', '')
            pos = token.get('upos', '')
            head = token.get('head', 0)
            deprel = token.get('deprel', '')

            dependencies = []
            if deprel:
                dep_obj = TestDependance(text=shape, lemma=lemma, pos=pos, dependencies=deprel)
                dependencies.append(dep_obj)

            token_obj = Token(shape=shape, lemma=lemma, pos=pos, dependencies=dependencies)
            output.append(token_obj)

    article.analysis = output
    return article
'''







# Chargement du corpus à partir de la sortie standard
#corpus = sys.stdin.read()




'''
def analyze_from_stdin(analyzer=None):
    load_model, analyze = name2analyzer[analyzer]
    # Charger le corpus à partir de l'entrée standard
    corpus = load_corpus_from_stdin()  # Fonction pour charger le corpus à partir de l'entrée standard

    # Analyser le corpus
    analyzed_corpus = analyze_corpus(corpus)  # Fonction pour analyser le corpus

    # Imprimer les résultats ou les enregistrer dans un fichier
    print(analyzed_corpus)  # Imprimer les résultats à la sortie standard

'''
'''
import sys
from datastructures import analyze_corpus

def analyze_from_stdin():
    corpus_input = sys.stdin.read()
    result = analyze_corpus(corpus_input)
    print(result)

if __name__ == "__main__":
    analyze_from_stdin()
'''





name2analyzer = {
    "spacy": (load_spacy, analyze_spacy),
    "stanza": (load_stanza, analyze_stanza),
    "trankit": (load_trankit, analyze_trankit),
}


def main(input_file=None, load_serialized=None, save_serialized=None, output_file=None, analyzer=None):
    DEMO_HARD_LIMIT = 10 # pour faire une démonstration au besoin

    if input_file:
        # Charger le corpus à partir du fichier
        load_corpus = name2loader[load_serialized or "json"]
        corpus = load_corpus(input_file)
    else:
        # Charger le corpus à partir de l'entrée standard
        #import json  # ou autre format selon votre besoin
        #import pickle
        #corpus_data = sys.stdin.read()
        #corpus = Corpus.from_dict(json.loads(corpus_data))
        #corpus = sys.stdin.read()

        # Lire les données binaires depuis l'entrée standard
        serialized_corpus = sys.stdin.buffer.read()
        # Désérialiser l'objet Corpus à partir des données sérialisées
        if save_serialized == "pickle":
            #serialized_corpus = sys.stdin.buffer.read()
            corpus = pickle.loads(serialized_corpus)
        elif save_serialized == "json":
            #serialized_corpus = sys.stdin.buffer.read().decode()
            #corpus = json.loads(serialized_corpus.decode())
            corpus = json.loads(serialized_corpus)
            #print(serialized_corpus)
        elif save_serialized == "xml":
            corpus = xml.loads(corpus)


    #load_corpus = name2loader[load_serialized or "json"]
    save_corpus = name2saver[save_serialized or "json"]
    load_model, analyze = name2analyzer[analyzer]

    #corpus = load_corpus(input_file)
    model = load_model()

    corpus.items = corpus.items[:DEMO_HARD_LIMIT]  # commenter pour traiter tout le corpus
    corpus.items = [analyze(model, item) for item in corpus.items]

    if output_file:
        save_corpus(corpus, output_file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    #parser.add_argument("input_file", help="Input file, a serialized corpus.")
    parser.add_argument("-l", "--load-serialized", choices = sorted(name2loader.keys()))
    parser.add_argument("-s", "--save-serialized", choices = sorted(name2saver.keys()))
    parser.add_argument("-o", "--output-file", help="Output file")
    parser.add_argument("-a", "--analyzer", choices=sorted(name2analyzer.keys()))

    args = parser.parse_args()
    main(
        #input_file=args.input_file,
        load_serialized=args.load_serialized,
        save_serialized=args.save_serialized,
        output_file=args.output_file,
        analyzer=args.analyzer
    )
