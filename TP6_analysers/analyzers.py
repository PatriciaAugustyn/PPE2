#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from trankit import Pipeline
from datastructures import *
from rss_reader import *
from rss_parcours import *
import os
import stanza
import spacy
from collections import namedtuple



def load_spacy():
    return spacy.load("fr_core_news_sm")


def analyse_spacy(item, nlp):
    result = nlp((item.title or "") + "\n" + (item.description or ""))
    output = []
    for token in result:
        output.append(Token(token.text, token.lemma_, token.pos_))
    item.tokens = output
    return item



def analyse_stanza(item : Item, nlp):
    
    doc = nlp((item.title or "") + "\n" + (item.description or ""))
    result = []
    for sentence in doc.sentences:
        for word in sentence.words:
            result.append(Token(word.text, word.lemma, word.pos))
    item.tokens=result
    return item








# Fonction pour charger le modèle Trankit pour le français
def load_trankit_model():
    nlp = Pipeline(lang='french')
    # et ajouter les autres français ?
    nlp.add('french-partut')
    nlp.add('french-sequoia')
    return nlp



# Fonction pour enrichir un objet Item avec les résultats de l'analyse
def analyze_trankit(item, nlp):
    #nlp = load_trankit_model()
    text = ''
    tokens_list = []
    if item.title:
        text = text + item.title + "\n"
    if item.description:
        text = text + item.description

    data = nlp(text)

    # Parcourir chaque phrase dans 'sentences'
    for sentence in data['sentences']:
        #tokens_sentence = []
        # Parcourir chaque token dans 'tokens'
        for token in sentence['tokens']:
            # Récupérer les valeurs 'text', 'lemma' et 'upos' pour chaque token ; et si ne trouve pas, alors on prend une chaine de caractère vide comme valeur
            #token_text = token['text']
            token_text = token.get('text', '')
            #token_lemma = token['lemma']
            token_lemma = token.get('lemma', '')
            #token_upos = token['upos']
            token_upos = token.get('upos', '')
            #tokens_sentence.append(Token(text=token_text, lemma=token_lemma, upos=token_upos))
            tokens_list.append(Token(forme=token_text, lemme=token_lemma, pos=token_upos))
    item.tokens = tokens_list

    return item





def main():
    # Définition des arguments en ligne de commande
    parser = argparse.ArgumentParser(description="Analyse d'un corpus sauvegardé")
    parser.add_argument("-t", "--tool", choices=["spacy", "stanza", "trankit"], help="Outil pour l'analyse")
    parser.add_argument("-i", "--input_file", required=True, type=str, help="Chemin vers le fichier contenant le corpus sauvegardé")
    parser.add_argument("-o", "--output_file", required=True, type=str, help="Chemin vers le fichier où sauvegarder le résultat de l'analyse")
    args = parser.parse_args()

    corpus = load(args.input_file)

    if args.tool == "spacy":
        nlp = load_spacy()
        for item in corpus.items:
            analyse_spacy(item, nlp)
    elif args.tool == "stanza":
        stanza.download('fr') 
        nlp = stanza.Pipeline(lang='fr', processors='tokenize,lemma,pos,ner')
        for item in corpus.items:
            analyse_stanza(item, nlp)
    elif args.tool == "trankit":
        nlp = load_trankit_model()
        for item in corpus.items:
            analyze_trankit(item, nlp)

    save(corpus, args.output_file)




if __name__ == '__main__':
    main()
