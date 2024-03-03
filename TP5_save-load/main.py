'''
Created on Thu Feb 29 19:47:10 2024
@author: AUGUSTYN Patricia

Attention 1 : Si la commande ne fonctionne pas, réécrivez là manuellement car il est possible que certains caractères se copient/collent mal ;)
Attention 2 : Si vous souhaitez utiliser le module feedparser, faites en sorte d'avoir le temps car c'est long


Voici un petit manuel sur comment utiliser cette fonction :

1) Si vous voulez afficher tout votre corpus :
        python3 main.py --etree --corpus ./Corpus-asp/
        python3 main.py --re --corpus ./Corpus-asp/
        python3 main.py --feedparser --corpus ./Corpus-asp/

2) Si vous voulez filtrer sur les dates : vous avez l'option --date-debut et --date-fin
        python3 main.py --etree --corpus ./Corpus-asp/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100"
        python3 main.py --re --corpus ./Corpus-asp/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100"
        python3 main.py --feedparser --corpus ./Corpus-asp/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100"


3) Pour lancer le script avec filtrage sur les dates et sur les category:
    python3 main.py --etree --corpus ./Corpus-asp/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100" --category "Voyage"
    python3 main.py --re --corpus ./Corpus-asp/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100" --category "Culture"
    python3 main.py --feedparser --corpus ./Corpus-asp/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100" --category "Musique"

'''
import argparse
from rss_filtrage import parcourir_corpus, choix_filtrage, afficher_resultats
from datastructures import save_pickle, load_pickle
from pathlib import Path

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


    args = parser.parse_args()
    corpus = parcourir_corpus(args.corpus, args)
    corpus_choisi = choix_filtrage(corpus, args)

    save_pickle(corpus_choisi, Path("corpus.xml"))
    loaded_corpus = load_pickle(Path("corpus.xml"))


    data = []
    for item in corpus_choisi:
        guid = item.get('guid', '')
        title = item.get('title', '')
        link = item.get('link', '')
        description = item.get('description', '')
        pubdate = item.get('pubdate', '')
        category = item.get('category', [])

        # Pour éviter les erreurs de type : str(cell) if _isnumber(cell) else _type(cell, numparse)(cell) NoneType takes no arguments
        formatted_guid = str(guid) if guid is not None else ""
        formatted_title = str(title) if title is not None else ""
        formatted_link = str(link) if link is not None else ""
        formatted_description = str(description) if description is not None else ""
        formatted_pubdate = str(pubdate) if pubdate is not None else ""
        formatted_category = str(category) if category is not None else ""

        # Voici le format de notre requête
        data.append([{args.category: formatted_category},formatted_guid, formatted_title, formatted_link, formatted_description, formatted_pubdate])

        #data.append([{args.category: formatted_category}, {"GUID": formatted_guid, "Titre": formatted_title, "Lien": formatted_link, "Description": formatted_description, "Date de publication": formatted_pubdate}])
    # Affichage des données
    afficher_resultats(data,args)

if __name__ == "__main__":
    main()

