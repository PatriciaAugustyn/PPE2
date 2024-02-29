'''Cette correction a été prise rapidement, donc cela doit être considérer comme une aide ! '''

import re
from pathlib import Path

text = Path("sample.xml").read_text()

# récupérer le texte, ? = prendre le match le plus court
# flags = re.DOTALL --> il va matcher les retours à la ligne 
items = re.finditer("<item>.?</item>", text, flags=re.DOTALL ) 
item = next(items) # on a 1 item

item_text = item.group(0)
# On affiche tout item
print(item_text)

# Ajout de l'espace potentiel suivie du texte
category = re.search("<category\\s?.*?>(.*?)</category>", item_text)
# print("\\") --> \

item_dict = {}

# Quand category n'est pas None
if category:
    item_dict["categories"] = []
    item_dict["categories"].append(category.group(1))
else :
    item_dict["categories"] = []


# Si on a plusieurs category 
item_dict["categories"] = []
categories = re.finditer("<category\\s?.*?>(.*?)</category>", item_text)
for category in categories:
    item_dict["categories"].append(category.group(1))
#print(item_dict["categories"])

# SOLUTION ETREE
from xml import etree
import ElementTree as ET

root = ET.parse("sample.xml")

#iterfind = génère les éléments les uns à la suite des autres
iterator = root.iterfind(".//item") # on veut n'importe où à partir de la racine

item = next(iterator)

#list(item)
#item.find("title")
# Si on avait pas d'élément la boucle ne fait rien avec iterfind()
for subitem in item.iterfind("category"):
    print(subitem)

# Récupérer le text = subitem.text
# Si on cherche quelque chose à ça n'existe pas
element = item.find("date")
# Tester si : element is None

output = {}
if not element:
    output["date"] = None
else:
    output["date"] = subitem.text

#dict_keys(["date"])
#output["date"] --> rien mais si output["foobar"] cela plante
    
# Si on veut plusieurs category
output["categorie"] = []
for subitem in item.iterfind("category"):
    output["categories"].append(subitem.text)



# SOLUTION FEEDPARSER : Il faut un environnement virtuel
import feedparser

feed = feedparser.parse("sample.xml")
#feed_keys() 

item = feed.entries[0]
#item.title
#item.description
#item.tags  

categories = []
'''
si on fait item["tags"] ça plante, donc on ajoute
for category in item.tags:
    categories.append(category["term"])
'''
for category in item.get("tags", []):
    categories.append(category["term"])
# tags = contenu textuel des balises category xml

# Notre code était bon et pour la suite de la correction on a pas eu 

categories_globale = [it["term"] for it in feed.feed.get("tags", [])]
item_d = {}
item_d["categories"] = categories_globale.copy()


################ PARTIE 2 ####################
import os
def iterate_os(folder: str | Path) -> list:
    files = []
    for iteù in os.listdir(folder):
        path = folder + "/" + item
        if os.path.isfile(path):
            files.append(path)
    return files

def iterate_pathlib_noglob(folder: str | Path) -> list:
    files = []
    for path in Path(folder).iterdir():
        if path.is_file():
            files.append(path)
    return files

# Les éléments qu'on attend d'avoir dans une liste
def iterate_pathlib(folder: str | Path) -> list:
    return sorted(Path(folder).glob("**/*.xml"))

# Ensemble des clés qui représentent l'ensemble de nos alternatives
name2iterator = {
    "os":   iterate_os,
    "pathlib":  iterate_pathlib_noglob,
    "pathlibglob": iterate_pathlib,
}

# LES FILTRES
# pour les arguments optionnels de fonction
from typing import Optional
def filtre_categories(item: dict, categories_valides: Optional[set] = None ) -> bool:
    
    # category ne vaut pas none donc on renvoie vrai car on a pas de filtre
    if not categories_valides:
        return True
    cats = item.get("categories", set())

    # on regarde l'intersection de nos 2 ensembles
    # si elle est pas vide elle sera différente de zéro
    return len(cats.intersection(categories_valides)) != 0

# Utiliser datetime pour parser les dates dans le RSS   
def filtre_start_date(item: dict, start_date: Optional[date]):
    if start_date is None:
        return True
    pubdate = item.get("date")

    if pubdate is None:
        # return False possible
        return True 
    # On regarde si la date de début est inférieur à la date de publication
    return start_date <= pubdate

def filtrer(item: dict, categories_valides: Optional[set] = None, start_date: Optional[date]):
    if not filtre_categories(item, categories_valides):
        return False
    if not filtre_start_date(item, start_date):
        return False
    return True


# Transformer plusieurs fonctions qui a un seul argument !
def filtre_title_contains(substring: str):
    # Cet fonction fonctionne sur l'item
    # On définit une sous fonction qui a la fonction final et ne prend qu'un seul paramètre
    def check_filtre(item: dict):
        return substring in mon_item["title"]
    # Notre fonction prend  notre item et applique notre sous-chaine sur l'item
    return check_filtre

# on déclare une variable qui est une fonction
contain_a = filtre_title_contains("a")

#contain_a({"title": Oui"}) -> False et si change par "Ouais" -> True

#filtres = liste de fonction
def filtre2(item: dict, filtres: list):
    for filtre in filtres:
        if not filtre(item):
            return False
    return True


# MAIN() [stay tuned...]












