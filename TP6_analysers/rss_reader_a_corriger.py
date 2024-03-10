import argparse
import re
import xml.etree.ElementTree as ET
import feedparser
import pathlib as PL 
from datetime import datetime

"""
Ce script peut être lancé avec ces exemples de commande :
python3 rss_reader.py feedparser ./2024-2/ category 'Société'
python3 rss_reader.py re ./2024-2/ date 10-02-2024 11-02-2024
python3 rss_reader.py etree ./2024-2/ category 'Politique'
"""
  

def read_rss_re(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as file:
        content = file.read()
    items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)

    data = []
   
    for item in items:
        title_tr = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
        description_tr = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
        category_tr = re.search(r'<category>(.*?)</category>', item, re.DOTALL)
        pubDate_tr = re.search(r'<pubDate>(.*?)</pubDate>', item, re.DOTALL)
       
        title = title_tr.group(1) if title_tr else ''
        description = description_tr.group(1) if description_tr else ''
        category = category_tr.group(1) if category_tr else ''
        pubDate = pubDate_tr.group(1) if pubDate_tr else ''
        data.append({'title': title, 'description': description, 'category': category, 'pubDate': pubDate})
    return data


def read_rss_etree(xml_file):
    data = []
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for item in root.findall('.//item'):
            item_data = {}
            for child in item:
                if child.tag == 'title':
                    item_data['title'] = child.text
                elif child.tag == 'description':
                    item_data['description'] = child.text
                elif child.tag == 'category':
                    item_data['category'] = child.text
                elif child.tag == 'pubDate':
                    item_data['pubDate'] = child.text
            data.append(item_data)
        
        return data
    except ET.ParseError:
        print(f"Oups, etree ne peut pas lire cet item")
        return['']
        

def read_rss_feedparser(xml_file):
    fluxRSS = feedparser.parse(xml_file)
    items = []
    for item in fluxRSS.entries:
        titre = item.title.strip() if hasattr(item, 'title') else ''
        description = item.description.strip() if hasattr(item, 'description') else ''
        categorie = item.category.strip() if hasattr(item, 'category') else ''
        datePub = item.get('published', item.get('pubDate', ''))      
        metadata = {
            'title': titre,
            'description': description,
            'category': categorie,
            'pubDate': datePub,
        }       
        items.append(metadata)    
    return items

#modification semaine 5
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
        type=PL.Path, 
        help="Chemin du corpus xml"
        )
    parser.add_argument(
        "option_filtrage",
        choices=['date', 'source', 'category'],
        help="Choisissez un filtre"
    )
    parser.add_argument(
        "contenu_filtre",
        type=str,
        help="Écrivez le contenu que vous cherchez"        
    )
    parser.add_argument(
        "date_debut",
        nargs="*",
        type=lambda d: datetime.strptime(d, "%d-%m-%Y").date(),
        help="Les artciles après cette date inluse (JJ-MM-AAAA)"
        )
    parser.add_argument(
        "date_fin",
        nargs="*", 
        type=lambda d: datetime.strptime(d, "%d-%m-%Y").date(), 
        help="Les artciles avant cette date incluse(JJ-MM-AAAA)"
        )
    args = parser.parse_args()
    return args

#r3 semaine 5
def filtrage_category(liste_dictionnaire):
    args = parseur()
    categorie_existe = False
    for item in liste_dictionnaire :
        if 'category' in item and item['category'] == args.contenu_filtre:
                print(item)
                categorie_existe = True
                return item
    if not categorie_existe: 
        False
   
#r1 semaine 5    
def filtre_date(items_data, date_debut=None, date_fin=None):
    articles_filtres_date = []
    if date_debut is None and date_fin is None:  
        return articles_filtres_date  
    for item in items_data:
        try:
            article_date = datetime.strptime(item['pubDate'], "%a, %d %b %Y %X %z")
            if date_debut and date_fin:
                if date_debut <= article_date.date() <= date_fin:
                    articles_filtres_date.append(item)
            elif date_debut and not date_fin:
                if date_debut <= article_date.date():
                    articles_filtres_date.append(item)
            elif date_fin and not date_debut:
                if article_date.date() <= date_fin:
                    articles_filtres_date.append(item)
        except ValueError:
            pass
    return articles_filtres_date


#r2 semaine 5 (cette partie du code ne marche pas)
def filtre_source(root_directory_path, sources):
    root_directory = PL.Path(root_directory_path)
    all_files = list(root_directory.rglob('*'))
    results = {source: [] for source in sources}
    for file in all_files:
        if file.is_file():
            for source in sources:
                if source in file.name: 
                    results[source].append(str(file))
    results = {source: files for source, files in results.items() if files}
    return results


def main():
  
    args = parseur()
    #on va extraire les documents avec pathlib et glob()
    dossier_parent = PL.Path(args.xml_corpus)
    fichiers_uniques = set() # les sets ne permettent pas les doublons, il est plus rapide que de le faire avec une liste.
    for fichier in dossier_parent.glob('**/*.xml'):
        fichier_str = str(fichier)
        if fichier_str not in fichiers_uniques:
            fichiers_uniques.add(fichier_str) 
   
   
    for chaque_fichier in fichiers_uniques :
        if args.methode == 're':
            dico = read_rss_re(chaque_fichier)
        elif args.methode == 'etree':
            dico = read_rss_etree(chaque_fichier)
        elif args.methode == 'feedparser':
            dico = read_rss_feedparser(chaque_fichier)
        else:
            raise ValueError("Méthode invalide. Veuillez spécifier : re / etree / feedparser")
        
       #on se sert des variables qu'on a créées avant !
        if args.option_filtrage == 'date': #on lance le filtre de date
           if args.date_debut and args.date_fin:
                items_filtrés = filtre_date(dico, args.date_debut[0], args.date_fin[0])
                if items_filtrés:
                    for item in items_filtrés:
                        print(item) 
           elif args.date_debut:
                items_filtrés = filtre_date(dico, args.date_debut[0])
                if items_filtrés:
                    for item in items_filtrés:
                        print(item)
           elif args.date_fin:
                items_filtrés = filtre_date(dico, None, args.date_fin[0])
                if items_filtrés:
                    for item in items_filtrés:
                        print(item)
        if args.option_filtrage == 'source': #cette partie du code ne marche pas
            sources = ['BFM', 'France Info', 'Le Figaro', 'Libération', 'Blast']
            if args.option_filtrage in ['category', 'source']:
                items_filtrés = filtre_source(dico, args.option_filtrage, args.contenu_filtre, sources)
                for item in items_filtrés:
                    print(item)
        if args.option_filtrage == 'category': #on lance le filtre de catégorie
            filtrage_category(dico)
            
            
if __name__ == '__main__':
    main()
