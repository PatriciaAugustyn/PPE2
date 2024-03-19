#python3 patterns.py test_dep.json -o test_pattern.csv -p <r1>,<r1, r2>,<r1, r2, r3>

import argparse
import csv
from datastructures import *

def extract_verb_obj(corpus: Corpus):
    pattern = "verb --obj-> noun"
    instances = {}
    for item in corpus.items:
        for token in item.analysis:
            for dep in token.dependencies:
                if dep.dependencies == 'obj' and token.pos == 'VERB' and dep.pos == 'NOUN':
                    instance = (token.lemma, dep.lemma)
                    instances[instance] = instances.get(instance, 0) + 1
    return pattern, instances

def extract_verb_subj(corpus: Corpus):
    pattern = "verb --nsubj-> noun"
    instances = {}
    for item in corpus.items:
        for token in item.analysis:
            for dep in token.dependencies:
                if dep.dependencies == 'nsubj' and token.pos == 'VERB' and dep.pos == 'NOUN':
                    instance = (token.lemma, dep.lemma)
                    instances[instance] = instances.get(instance, 0) + 1
    return pattern, instances

def extract_noun_mod(corpus: Corpus):
    pattern = "noun --nmod-> noun"
    instances = {}
    for item in corpus.items:
        for token in item.analysis:
            for dep in token.dependencies:
                if dep.dependencies == 'nmod' and token.pos == 'NOUN' and dep.pos == 'NOUN':
                    instance = (token.lemma, dep.lemma)
                    instances[instance] = instances.get(instance, 0) + 1
    return pattern, instances

def save_to_file(pattern_instances, output_file):
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(['Pattern', 'Instance', 'Count'])
        for pattern, (pattern_str, instances) in pattern_instances.items(): 
            for instance, count in instances.items():
                writer.writerow([pattern_str, " -- ".join(instance), count])

def main(input_file, output_file=None, patterns=None):
    file_extension = Path(input_file).suffix.lower()
    if file_extension == '.json':
        corpus = load_json(input_file)
    elif file_extension == '.xml':
        corpus = load_xml(input_file)
    elif file_extension == '.pkl' or file_extension == '.pickle':
        corpus = load_pickle(input_file)
    else:
        raise ValueError("Unsupported file format. Please provide a .json, .xml, or .pickle file.")
    
    selected_patterns = patterns.split(',') if patterns else []
    pattern_instances = {}

    if 'r1' in selected_patterns or not patterns:
        pattern_instances['r1'] = extract_verb_obj(corpus)
    if 'r2' in selected_patterns or not patterns:
        pattern_instances['r2'] = extract_verb_subj(corpus)
    if 'r3' in selected_patterns or not patterns:
        pattern_instances['r3'] = extract_noun_mod(corpus)
    
    if output_file:
        save_to_file(pattern_instances, output_file)
    else:
        for pattern, (pattern_str, instances) in pattern_instances.items():
            print(f"Pattern: {pattern_str}, Instances and Counts:")
            for instance, count in instances.items():
                print(f"  {instance}: {count}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract specific dependency patterns from a corpus.")
    parser.add_argument("input_file", help="Input file path for the corpus to be analyzed.")
    parser.add_argument("-o", "--output_file", help="Output file path for saving the results.")
    parser.add_argument("-p", "--patterns", help="Comma-separated list of patterns to extract (r1, r2, r3). If not provided, all patterns will be extracted.")

    args = parser.parse_args()
    main(args.input_file, args.output_file, args.patterns)
