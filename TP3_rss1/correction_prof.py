'''Cette correction a été prise rapidement, donc cela doit être considérer comme une aide ! '''

import re

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













