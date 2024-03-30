from datastructures import Token, Item, Match, name2loader, name2saver

from collections import Counter, defaultdict


def pat_noun(sentence: list[Token]) -> list[Match]:
    rule_name = "noun"
    results = []
    for token in sentence:
        if token.pos == "NOUN":
            results.append(Match(rule_name, (token.lemma,), (token.pos,), ""))
    return results




def pat_verb_obj_noun(sentence: list[Token]) -> list[Match]:
    rule_name = "V -obj-> N"
    results = []
    for token in sentence:
        if token.pos == "NOUN" and token.dep == "obj":
                head_i = token.gov
                for i, head in enumerate(sentence):
                    if i == head_i and head.pos == "VERB":
                        results.append(Match(rule_name, (head.lemma, token.lemma), (head.pos, token.pos), token.dep))
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
                            results.append(Match(rule_name, (head.lemma, token.lemma), (head.pos, token.pos), token.dep))
        return results
    return pat

def not_so_simple_rel(rule_name: str,
               pos1: str,
               deprel: str,
               pos2: str
               ):
    def pat(sentence: list[Token]) -> list[Match]:
        results = []
        for i, token in enumerate(sentence):
            if token.pos == pos2 and token.dep == deprel:
                head_i = token.gov
                children = get_children(i, sentence)
                if not "mark" in children and not "case" in children:
                    if head_i < len(sentence):
                        head = sentence[head_i]
                        if head.pos == pos1:
                            results.append(Match(rule_name, (head.lemma, token.lemma), (head.pos, token.pos), token.dep))
        return results
    return pat

def marked_rel(rule_name, pos1, deprel, pos2):
    def pat(sentence: list[Token]) -> list[Match]:
        results = []
        for i, token in enumerate(sentence):
            if token.pos == pos2 and deprel in token.dep:
                children = get_children(i, sentence)
                if "mark" in children: 
                    mark = children["mark"][0].lemma
                    head = get_head(token, sentence)
                    if head.pos == pos1:
                        results.append(Match(mark + rule_name, (head.lemma, token.lemma), (head.pos, token.pos), mark))
        return results
    return pat


def case_rel(rule_name, pos1, deprel, pos2):
    def pat(sentence: list[Token]) -> list[Match]:
        results = []
        for i, token in enumerate(sentence):
            if token.pos == pos2 and deprel in token.dep:
                children = get_children(i, sentence)
                if "case" in children: 
                    mark = children["case"][0].lemma
                    head = get_head(token, sentence)
                    if head.pos == pos1:
                        results.append(Match(mark + rule_name, (head.lemma, token.lemma), (head.pos, token.pos), mark))
        return results
    return pat



def get_head(tok: Token, sentence: list[Token]) -> Token:
    if tok.gov < len(sentence):
        return sentence[tok.gov]
    else:
        return tok

def get_children(tok_i: int, sentence: list[Token]) ->  dict[str, list[Token]]:
    result = defaultdict(list)
    for tok in sentence:
        if tok.gov == tok_i:
            result[tok.dep].append(tok)
    return result

PATTERNS = [
        not_so_simple_rel("v -obj-> n", "VERB", "obj","NOUN"),
        not_so_simple_rel("n <-nsubj- v", "VERB", "nsubj", "NOUN"),
        not_so_simple_rel("n -nmod-> n", "NOUN","nmod", "NOUN"),
        marked_rel("_xcomp", "VERB", "xcomp","VERB"),
        case_rel("_iobj", "VERB", "obl","NOUN"),
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

    pred2arg_counts = defaultdict(Counter)
    arg2pred_counts = defaultdict(Counter)

    print("prédicat", "", "", "argument", "", "mesures", sep="\t")
    print("catégorie", "lemme", "relation", "catégorie", "lemme", "mesures", sep="\t")
    for m,i in counter.items():
        print(m.pos[0], m.lemmes[0], m.relation, m.pos[1], m.lemmes[1], i, sep="\t")
        pred2arg_counts[f"{m.lemmes[0]} {m.relation}"][m.lemmes[1]] += i
        arg2pred_counts[m.lemmes[1]][f"{m.lemmes[0]} {m.relation}"] += i

    return counter
                  

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
