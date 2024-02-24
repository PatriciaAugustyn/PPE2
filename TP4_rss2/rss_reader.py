import argparse, textwrap
import re
import xml.etree.ElementTree as ET
import feedparser
import os
import unicodedata

def lecture_fichier_flux_r1(path):
    '''Cette fonction permet de lire le fichier xml dont le chemin est donné en
    argument, et qui retourne le texte et les métadonnées des item du flux RSS.'''

    with open(path, "r", encoding="utf-8") as fichier:
        xml = fichier.read()

        # On veut cibler notre regex sur ce qui est seulement a l'intérieur des balises <title></title> et <description></description> : donc ()
        regex_titre = re.findall(r"<title>(.*)</title>", xml)
        regex_description = re.findall(r"<description>(.*)</description>", xml)

        # Les résultats : rendre la visualisation des données plus visible
        print("\nLe texte entre les balises <title></title> :\n")
        for titre in regex_titre:
            print(titre.strip())

        print("\nLe texte entre les balises <description></description> :\n")
        for description in regex_description:
            print(description.strip())

        # Bonus :
        regex_date = re.findall(r"<pubDate>(.*)</pubDate>", xml)
        regex_lien = re.findall(r"<link>(.*)</link>", xml)
        regex_categorie = re.findall(r"<category>(.*)</category>", xml)

        print("\nLe texte entre les balises <pubDate></pubDate> :\n")
        for date in regex_date:
            print(date.strip())

        print("\nLe texte entre les balises <link></link> :\n")
        for lien in regex_lien:
            print(lien.strip())

        print("\nLe texte entre les balises <category></category> :\n")
        for categorie in regex_categorie:
            print(categorie.strip())

def lecture_fichier_flux_r2(path):
     #doit donner le contenu des titres et descriptions
    #liste de titre/ liste de description et liste de méta donnée?
    tree = ET.parse(path)
    root = tree.getroot()
    title = []
    description =[]
    date = []
    category = []

    for channel in root.findall('channel'):
        for item in channel.findall('item'):
            date.append(item.findtext('pubDate'))
            title.append(item.findtext('title'))
            category.append(item.findtext('category'))
            description.append(item.findtext('description'))
        print(category)
    return channel, title, category, description

def lecture_fichier_flux_r3(path):
    try:
        feed = feedparser.parse(path)
        print("\nLe texte entre les balises <title></title> :\n")
        for entry in feed.entries:
            print(entry.title.strip())

        print("\nLe texte entre les balises <description></description> :\n")
        for entry in feed.entries:
            print(entry.description.strip())

        print("\nLe texte entre les balises <pubDate></pubDate> :\n")
        for entry in feed.entries:
            print(entry.published.strip())

        print("\nLe texte entre les balises <link></link> :\n")
        for entry in feed.entries:
            print(entry.link.strip())

        print("\nLe texte entre les balises <category></category> :\n")
        for entry in feed.entries:
            if 'tags' in entry:
                for tag in entry.tags:
                    print(tag.term.strip())

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")



# Modifier la valeur de retour par la fonction de r3 au format spécifié list[dict]

from datetime import datetime

def lecture_fichier_flux(path):
    try:
        # Parser le fichier RSS
        feed = feedparser.parse(path)

        # Initialisation de la liste pour stocker les données
        xmlData = []
        
        for entry in feed.entries:
            itemData = {}

            # Récupérer le titre si présent
            if 'title' in entry:
                itemData["titre"] = entry.title.strip()

            # Récupérer la description si présente
            if 'description' in entry:
                itemData["description"] = entry.description.strip()

            # Récupérer la date de publication si présente
            if 'published' in entry:
                try:
                    # Essayer de parser la date selon le premier format
                    format_date = "%a, %d %b %Y %H:%M:%S %z"
                    published_datetime = datetime.strptime(entry.published.strip(), format_date)
                    itemData["date"] = published_datetime
                except ValueError:
                    pass
                try:
                    # Essayer de parser la date selon le deuxième format
                    format_date = "%a, %d %b %Y %H:%M:%S %Z"
                    published_datetime = datetime.strptime(entry.published.strip(), format_date)
                    itemData["date"] = published_datetime
                except ValueError:
                    pass
            # Récupérer les catégories si présentes
            if 'tags' in entry:
                itemData["categories"] = []
                for tag in entry.tags:
                    itemData["categories"].append(tag.term.strip())

            if 'link' in entry:
                link = entry.link
                pattern = r'https?://(?:www\.)?(?:[^./]+\.)?([^./]+)\.'
                try:
                    source = re.match(pattern, link).group(1)
                except Exception as e:
                    link = feed.feed.link
                    pattern = r'https?://(?:www\.)?(?:[^./]+\.)?([^./]+)\.'
                    source = re.match(pattern, link).group(1)
                
                itemData["source"] = source
                
            # Ajouter les données de l'entrée à la liste
            xmlData.append(itemData)
        
        # Retourner les données
        return xmlData

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")



# Fonction s4-r1
def lister_fichiers_s4_r1(path:str, filted_by_date:dict):
    '''Cette fonction utilise le module os (notamment os.path et os.listdir, et proposera l'option de filtrer en fonction de la date (les articles parus depuis une date et/ou jusqu'à une date).Affiche les fichiers dans le dossier spécifié.
    '''

    # On va parcourir les fichier dans le dossier qu'on aura spécifié
    for filename in os.listdir(path):
            filepath = os.path.join(path, filename)

            if os.path.isdir(filepath):
                lister_fichiers_s4_r1(filepath, filted_by_date)

            else:
                xml = lecture_fichier_flux(filepath)
                # On va appliquer le filtre sur la date
                resultat = filtre_date(xml)

                if resultat:
                    # On va mettre à jout notre dictionnaire avec les résultat du filtre
                    filted_by_date.update(resultat)


def filtre(item: dict) -> bool:
    '''Fonction de filtre pour voir si un élément a une date ou non'''
    if "date" in item :
        return True
    else :
        return False

def filtre_date(rssFile:list):
    '''Cette fonction permet de filtrer les éléments qui ont une date en prenant en entrée une liste d'élément RSS'''

    # On initialise le dictionnaire qui nous servira en sortie
    filted_by_date = {}

    # On va parcourir tous les éléments dans la liste donnée
    for item in rssFile :

        # On va voir si l'élément a une date et l'ajouté dans notre dictionnaire
        if filtre(item):
            key_date = item["date"]
            if key_date not in filted_by_date:
                filted_by_date[key_date] = []
            filted_by_date[key_date].append(item)


        else :
            none_date = "Cette date est absente !"
            if none_date not in filted_by_date :
                filted_by_date[none_date] = []
            filted_by_date[none_date].append(item)
    return filted_by_date

# FIN DE s4-r1



# r2 use pathlib without glob()

from pathlib import Path

def folder_reader_r2(folder:str, corpus_filted:dict):
    path = Path(folder)
    for item in path.iterdir():
        if item.is_file():
            xmlData = lecture_fichier_flux(item)
            data_filted = filter_source(xmlData)
            corpus_filted.update(data_filted)
        elif item.is_dir():
            folder_reader_r2(item, corpus_filted)

def filtre_source(item: dict) -> bool:
    if "source" in item:
        return True
    else:
        return False


def filter_source(rssFile:list):
    filted_by_s = {}
    
    for item in rssFile:
        if filtre_source(item):
            key_s = item['source']
            if key_s not in filted_by_s:
                filted_by_s[key_s] = []
            filted_by_s[key_s].append(item)
        else:
            
            none_s = "None source"
            if none_s not in filted_by_s:
                filted_by_s[none_s] = []
            filted_by_s[none_s].append(item)
    
    return filted_by_s

# End of r2



# r3 use pathlib zith glob()

from pathlib import Path

def folder_reader_r3(folder:str):
    # Créer un objet Path à partir du chemin du dossier fourni
    try:
        path = Path(folder)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    # Initialiser un dictionnaire pour stocker les données filtrées par catégorie
    filted_all_cat = {}
    
    # Parcourir tous les fichiers XML dans le dossier et ses sous-dossiers
    for filePath in path.glob('**/*.xml'):
        # Lire les données XML à partir du fichier
        xmlData = lecture_fichier_flux(filePath)

        try:
            # Filtrer les données par catégorie
            filted_one_cat = filter_category(xmlData)
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

        # Mettre à jour le dictionnaire avec les données filtrées par catégorie
        filted_all_cat.update(filted_one_cat)

    return filted_all_cat

# Fonction pour vérifier si cet donne existe balise <category>
def filtre_category(item: dict) -> bool:
    if "categories" in item:
        return True
    else:
        return False
    
# Fonction pour filtrer les données par catégorie
def filter_category(rssFile:list):
    filted_by_cat = {}
    for item in rssFile:
        # Vérifier si l'élément contient la balise <category>
        if filtre_category(item):
            key_cat = tuple(item['categories'])
            # Ajouter l'élément au dictionnaire selon sa catégorie
            if key_cat not in filted_by_cat:
                filted_by_cat[key_cat] = []
            filted_by_cat[key_cat].append(item)
        else:
            # Si l'élément n'a pas de catégorie, l'ajouter à une catégorie spéciale
            none_cat = tuple(["None category"])
            if none_cat not in filted_by_cat:
                filted_by_cat[none_cat] = []
            filted_by_cat[none_cat].append(item)
    
    return filted_by_cat

# End of r3




def main():
    # Configuration du parser d'arguments en ligne de commande
    parser = argparse.ArgumentParser(description =textwrap.dedent('''Usage:
python rss_reader.py -m mode -r role -d date_début -f date_fin (pour r1) -s source (pour r2) -c category (pour r3)
Extrayez les informations clés d'un fichier .rss ou extrayez les informations clés de tous les fichiers .rss d'un dossier comme un corpus et flitrez-les par date, source ou catégorie.'''),
    usage='ustiliez "python %(prog)s --help" pour plus d\'information',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog=textwrap.dedent('''Merci d'avoir lu notre manuel !
Site de la répertoire <https://gitlab.com/plurital-ppe2-2024/groupe14/projet.git>'''))

    parser.add_argument("-m", "--mode", choices=["unique", "corpus"],
                        help=textwrap.dedent('''Deux modes sont disponibles ici:
    unique: pour ne lire qu'un seul fichier dans l'exercice rss 1
    corpus: pour lire tous les fichiers d'un dossier comme un corpus dans l'exercice rss 2.'''))
    
    parser.add_argument("-r", "--role", 
                        choices=["r1", "r2", "r3"], 
                        help=textwrap.dedent('''Les fonctions dont trois rôles différents sont responsables,
pour le modèle UNIQUE :
    r1 : extrait des informations à l'aide de re
    r2 : extrait des informations en utilisant etree
    r3 : extraction d'informations à l'aide de feedparser
Pour le schéma du corpus :
    r1 : utilisation du module os pour parcourir les fichiers et les trier par date
    r2 : utilisation du module pathlib pour parcourir les fichiers (sans utiliser la méthode glob()) et les trier par source
    r3 : utiliser le module pathlib pour parcourir les fichiers (en utilisant la méthode glob()) et les trier par catégorie'''))

    parser.add_argument('-d', '--date_debut', help='Heure de début. Sélectionnez l\'heure actuelle si c\'est la seule option possible. Format horaire: DD/MM/YYYY UTC±N', required=False)

    parser.add_argument('-f', '--date_fin', help='Heure de fin. Tout sélectionner de l\'heure de début à l\'heure de fin. Format horaire: DD/MM/YYYY UTC±N', required=False)

    parser.add_argument('-s', '--source', help='Source de l\'article. Insensible aux majuscules et minuscules.', required=False)

    parser.add_argument('-c', '--category', help='Catégorie de l\'article. Sensible aux majuscules et minuscules.', required=False)

    parser.add_argument("chemin", help="Il faut ajouter le chemin vers votre fichier XML ou doissier !")

    # Analyse des arguments
    args = parser.parse_args()
    path = args.chemin
    
    # Traitement en fonction du mode et du rôle spécifiés
    if args.mode == "unique":
        if args.role == "r1":
            if args.date_debut or args.date_fin or args.source or args.category:
                raise ValueError("Cette option n'est pas disponible ici !!!")
            lecture_fichier_flux_r1(path)
        elif args.role == "r2":
            if args.date_debut or args.date_fin or args.source or args.category:
                raise ValueError("Cette option n'est pas disponible ici !!!")
            lecture_fichier_flux_r2(path)
        elif args.role == "r3":
            if args.date_debut or args.date_fin or args.source or args.category:
                raise ValueError("Cette option n'est pas disponible ici !!!")
            lecture_fichier_flux_r3(path)
        else:
            raise ValueError("Veuillez préciser le rôle ;) ")
    elif args.mode == "corpus":
        if args.role == "r1":
            if args.source or args.category:
                raise ValueError("Cette option n'est pas disponible ici !!!")
            
            corpus_filtre_date = {}
            lister_fichiers_s4_r1(path, corpus_filtre_date)
            
            if args.date_debut:
                date_format = "%m/%d/%Y %H:%M:%SUTC%z"
                try:
                    date_debut = datetime.strptime(args.date_debut, date_format)
                except Exception as e:
                    print(f"Format d'heure incorrect : {e}")
                if args.date_fin :
                    try:
                        date_fin = datetime.strptime(args.date_fin, date_format)
                    except Exception as e:
                        print(f"Format d'heure incorrect : {e}")
                    index = 1
                    for key in corpus_filtre_date.keys():
                        
                        if key >= date_debut and key <= date_fin:
                            
                            for item in corpus_filtre_date.get(key):
                                print(f"\tItem {index}:")

                                if("titre" in item):
                                    titre = item["titre"]
                                    print(f"\t\tTitre : {titre}")
                                
                                if("description" in item):
                                    description = item["description"]
                                    print(f"\t\tDescription : {description}")
                                
                                if("date" in item):
                                    format_date = "%m/%d/%Y %H:%M:%SUTC%z"
                                    formatted_date = item["date"].strftime(format_date)
                                    print(f"\t\tDate : {formatted_date}")
                                
                                if("categories" in item):
                                    categories = item["categories"]
                                    print(f"\t\tCategories : {categories}")
                                index += 1
                else:
                    for key in corpus_filtre_date.keys():
                        index = 1
                        if key == date_debut:
                            
                            for item in corpus_filtre_date.get(key):
                                print(f"\tItem {index}:")

                                if("titre" in item):
                                    titre = item["titre"]
                                    print(f"\t\tTitre : {titre}")
                                
                                if("description" in item):
                                    description = item["description"]
                                    print(f"\t\tDescription : {description}")
                                
                                if("date" in item):
                                    format_date = "%m/%d/%Y %H:%M:%SUTC%z"
                                    formatted_date = item["date"].strftime(format_date)
                                    print(f"\t\tDate : {formatted_date}")
                                
                                if("categories" in item):
                                    categories = item["categories"]
                                    print(f"\t\tCategories : {categories}")
                                index += 1
            else:
                if args.date_fin :
                    raise ValueError("Veuillez préciser l'heure de début d'abord s.v.p;) ")
                else:
                    for key in corpus_filtre_date.keys():
                        print(f"Pour date {key} :")
                        index = 1
                        for item in corpus_filtre_date.get(key):
                            print(f"\tItem {index}:")

                            if("titre" in item):
                                titre = item["titre"]
                                print(f"\t\tTitre : {titre}")
                            
                            if("description" in item):
                                description = item["description"]
                                print(f"\t\tDescription : {description}")
                            
                            if("date" in item):
                                format_date = "%m/%d/%Y %H:%M:%SUTC%z"
                                formatted_date = item["date"].strftime(format_date)
                                print(f"\t\tDate : {formatted_date}")
                            
                            if("categories" in item):
                                categories = item["categories"]
                                print(f"\t\tCategories : {categories}")
                            index += 1
        elif args.role == "r2":
            if args.date_debut or args.date_fin or args.category:
                raise ValueError("Cette option n'est pas disponible ici !!!")
            
            corpus_filtre_s = {}
            folder_reader_r2(path, corpus_filtre_s)

            if args.source:
                # blast-info
                # elucid
                # bfmtv <=> BFMTV
                # francetvinfo <=>
                # lefigaro <=> Le Figaro
                # liberation <=> Libération
                input_string = args.source
                normalized_string = unicodedata.normalize('NFKD', input_string)
                processed_string = normalized_string.encode('ASCII', 'ignore').decode('utf-8')
                key = processed_string.lower().replace(' ', '')
                index = 1
                for item in corpus_filtre_s.get(key):
                    print(f"\tItem {index}:")

                    if("titre" in item):
                        titre = item["titre"]
                        print(f"\t\tTitre : {titre}")
                    
                    if("description" in item):
                        description = item["description"]
                        print(f"\t\tDescription : {description}")
                    
                    if("date" in item):
                        format_date = "%m/%d/%Y %H:%M:%SUTC%z"
                        formatted_date = item["date"].strftime(format_date)
                        print(f"\t\tDate : {formatted_date}")
                    
                    if("categories" in item):
                        categories = item["categories"]
                        print(f"\t\tCategories : {categories}")
                    index += 1
            else:
                for key in corpus_filtre_s.keys():
                    print(f"Pour source {key} :")
                    index = 1
                    for item in corpus_filtre_s.get(key):
                        print(f"\tItem {index}:")

                        if("titre" in item):
                            titre = item["titre"]
                            print(f"\t\tTitre : {titre}")
                        
                        if("description" in item):
                            description = item["description"]
                            print(f"\t\tDescription : {description}")
                        
                        if("date" in item):
                            format_date = "%m/%d/%Y %H:%M:%SUTC%z"
                            formatted_date = item["date"].strftime(format_date)
                            print(f"\t\tDate : {formatted_date}")
                        
                        if("categories" in item):
                            categories = item["categories"]
                            print(f"\t\tCategories : {categories}")
                        index += 1
                
        elif args.role == "r3":
            if args.date_debut or args.date_fin or args.source:
                raise ValueError("Cette option n'est pas disponible ici !!!")
            
            corpus_filtre_cat = folder_reader_r3(path)

            if args.category:
                keyword = args.category
                for key in corpus_filtre_cat.keys():
                    if keyword in key:
                        index = 1
                        for item in corpus_filtre_cat.get(key):
                            print(f"\tItem {index}:")

                            if("titre" in item):
                                titre = item["titre"]
                                print(f"\t\tTitre : {titre}")
                            
                            if("description" in item):
                                description = item["description"]
                                print(f"\t\tDescription : {description}")
                            
                            if("date" in item):
                                format_date = "%m/%d/%Y %H:%M:%SUTC%z"
                                formatted_date = item["date"].strftime(format_date)
                                print(f"\t\tDate : {formatted_date}")
                            
                            if("categories" in item):
                                categories = item["categories"]
                                print(f"\t\tCategories : {categories}")
                            index += 1

            else:
                for key in corpus_filtre_cat.keys():
                    print(f"Pour categories {key} :")
                    index = 1
                    for item in corpus_filtre_cat.get(key):
                        print(f"\tItem {index}:")

                        if("titre" in item):
                            titre = item["titre"]
                            print(f"\t\tTitre : {titre}")
                        
                        if("description" in item):
                            description = item["description"]
                            print(f"\t\tDescription : {description}")
                        
                        if("date" in item):
                            format_date = "%m/%d/%Y %H:%M:%SUTC%z"
                            formatted_date = item["date"].strftime(format_date)
                            print(f"\t\tDate : {formatted_date}")
                        
                        if("categories" in item):
                            categories = item["categories"]
                            print(f"\t\tCategories : {categories}")
                        index += 1

        else:
            raise ValueError("Veuillez préciser le rôle ;) ")
    else:
        raise ValueError("Veuillez préciser le mode ;) ")
    

if __name__ == '__main__':
    main()
