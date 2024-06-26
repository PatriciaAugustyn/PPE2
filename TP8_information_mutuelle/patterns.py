#python3 patterns.py -l json ./corpus_analyzed.json
from datastructures import Token, Item, Match, name2loader
from collections import defaultdict, Counter
import argparse
import json
import math
import csv

def complex_rel(rule_name: str, pos1: str, deprel1: str, pos2: str, deprel2: str, pos3: str):
    def pat(sentence: list[Token]) -> list[Match]:
        results = []
        for token in sentence:
            if token.pos == pos3 and token.dep == deprel2:
                mid_i = token.gov
                if mid_i < len(sentence):
                    mid_token = sentence[mid_i]
                    if mid_token.pos == pos2 and mid_token.dep == deprel1:
                        head_i = mid_token.gov
                        if head_i < len(sentence):
                            head_token = sentence[head_i]
                            if head_token.pos == pos1:
                                results.append(Match(rule_name, (head_token.lemma, mid_token.lemma, token.lemma)))
        return results
    return pat

def simple_rel(rule_name: str, pos1: str, deprel: str, pos2: str):
    def pat(sentence: list[Token]) -> list[Match]:
        results = []
        for token in sentence:
            if token.pos == pos2 and token.dep == deprel:
                head_i = token.gov
                if head_i < len(sentence):
                    head_token = sentence[head_i]
                    if head_token.pos == pos1:
                        results.append(Match(rule_name, (head_token.lemma, token.lemma)))
        return results
    return pat

def calculate_cooccurrences(matches):
    predicate_counts = defaultdict(int)
    argument_counts = defaultdict(int)
    cooccurrences = defaultdict(int)

    for match in matches:
        predicate = match.lemmes[0]
        argument = match.lemmes[1]
        predicate_counts[predicate] += 1
        argument_counts[argument] += 1
        cooccurrences[(predicate, argument)] += 1

    return predicate_counts, argument_counts, cooccurrences

def calculate_mutual_information(predicate_counts, argument_counts, cooccurrences, total_matches):
    mutual_information_results = defaultdict(float)

    for (predicate, argument), cooccur_count in cooccurrences.items():
        p_predicate = predicate_counts[predicate] / total_matches
        p_argument = argument_counts[argument] / total_matches
        p_cooccur = cooccur_count / total_matches

        if p_cooccur > 0:
            mi = math.log2(p_cooccur / (p_predicate * p_argument))
            mutual_information_results[(predicate, argument)] = mi

    return mutual_information_results

PATTERNS = [
        simple_rel("v -obj-> n", "VERB", "obj","NOUN"),
        simple_rel("n <-nsubj- v", "VERB", "nsubj", "NOUN"),
        simple_rel("n -nmod-> n", "NOUN","nmod", "NOUN"),
        complex_rel("v -xcomp-> v -mark-> adp", "VERB", "xcomp", "VERB", "mark", "ADP"),
        complex_rel("n -amod-> adj -nmod-> n", "NOUN", "amod", "ADJ", "nmod", "NOUN"),
        complex_rel("v -advmod-> adv -nmod-> n", "VERB", "advmod", "ADV", "nmod", "NOUN"),
        complex_rel("v -obl-> n -case-> adp", "VERB", "obl", "NOUN", "case", "ADP")
        ]

def main(input_file, load_serialized):
    DEMO_HARD_LIMIT = 1000
    load_corpus = name2loader[load_serialized]
    corpus = load_corpus(input_file)

    corpus.items = corpus.items[:DEMO_HARD_LIMIT]
    all_matches = []
    for item in corpus.items:
        for sentence in item.analysis:
            for pattern in PATTERNS:
                matches = pattern(sentence)
                all_matches.extend(matches)

    predicate_counts, argument_counts, cooccurrences = calculate_cooccurrences(all_matches)
    im_resultats = calculate_mutual_information(predicate_counts, argument_counts, cooccurrences, len(all_matches))

    # Writing to CSV with the specified headers
    with open('resultats.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['catégorie_prédicat', 'lemme_prédicat', 'relation', 'catégorie_argument', 'lemme_argument', 'fréquence', 'IM']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        
        for match in all_matches:
            relation = match.rule.split()[1]
            predicate_category = match.rule.split()[0]
            predicate_lemma = match.lemmes[0]
            argument_category = match.rule.split()[-1]
            argument_lemma = match.lemmes[1]
            frequency = cooccurrences[(predicate_lemma, argument_lemma)]
            im_value = im_resultats[(predicate_lemma, argument_lemma)]

            writer.writerow([predicate_category, predicate_lemma, relation, argument_category, argument_lemma, frequency, im_value])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input file, a serialized corpus.")
    parser.add_argument("-l", "--load-serialized", choices=sorted(name2loader.keys()))

    args = parser.parse_args()
    main(input_file=args.input_file, load_serialized=args.load_serialized)
