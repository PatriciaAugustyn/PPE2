import argparse
import re
import xml.etree.ElementTree as ET
import feedparser
from pathlib import Path
from datetime import datetime
from typing import Optional

"""
Ce script peut être lancé avec ces exemples de commande :
python3 rss_reader.py feedparser ./2024-2/ category 'Société'
python3 rss_reader.py re ./2024-2/ date 10-02-2024 11-02-2024
python3 rss_reader.py etree ./2024-2/ category 'Politique'
python3 ./projet/correction.py etree ./TP4/ressources/2024/01/26/ven.2024-01-26.00:28 --source 'BFMTV' --category 'Musique' --date_debut 23-01-2024 --date_fin 25-01-2024
"""
  
def clean_cdata(data: str) -> str:
    if data is None:
        return ''
    return re.sub(r'^<!\[CDATA\[(.*?)\]\]>$', r'\1', data, flags=re.DOTALL)



def clean_html(data:str)-> str:
    data = re.sub(r'<!--.*?-->', '', data, flags=re.DOTALL)
    data = re.sub('<.+?>', '', data, flags=re.DOTALL)
    return data

def read_rss_re(filename: str | Path)-> list[dict[str, str]]:
    filepath = Path(filename)
    fname = filepath.stem
    content = filepath.read_text()

    channel_category_match = re.search(r"<category>(.*?)</category>", content, re.DOTALL)
    channel_category = clean_cdata(channel_category_match.group(1)) if channel_category_match else ""

    items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
    
    output = []
   
    for item in items:
        data = {}
        title_tr = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
        description_tr = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
        pubDate_tr = re.search(r'<pubDate>(.*?)</pubDate>', item, re.DOTALL)
       
        data["title"] = clean_cdata(title_tr.group(1)) if title_tr else ''
        data["description"] = clean_html(clean_cdata(description_tr.group(1))) if description_tr is not None else ''
        data["pubDate"] = clean_cdata(pubDate_tr.group(1)) if pubDate_tr else ''
        
        category_tr = re.findall(r'<category>(.*?)</category>', item, re.DOTALL)
        
        data["category"] = [clean_cdata(category) for category in category_tr]

        if channel_category:
            data["category"].append(channel_category)
        
        data["category"] = list(set(data["category"]))
        # print(data['category'])

        output.append(data)

    
    return output


def read_rss_etree(filename: str|Path)-> list[dict[str, str]]:
    data = []
    try:
        root = ET.parse(filename)

        channel_category = root.find('.//channel/category')
        if channel_category is not None:
            channel_category_text = clean_html(clean_cdata(channel_category.text))
        else:
            channel_category_text = ""

        tags = {"title", "description", "pubDate"}
        for item in root.iterfind('.//item'):
            item_data = {}
            for tag in tags:
                if not tag:
                    item_data[tag] = ""
                else:
                    item_data[tag] = clean_html(clean_cdata(item.find(tag).text)) if item.find(tag) is not None else ""


            item_data["category"] = [channel_category_text] + [clean_html(clean_cdata(item.text)) for item in item.findall("category")]

            # print(item_data)
            data.append(item_data)
        
        return data
        
    except ET.ParseError as e:
        print(f"Oups, etree ne peut pas lire cet item : {e}")
        return['']

 
    
def read_rss_feedparser(filename: str|Path)-> list[dict[str, str]]:
    fluxRSS = feedparser.parse(filename)
    items = []
    # print(fluxRSS)
    global_category = ""
    for cats in fluxRSS.feed.get("tags", []):
        global_category = cats.get("term", "")
        # print(global_category)

    for item in fluxRSS.entries:
        titre = item.title.strip() if hasattr(item, 'title') else ''
        description = item.description.strip() if hasattr(item, 'description') else ''
        datePub = item.get('published', item.get('pubDate', ''))   
        categories = [clean_html(clean_cdata(category.term)) for category in item.get("tags", [])]

        if global_category and global_category not in categories:
            categories.append(clean_html(clean_cdata(global_category)))

        metadata = {
            'title': clean_html(clean_cdata(titre)),
            'description': clean_html(clean_cdata(description)),
            'category': categories,
            'pubDate': datePub,
        }       

        items.append(metadata) 
           
    return items


#r3 semaine 5
def filtre_category(item: dict, categorie_existe: Optional[set] = None)-> bool :
    # print(item['category'], categorie_existe)
    if categorie_existe is None:
        print(f"Aucun élément trouvé pour la catégorie '{categorie_existe}'.")
        return True
    for categorie in item['category']:
        if categorie_existe.lower() in categorie.lower():
            # print(item)
            return True
        else:
            return False
   
#r1 semaine 5    
def filtre_date(item: dict, date_debut: Optional[datetime.date] = None, date_fin: Optional[datetime.date] = None) -> bool:
    if date_debut is None and date_fin is None:
        return True  # Si aucune date n'est spécifiée, l'article passe le filtre
    try:
        # print(item['pubDate'])
        article_date = datetime.strptime(item['pubDate'], "%a, %d %b %Y %H:%M:%S %Z").date()
        # print(article_date)
        if date_debut and date_fin:
            return date_debut <= article_date <= date_fin
        elif date_debut:
            return article_date >= date_debut
        elif date_fin:
            return article_date <= date_fin
    except (TypeError, ValueError) as e:
        print(f"Error parsing date: {e}")
    return False


def filtre_source(fichier = Path, source: Optional[str] = None)-> bool:
    if source is None:
        return False
    if source.lower() in fichier.name.lower():
        return True


def iterate_pathlib_glob(folder: str|Path) -> list:
    return sorted(Path(folder).glob("**/*.xml"))

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
        help="Chemin du corpus xml"
        )

    parser.add_argument("--source", choices=["BFMTV", "Libération", "France info", "Le Figaro", "Blast", "Elucid"], help="Filtrer par source", default=None)
    parser.add_argument("--category", help="Filtrer par catégorie", default=None)

    parser.add_argument(
        "--date_debut",
        nargs="?",
        type=lambda d: datetime.strptime(d, "%d-%m-%Y").date(),
        help="Les artciles après cette date inluse (JJ-MM-AAAA)",
        default=None
        )
    parser.add_argument(
        "--date_fin",
        nargs="?", 
        type=lambda d: datetime.strptime(d, "%d-%m-%Y").date(), 
        help="Les artciles avant cette date incluse(JJ-MM-AAAA)",
        default=None
        )
    
    args = parser.parse_args()

    return args

def main():
    args = parseur()
    #on va extraire les documents avec pathlib et glob()
    dossier_parent = Path(args.xml_corpus)
   
    fichiers_uniques = iterate_pathlib_glob(dossier_parent)

    items_filtrés_globaux = []
   
    for chaque_fichier in fichiers_uniques :
        if args.source and not filtre_source(chaque_fichier, args.source):
            continue

        if args.methode == 're':
            dico = read_rss_re(chaque_fichier)
        elif args.methode == 'etree':
            dico = read_rss_etree(chaque_fichier)
        elif args.methode == 'feedparser':
            dico = read_rss_feedparser(chaque_fichier)
        else:
            raise ValueError("Méthode invalide. Veuillez spécifier : re / etree / feedparser")

       #on se sert des variables qu'on a créées avant !
        for item in dico:
            # print(item)
            if args.date_debut and args.date_fin:
                if not filtre_date(item, args.date_debut, args.date_fin):
                    continue
            elif args.date_debut:
                # print(chaque_fichier)
                if not filtre_date(item, args.date_debut):
                    continue
            elif args.date_fin:
                if not filtre_date(item, None, args.date_fin):
                    continue

            if args.category: #on lance le filtre de catégorie
                if not filtre_category(item, args.category):
                    continue
                
            items_filtrés_globaux.append(item)

    for item in items_filtrés_globaux:
        print(item)
            
if __name__ == '__main__':
    main()
