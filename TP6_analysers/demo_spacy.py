#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Attention cette fonction ne fonctionne pas avec .pkl

import spacy
import sys

if len(sys.argv) != 2:
    print("Utilisation : python3 demo_spacy.py <chemin_du_fichier>")
    sys.exit(1)

# Charger le contenu du fichier
fichier_path = sys.argv[1]
with open(fichier_path, 'r') as fichier:
    test = fichier.read()


nlp = spacy.load("fr_core_news_sm")

def return_token(sentence):
    doc = nlp(sentence)
    return [X.text for X in doc]

def return_token_sent(sentence):
    doc = nlp(sentence)
    return [X.text for X in doc.sents]

def return_POS_lemma(sentence):
    doc = nlp(sentence)
    return [(X.text, X.pos_, X.lemma_) for X in doc]

# Récupérer les résultats
tokens = return_token(test)
sentences = return_token_sent(test)
pos_lemma_tags = return_POS_lemma(test)

# Vous pouvez changer resultat_spacy.json en .xml ou .pkl et dans le print ;)
with open("resultat_spacy.json", 'w') as resultat_fichier:
    resultat_fichier.write("Etiquetage morpho-syntaxique et lemmatisation:\n")
    resultat_fichier.write("\t".join(["#", "Token", "POS", "Lemme"]) + "\n")
    for i, (token, pos, lemma) in enumerate(pos_lemma_tags):
        resultat_fichier.write(f"{i+1}\t{token}\t{pos}\t{lemma}\n")

print(f"Les résultats ont été enregistrés dans le fichier 'resultat_spacy.json' pour le fichier '{fichier_path}'.")
