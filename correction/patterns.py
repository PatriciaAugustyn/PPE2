from datastructures import Token, Item, Match, name2loader, name2saver

from collections import Counter


def pat_noun(sentence: list[Token]) -> list[Match]:
    rule_name = "noun"
    results = []
    for token in sentence:
        if token.pos == "NOUN":
            results.append(Match(rule_name, (token.lemma,)))
    return results




def pat_verb_obj_noun(sentence: list[Token]) -> list[Match]:
    rule_name = "V -obj-> N"
    results = []
    for token in sentence:
        if token.pos == "NOUN" and token.dep == "obj":
                head_i = token.gov
                for i, head in enumerate(sentence):
                    if i == head_i and head.pos == "VERB":
                        results.append(Match(rule_name, (head.lemma, token.lemma)))
    return results

def simple_rel(rule_name: str,
               pos1: str,
               deprel: str,
               pos2: str
               ):
    def pat(sentence: list[Token]) -> list[Match]:
        results = []
        for token in sentence:
            if token.pos == pos2 and token.dep == deprel:
                    head_i = token.gov
                    if head_i < len(sentence):
                        head = sentence[head_i]
                        if head.pos == pos1:
                            results.append(Match(rule_name, (head.lemma, token.lemma)))
        return results
    return pat

  

PATTERNS = [
        simple_rel("v -obj-> n", "VERB", "obj","NOUN"),
        simple_rel("n <-nsubj- v", "VERB", "nsubj", "NOUN"),
        simple_rel("n -nmod-> n", "NOUN","nmod", "NOUN")
        ]

def main(input_file, load_serialized=None):
    DEMO_HARD_LIMIT = 1000 # pour faire une démonstration au besoin

    load_corpus = name2loader[load_serialized or "json"]

    corpus = load_corpus(input_file)
    
    corpus.items = corpus.items[:DEMO_HARD_LIMIT]  # commenter pour traiter tout le corpus
    counter = Counter()
    for item in corpus.items:
        for pattern in PATTERNS:
            for sentence in item.analysis:
                 matches = pattern(sentence)
                 counter += Counter(matches)
    for m,i in counter.items():
        print(i,m)
                  

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input file, a serialized corpus.")
    parser.add_argument("-l", "--load-serialized", choices = sorted(name2loader.keys()))
    
    args = parser.parse_args()
    main(
        input_file=args.input_file,
        load_serialized=args.load_serialized,
    )
