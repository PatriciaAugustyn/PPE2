from datastructures import Token, Item, name2loader, name2saver
from datastructures import Corpus

""" ligne de commande 
ython analyzers.py output.json -l json -s json -o analyzed_stanza-corpus.json -a stanza
"""

def load_spacy():
    import spacy
    return spacy.load("fr_core_news_lg")


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


def analyze_stanza(parser, article: Item) -> Item:
    result = parser( (article.title or "" ) + "\n\n" + (article.description or ""))
    output = []
    for sentence in result.sentences:
        for token in sentence.words:
            #print(token.head)
            output.append(Token(
                    id=token.id,
                    shape=token.text,
                    lemma=token.lemma,
                    pos=token.upos,
                    dep=token.deprel,
                    gov=sentence.words[token.head - 1].text if 0 < token.head <= len(sentence.words) else None,
                    gov_id=token.head,
                ))
    article.analysis = [output]
    return article


def analyze_trankit(parser, article: Item) -> Item:
    result = parser( (article.title or "" ) + "\n" + (article.description or ""))
    output = []
    for sentence in result['sentences']:
        for token in sentence['tokens']:
            if 'expanded' not in token.keys():
                token['expanded'] = [token]
            for w in token['expanded']:
                output.append(Token(w['text'], w['lemma'], w['upos']))
    article.analysis = output
    return article



name2analyzer = {
    "spacy": (load_spacy, analyze_spacy),
    "stanza": (load_stanza, analyze_stanza),
    "trankit": (load_trankit, analyze_trankit),
}


def main(input_file, load_serialized=None, save_serialized=None, output_file=None, analyzer=None):
    DEMO_HARD_LIMIT = 10 # pour faire une démonstration au besoin

    load_corpus = name2loader[load_serialized or "json"]
    save_corpus = name2saver[save_serialized or "json"]
    load_model, analyze = name2analyzer[analyzer]

    corpus = load_corpus(input_file)
    model = load_model()
    
    corpus.items = corpus.items[:DEMO_HARD_LIMIT]  # commenter pour traiter tout le corpus
    corpus.items = [analyze(model, item) for item in corpus.items]

    if output_file:
        save_corpus(corpus, output_file)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input file, a serialized corpus.")
    parser.add_argument("-l", "--load-serialized", choices = sorted(name2loader.keys()))
    parser.add_argument("-s", "--save-serialized", choices = sorted(name2saver.keys()))
    parser.add_argument("-o", "--output-file", help="Output file")
    parser.add_argument("-a", "--analyzer", choices=sorted(name2analyzer.keys()))
    
    args = parser.parse_args()
    if args.input_file:
        loader = name2loader[args.load_serialized]
        corpus = loader(args.input_file)
    else:
        corpus = Corpus(sys.stdin.read())

    main(
        input_file=args.input_file,
        load_serialized=args.load_serialized,
        save_serialized=args.save_serialized,
        output_file=args.output_file,
        analyzer=args.analyzer
    )
