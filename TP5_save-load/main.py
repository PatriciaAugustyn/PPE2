'''
Created on Thu Feb 29 19:47:10 2024
@author: AUGUSTYN Patricia
# -*- coding: utf-8 -*-

Voici un petit manuel sur comment utiliser cette fonction (ATTENTION: l'exécution prend du temps):

1) Si vous voulez afficher tout votre corpus :
        python3 main.py --etree --corpus ./Corpus-asp/
        python3 main.py --re --corpus ./Corpus-asp/
        python3 main.py --feedparser --corpus ./Corpus-asp/

2) Si vous voulez filtrer sur les dates : vous avez l'option --date-debut et --date-fin
        python3 main.py --etree --corpus ./Corpus-asp/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb    2024 21:30:09 +0100"
        python3 main.py --re --corpus ./Corpus-asp/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100"
        python3 main.py --feedparser --corpus ./Corpus-asp/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100"

3) Pour lancer le script avec filtrage sur les dates et sur les category:
    python3 main.py --etree --corpus ./Corpus-asp/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100" --category "Voyage"
    python3 main.py --re --corpus ./Corpus-asp/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100" --category "Culture"
    python3 main.py --feedparser --corpus ./Corpus-asp/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100" --category "Musique"

4) Pour lancer le script et sauvegarder le résultat dans un fichier au format pickle:
	python3 main.py --etree --corpus ./Corpus-asp/ --save-pickle ./corpus.pkl

5) Pour charher le chargement des données à partir du fichier au format pickle:
python3 main.py --etree --corpus ./Corpus-asp --load-pickle ./corpus.pkl

Important: les arguments "--etree --corpus ./Corpus-asp" sont présents ici uniquement en raison de la
logique du code précedant. En réalité, ils ne sont pas nécessaires pour charger les données depuis un fichier
au format pickle. Pour éviter d'avoir à ajouter ces arguments à chaque fois que nous exécutons le code, il
faut modifier la fonction "parcourir_corpus".

6/ Pour exécuter le script qui sauvegardera le résultat de filtrage dans le fichier XML nommé corpus.xml:
python3 main.py --etree --corpus ./Corpus-asp/ --save-xml ./corpus.xml

7/ Pour exécuter le script qui chargera le corpus à partir du fichier XML nommé corpus.xml:
python3 main.py --load-xml ./corpus.xml --etree

Important: l'argument "--etree" est présent ici uniquement en raison de la
logique du code précedant. Pour éviter d'avoir à ajouter des arguments qui ne servent à rien à chaque fois que nous exécutons le code, il faut modifier la fonction "parcourir_corpus".

8/ Pour exécuter le script qui sauvegardera le résultat de filtrage dans le fichier json nommé corpus.json:
python3 main.py --etree --corpus ./Corpus-asp/ --save-json ./corpus.json

9/ Pour exécuter le script qui chargera le corpus à partir du fichier json nommé corpus.json:
python3 main.py --load-json ./corpus.json --etree

(la même remarque que pour l'exemple numéro 7)
'''

import argparse
from datastructures import Corpus, Item
from pathlib import Path
from rss_filtrage import parcourir_corpus, choix_filtrage, afficher_resultats
from XML_save_load import save_xml, load_xml
from PKL_save_load import save_pickle, load_pickle
from JSON_save_load import save_json, load_json

def main():
    parser = argparse.ArgumentParser(description="Un script qui lit le fichier xml dont le chemin est donné en argument, et qui retourne le texte et les métadonnées des item du flux RSS.", usage='use "python %(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter, epilog="Merci d'avoir lu notre manuel ! Passez une excellente journée/soirée !")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--re', action='store_true', help="Utilisez cette option pour que le fichier xml soit parsé avec RegEx")
    group.add_argument('--etree', action='store_true', help="Utilisez cette option pour que le fichier xml soit parsé avec etree")
    group.add_argument('--feedparser', action='store_true', help="Utilisez cette option pour que le fichier xml soit parsé avec feedparser")
    parser.add_argument('--corpus', metavar='CORPUS_PATH', help="Chemin vers le répertoire contenant les fichiers XML à traiter.")
    parser.add_argument('--date', action='store_true', help="Précisez cette option pour filtrer les résultats par date.")
    parser.add_argument('--date-debut', metavar='DATE', help="La date de début pour filtrer les résultats.")
    parser.add_argument('--date-fin', metavar='DATE', help="La date de fin pour filtrer les résultats.")
    parser.add_argument('--category', metavar='CATEGORY', help="Précisez la <category> selon laquelle vous souhaitez filtrer les résultats")
    parser.add_argument('--save-pickle', metavar='SAVE_PICKLE', help="Enregistrez le corpus au format pickle.")
    parser.add_argument('--load-pickle', metavar='LOAD_PICKLE', help="Chargez le corpus à partir d'un fichier pickle.")
    parser.add_argument('--save-xml', metavar='SAVE_XML', help="Enregistrez le corpus au format XML.")
    parser.add_argument('--load-xml', metavar='LOAD_XML', help="Chargez le corpus à partir d'un fichier XML.")
    parser.add_argument('--save-json', metavar='SAVE_JSON', help="Enregistrez le corpus au format json.")
    parser.add_argument('--load-json', metavar='LOAD_JSON', help="Chargez le corpus à partir d'un fichier json.")

    args = parser.parse_args()

    if args.load_xml:
        corpus = load_xml(args.load_xml)
    elif args.load_pickle:
        corpus = load_pickle(args.load_pickle)
    elif args.load_json:
        corpus = load_json(Path("corpus.json"))
    else:
        corpus = parcourir_corpus(args.corpus, args)
        corpus = choix_filtrage(corpus, args)

    if args.save_xml:
        save_xml(corpus, args.save_xml)
        print("Le corpus a été enregistré sous {}".format(args.save_xml))
    elif args.save_pickle:
        save_pickle(corpus, args.save_pickle)
        print(f"Le corpus a été enregistré sous {args.save_pickle}")
    elif args.save_json:
        corpus = parcourir_corpus(args.corpus, args)
        corpus_choisi = choix_filtrage(corpus, args)
        save_json(corpus_choisi, Path("corpus.json"))
        print(f"Le corpus a été enregistré sous {args.save_json}")
    else:
        afficher_resultats(corpus, args)

if __name__ == "__main__":
    main()
