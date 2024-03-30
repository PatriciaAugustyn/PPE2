'''
@author AUGUSTYN Patricia

Attention : faite la commande pour installer la librairie tabulate : 
pip install tabulate
Pour plus d'information sur la librairie tabulate : https://pypi.org/project/tabulate/

Utilisation :
python3 demo_deps_spacy.py
'''

import spacy
from tabulate import tabulate


nlp = spacy.load("fr_core_news_sm")
text = "Reclus dans un établissement pénitentiaire au cœur du désert du Nevada, les frères Dalton considérés comme les brigands les plus dangereux de l'ouest, aspirent à retrouver leur liberté, mais en vain. Chaque stratagème élaboré par Joe, l’aîné des Dalton, se solde invariablement par un échec. Qu’ils tentent de se servir de Rantanplan, le canin du Directeur Général, ou de profiter de l’une des erreurs de l'entourage du directeur, leur dessein d’évasion se trouve irrémédiablement compromis. Après s’être enfuis, ils s’emploient à dévaliser les bourgades, mais regagnent toujours leur geôle."
doc = nlp(text)

# Liste des phrases d'un item d'une phrase et qui sera une liste de tokens
# Problème au niveau du gouverneur
contenu = [{"ID": token.i + 1, "Tokens": token.text, "POS": token.pos_, "Gouverneur": token.head.i, "DEP": token.dep_} for token in doc]

# Utilisation de headers="key" pour les clés du dictionnaire
print(tabulate(contenu, headers="keys", colalign=("center",), tablefmt="simple_grid"))



'''
# 2ème fonction pour afficher sur un lien les dépendances comme sur Arborator : 

import spacy
from spacy import displacy

nlp = spacy.load("fr_core_news_sm")
doc = nlp("Reclus dans un établissement pénitentiaire au cœur du désert du Nevada, les frères Dalton considérés comme les brigands les plus dangereux de l'ouest, aspirent à retrouver leur liberté, mais en vain. Chaque stratagème élaboré par Joe, l’aîné des Dalton, se solde invariablement par un échec. Qu’ils tentent de se servir de Rantanplan, le canin du Directeur Général, ou de profiter de l’une des erreurs de l'entourage du directeur, leur dessein d’évasion se trouve irrémédiablement compromis. Après s’être enfuis, ils s’emploient à dévaliser les bourgades, mais regagnent toujours leur geôle.")
displacy.serve(doc, style="dep")

'''





