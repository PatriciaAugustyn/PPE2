#parse_csv.py
import pandas as pd
import re
import sys

#pour lancer, il faut ajouter le nom de csv comme argument
#la commande précise "python parse_csv.py result_pattern.csv > result.csv"
#on a sauvegardé les résultats sur result.csv

# Vérifie si le nom du fichier est fourni en argument
if len(sys.argv) < 2:
    print("Usage: python parse_csv.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

# Lit le fichier CSV
df = pd.read_csv(filename, header=None, delimiter='\t', names=['Match', 'Frequency'])

predicate_counts = {}

pattern = re.compile(r"Match\(rule='(\w+)-(\w+)-(\w+)', lemmes=\(([^()]+)\)\)")

# Itère à travers chaque ligne du DataFrame
for index, row in df.iterrows():
    # Extraction des données en utilisant des expressions régulières
    match = pattern.match(row['Match'])
    if match:
        cat1, rel, cat2 = match.group(1), match.group(2), match.group(3)
        print(rel)
        lemmes = match.group(4).split(", ")
        # Clé pour identifier les prédicats
        key = (cat1, rel)
        # Si la clé n'est pas dans le dictionnaire, l'initialise avec une liste vide
        if key not in predicate_counts:
            predicate_counts[key] = []
        # Ajoute l'argument à la liste
        predicate_counts[key].append(lemmes[-1])
#print(predicate_counts)

# Initialise les listes pour stocker les données pour la table finale
final_predicates = []
final_arguments = []
final_measures = []

# Itère à travers les comptes de prédicats
for key, arguments in predicate_counts.items():
    predicate, relation = key
    print(relation)
    argument_counts = pd.Series(arguments).value_counts().to_dict()
    for argument, frequency in argument_counts.items():
        predicate_lemma = key[0]
        final_predicates.append(predicate_lemma)
        final_arguments.append(argument)
        final_measures.append(frequency)

result_df = pd.DataFrame({
    'Prédicat Catégorie': [pred[0] for pred in final_predicates],
    'Lemme': final_predicates,
    'Relation': relation,
    'Argument Catégorie': 'N',
    'Lemme': final_arguments,
    'Mesures Fréquence': final_measures
})

print(result_df)