from datastructures import Token, Item, Match, name2loader, name2saver
import csv
from collections import Counter, defaultdict
import math
""" python patterns.py analyzed_stanza-corpus.json -l json """

""" def pat_noun(sentence: list[Token]) -> list[Match]:
    rule_name = "noun"
    results = []
    for token in sentence:
        if token.pos == "NOUN":
            results.append(Match(rule_name, (token.lemma,)))
    return results """




""" def pat_verb_obj_noun(sentence: list[Token]) -> list[Match]:
    rule_name = "V -obj-> N"
    results = []
    for token in sentence:
        if token.pos == "NOUN" and token.dep == "obj":
                head_i = token.gov
                for i, head in enumerate(sentence):
                    if i == head_i and head.pos == "VERB":
                        results.append(Match(rule_name, (head.lemma, token.lemma)))
    return results """

def segment_into_sentences(tokens):
    sentences = []
    current_sentence = []
    for token in tokens:
        if token.id == 1 and current_sentence:
            sentences.append(current_sentence)
            current_sentence = [token]
        else:
            current_sentence.append(token)
    if current_sentence:  # Ajouter la dernière phrase si elle existe
        sentences.append(current_sentence)
    return sentences

def simple_rel(rule_name: str,
                pos1: str,
                deprel: str,
                pos2: str
                ):
    def pat(sentence: list[Token]) -> list[Match]:
        results = []
        # print(sentence)
        for token in sentence:
            if token.pos == pos2 and token.dep == deprel:
                head_i = token.gov_id # head_i = indice de la tête (governor) du token
                if head_i < len(sentence)+1: # si head_i est inf à la longueur de la phrase. head_i représente l'indice de la tête
                    head = sentence[head_i-1] # head = ? expl : Token(id=10, shape='pas', lemma='pas', pos='ADV', dep='advmod', gov='existe', head_id=9)
                    if head.pos == pos1 and head.id == token.gov_id: # Vérification de la relation entre les tokens
                        results.append(Match(rule_name, (head.lemma, token.lemma), (head.pos, token.pos), token.dep))        #print(results)
        return results
    return pat 

def complex_rel(rule_name: str,
                pos1: str,
                deprel1: str,
                pos2: str,
                deprel2: str,
                pos3: str
                ):
    def pat(sentence: list[Token]) -> list[Match]:
        results = []
        for token1_index, token1 in enumerate(sentence):
            if token1.pos == pos1:
                for token2_index, token2 in enumerate(sentence):
                    if token2.gov_id == token1_index+1 and token2.dep == deprel1 and token2.pos == pos2:
                        for token3_index, token3 in enumerate(sentence):
                            if token3.gov_id == token2_index+1 and token3.pos == pos3:
                                results.append(Match(rule_name, (token2.lemma, token3.lemma), (token2.pos, token3.pos), token3.dep))        #print(results)
        return results
    return pat

PATTERNS = [
    simple_rel("v-obj-n", "VERB", "obj","NOUN"),
    simple_rel("v-nsubj-n", "VERB", "nsubj", "NOUN"),
    simple_rel("n-nmod-n", "NOUN","nmod", "NOUN"),
    complex_rel("v-xcomp-v-mark-adp", "VERB", "xcomp", "VERB", "mark", "ADP"),
    complex_rel("v-nsubj-n-amod-adj", "VERB", "nsubj", "NOUN", "amod", "ADJ"),
    complex_rel("v-obl:mod-n-case-adp", "VERB", "obl:mod", "NOUN", "case", "ADP"),
    complex_rel("n-conj-n-cc-cconj", "NOUN", "conj", "NOUN", "case", "CCONJ")
]

# ne fonctionne pas, juste la ligne des titres s'affiche
def info_mutuelle(results, output_file):
    # en sortie on souhaite un fichier csv
    with open("information_mutuelle.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerow(["predicate", "lemma_predicate", "relation", "cat/argument", "lemma_argument", "Mesure"])
    
        for elem in results:
            #print(elem)
            sep_element = elem.rule.split("-")
            category_predicate = sep_element[0]
            relation = sep_element[1]
            category_argument = sep_element[2]
            lemma_predicate = elem.lemma[0]
            lemma_argument = elem.lemma[1]
            writer.writerow([category_predicate, lemma_predicate, relation, category_argument, lemma_argument, "Mesure"])
    
    #print(information_mutuelle)


"""     for pred, arg_counts in pred2arg_counts.items():
        for arg, count in arg_counts.items():
            pmi = count * (count / (pred2arg_counts[pred][arg] * arg2pred_counts[arg][pred]))
            print(pmi) """


def main(input_file, load_serialized=None):
    DEMO_HARD_LIMIT = 1000 # pour faire une démonstration au besoin

    load_corpus = name2loader[load_serialized or "json"]

    corpus = load_corpus(input_file)
    #print(corpus)
    corpus.items = corpus.items[:DEMO_HARD_LIMIT]  # commenter pour traiter tout le corpus
    #print(corpus.items)
    counter = Counter()

    for item in corpus.items:
        for tokens in item.analysis: 
            sentences = segment_into_sentences(tokens)
            for sentence in sentences:
                for pattern in PATTERNS:
                    matches = pattern(sentence)
                    # print(matches)
                    counter += Counter(matches)
    
    pred2arg_counts = defaultdict(Counter)
    arg2pred_counts = defaultdict(Counter)

    with open('result_pattern.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["predicate", "lemma_predicate", "relation", "cat/argument", "lemma_argument", "Mesure", "IM"])

        for m, i in counter.items():
            pred2arg_counts[(m.pos[0], m.lemmes[0], m.relation)][m.lemmes[1]] += i
            arg2pred_counts[m.lemmes[1]][(m.pos[0], m.lemmes[0], m.relation)] += i

        for pred, arg_counts in pred2arg_counts.items():
            for arg, count in arg_counts.items():
                pred_count = sum(pred2arg_counts[pred].values())
                arg_count = sum(arg2pred_counts[arg].values())

                total_token = sum(counter.values())
                pmi = math.log2((count / total_token) / ((pred_count / total_token) * (arg_count / total_token)))

                pos_predicate, lemma_predicate, relation = pred
                #pos_argument, lemma_argument = arg


                writer.writerow([pos_predicate, lemma_predicate, relation, arg, count, pmi])

    return counter

"""         for pred, arg_counts in pred2arg_counts.items():
            for arg, count in arg_counts.items():
                pred_count = sum(pred2arg_counts[pred].values())
                arg_count = sum(arg2pred_counts[arg].values())

                total_token = sum(counter.values())
                pmi = math.log2((count / total_token) / ((pred_count / total_token) * (arg_count / total_token)))

                pos_predicate, lemma_predicate, relation = pred

                writer.writerow([pos_predicate, lemma_predicate, relation, arg, count, pmi]) """






"""      # appel de la fonction info_mutuelle
    info_mutuelle(counter.most_common(), "information_mutuelle.csv") """

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
