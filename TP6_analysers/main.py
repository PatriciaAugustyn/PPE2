import argparse
from pathlib import Path
from datetime import datetime
import os
from datastructures import *
from rss_parcours import *


"""
utilisation :
python main.py re/etree/feedparser <xml_corpus> --source <source> --category <category> --date_debut <date_debut> --date_fin <date_fin> --save_corpus <format=filename>
ex: python3 main.py etree ../TP4/ressources/2024/01/26 --source 'BFMTV' --category 'Musique' --date_debut 23-01-2024 --date_fin 25-01-2024 --save_corpus pickle=corpus_filtered.pickle

load_corpus :
python main.py --load_corpus <format=filename> re/etree/feedparser --source <source> --category <category> --date_debut <date_debut> --date_fin <date_fin> 
ex : python3 main.py etree --load_corpus pickle=corpus_filtered.pickle --date_fin 23-01-2024

load_corpus + save_corpus :
python main.py --load_corpus <format=filename> re/etree/feedparser --source <source> --category <category> --date_debut <date_debut> --date_fin <date_fin> --save_corpus <format=filename>
ex : python3 main.py etree --load_corpus pickle=corpus_filtered.pickle --date_fin 23-01-2024 --save_corpus pickle=23_01_2024.pickle
"""

def parseur(): 
    parser = argparse.ArgumentParser(
        description="Retourne le texte et les métadonnées des <item/> du flux RSS file"
        )
    parser.add_argument(
        "methode", 
        choices=['re', 'etree', 'feedparser'],
        help="Choisir une méthode : re/etree/feedparser"
        )
    parser.add_argument(
        "xml_corpus",
        type=Path,
        nargs="?",
        help="Chemin du corpus xml"
        )
    
    parser.add_argument("--source", choices=["BFMTV", "Libération", "France info", "Le Figaro", "Blast", "Elucid"], help="Filtrer par source", default=None)
    parser.add_argument("--category", help="Filtrer par catégorie", default=None)

    parser.add_argument(
        "--date_debut",
        nargs="?",
        type=lambda d: datetime.strptime(d, "%d-%m-%Y").date(),
        help="Les articles après cette date inluse (JJ-MM-AAAA)",
        default=None
        )
    parser.add_argument(
        "--date_fin",
        nargs="?", 
        type=lambda d: datetime.strptime(d, "%d-%m-%Y").date(), 
        help="Les articles avant cette date incluse(JJ-MM-AAAA)",
        default=None
        )

    parser.add_argument("--load_corpus", help="Load filtered corpus from xml, json or pickle file (xml/json/pickle=filename)", default=None)
    parser.add_argument("--save_corpus", help="Save filtered corpus to  xml, json or pickle file (xml/json/pickle=filename)", default=None)
    
    args = parser.parse_args()
    return args

def main():
    args = parseur()
    
    if args.load_corpus:
        if "=" in args.load_corpus:
            print(args.load_corpus)
            load_format, load_filename = args.load_corpus.split('=')
            if load_format == 'xml':
                filtered_corpus = load_xml(Path(load_filename))
                pass
            elif load_format == 'json':
                filtered_corpus = load_json(Path(load_filename))
            elif load_format == 'pickle':
                filtered_corpus = load_pickle(Path(load_filename))

            items_filtrés_globaux = []
            for item in filtered_corpus:
                # Appliquer les filtres de source, date et catégorie
                if args.source and not filtre_source(item, args.source):
                    continue
                
                if args.date_debut and args.date_fin:
                    if not filtre_date(item, args.date_debut, args.date_fin):
                        continue
                elif args.date_debut:
                    if not filtre_date(item, args.date_debut):
                        continue
                elif args.date_fin:
                    if not filtre_date(item, None, args.date_fin):
                        continue
            
                if args.category: 
                    if not filtre_category(item, args.category):
                        continue

                items_filtrés_globaux.append(item)
        else:
            print(f"Erreur : Utilisez la syntaxe 'format=chemin' ")
            return

    else:

        corpus = Corpus(args.xml_corpus)
        items_filtrés_globaux = []
        titres_vus = []
        
        #EXCEPTION POUR GERER SI ON APPELLE UNIQUEMENT UN FICHIER
        if os.path.isfile(args.xml_corpus):
            fichiers_uniques = [Path(args.xml_corpus)]
        elif os.path.isdir(args.xml_corpus):
            fichiers_uniques = corpus.iterate_pathlib_glob()
        else:
            print("Le chemin spécifié n'est ni un fichier ni un répertoire valide.")
            return    

        for chaque_fichier in fichiers_uniques :
            
            if args.methode == 're':
                dico = corpus.read_rss_re(chaque_fichier)
            elif args.methode == 'etree':
                dico = corpus.read_rss_etree(chaque_fichier)
            elif args.methode == 'feedparser':
                dico = corpus.read_rss_feedparser(chaque_fichier)
            else:
                raise ValueError("Méthode invalide. Veuillez spécifier : re / etree / feedparser")

            #on se sert des variables qu'on a créées avant !
            for item in dico:
                # Vérifier si item est un dictionnaire
                if isinstance(item, dict):
                    titre = item.get('title')
                    if titre in titres_vus:
                        continue
                
                    # Si le titre n'est pas dans la liste des titres vus, l'ajouter et ajouter l'article aux articles filtrés
                    titres_vus.append(titre)
        
                    if args.source and not filtre_source(item, args.source):
                        continue

                    # Appliquer les autres filtres
                    if args.date_debut and args.date_fin:
                        if not filtre_date(item, args.date_debut, args.date_fin):
                            continue
                    elif args.date_debut:
                        if not filtre_date(item, args.date_debut):
                            continue
                    elif args.date_fin:
                        if not filtre_date(item, None, args.date_fin):
                            continue
            
                    if args.category: #on lance le filtre de catégorie
                        if not filtre_category(item, args.category):
                            continue

                    items_filtrés_globaux.append(item)
                    
                else:
                    print("Item n'est pas un dictionnaire ici")

    if args.save_corpus:
        if '=' in args.save_corpus:
            save_format, save_filename = args.save_corpus.split('=')
            if save_format == 'xml':
                save_xml(items_filtrés_globaux, Path(save_filename))
                pass  
            elif save_format == 'json':
                save_json(items_filtrés_globaux, Path(save_filename))
                pass   
            elif save_format == 'pickle':
                save_pickle(items_filtrés_globaux, Path(save_filename))
            else:
                print("Format de sauvegarde invalide. Les formats valides sont : xml, json, pickle")
        else:
            print("Format de sauvegarde invalide. Utilisez la syntaxe 'format=chemin'.")

    for item in items_filtrés_globaux:
        print(item)
            
if __name__ == '__main__':
    main()