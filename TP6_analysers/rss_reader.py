import argparse
import re
import xml.etree.ElementTree as ET
import feedparser
from pathlib import Path
from datetime import datetime
from typing import Optional, List
import os
# from datastructures import Corpus, Item

def clean_cdata(data: str) -> str:
    if data is None:
        return ''
    return re.sub(r'^<!\[CDATA\[(.*?)\]\]>$', r'\1', data, flags=re.DOTALL)



def clean_html(data:str)-> str:
    data = re.sub(r'<!--.*?-->', '', data, flags=re.DOTALL)
    data = re.sub('<.+?>', '', data, flags=re.DOTALL)
    data = re.sub(r'\xa0', ' ', data, flags=re.DOTALL)
    return data

def read_rss_re(filename: str | Path)-> list[dict]:
    from datastructures import Item
    #CHANGEMENT POUR UTILISATION DE LA CLASSE
    filepath = Path(filename)
    filename_only = filepath.name

    content = filepath.read_text()

    channel_category_match = re.search(r"<category>(.*?)</category>", content, re.DOTALL)
    channel_category = clean_cdata(channel_category_match.group(1)) if channel_category_match else ""

    items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)
    
    output = []
   
    for item in items:
        #enlever le dictionnaire pour utiliser la class Item
        #data = {}
        title_tr = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
        description_tr = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
        pubDate_tr = re.search(r'<pubDate>(.*?)</pubDate>', item, re.DOTALL)
       
        title = clean_cdata(title_tr.group(1)) if title_tr else ''
        description = clean_html(clean_cdata(description_tr.group(1))) if description_tr is not None else ''
        pubDate = clean_cdata(pubDate_tr.group(1)) if pubDate_tr else ''
        
        
        category_tr = re.findall(r'<category>(.*?)</category>', item, re.DOTALL)
        
        categories = [clean_cdata(category) for category in category_tr]

        if channel_category:
            categories.append(channel_category)
        
        categories = list(set(categories))

        #Utiliser Item
        items_rss = Item(title=title, description=description, pubDate=pubDate, category=categories, source=filename_only)
    
        
        output.append(items_rss.as_dict())

    
    return output


def read_rss_etree(filename: str|Path)-> list[dict]:
    from datastructures import Item
    data = []
    try:
        root = ET.parse(filename)
        filename_only = filename.name

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


            categories = [channel_category_text] + [clean_html(clean_cdata(item.text)) for item in item.findall("category")]
            categories = list(set(categories))
            
            #ici on ne peut pas utiliser title=title comme dans re car title est un element de item_data
            items = Item(title=item_data['title'], description=item_data['description'], pubDate=item_data['pubDate'], category=categories, source=filename_only)
            data.append(items.as_dict())
    
        
        return data
        
    except ET.ParseError as e:
        print(f"Oups, etree ne peut pas lire cet item : {e}")
        return['']

    
def read_rss_feedparser(filename: str|Path)-> list[dict[str, str]]:
    from datastructures import Item
    fluxRSS = feedparser.parse(filename)
    filename_only = filename.name

    items = []
    # print(fluxRSS)
    global_category = ""
    for cats in fluxRSS.feed.get("tags", []):
        global_category = cats.get("term", "")
        # print(global_category)

    for item in fluxRSS.entries:
        titre = clean_html(clean_cdata(item.title.strip())) if hasattr(item, 'title') else ''
        description = clean_html(clean_cdata(item.description.strip())) if hasattr(item, 'description') else ''
        datePub = item.get('published', item.get('pubDate', ''))   
        categories = [clean_html(clean_cdata(category.term)) for category in item.get("tags", [])]

        if global_category and global_category not in categories:
            categories.append(clean_html(clean_cdata(global_category)))


        items_rss = Item(title=titre, description=description, pubDate=datePub, category=categories, source=filename_only)
        items.append(items_rss.as_dict())
           
    return items



def parseur(): 
    parser = argparse.ArgumentParser(
        description="Retourne le texte et les métadonnées des <item/> du flux RSS file (fichier unique)"
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
    
    args = parser.parse_args()

    return args


def main():
    from datastructures import Corpus
    args = parseur()
    
    corpus = Corpus(args.xml_corpus)
    
    if os.path.isfile(args.xml_corpus):
        fichiers_uniques = [Path(args.xml_corpus)]
    else:
        print("Ce script permet uniquement de lire un seul fichier. Veuillez spécifier un fichier xml")
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


        for item in dico:
            print(item)
            
if __name__ == '__main__':
    main()

