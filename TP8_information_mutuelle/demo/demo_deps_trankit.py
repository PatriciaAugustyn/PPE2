'''
@author NGAUV Nicolas

Attention : faite la commande pour installer la librairie tabulate : 
pip install tabulate
Pour plus d'information sur la librairie tabulate : https://pypi.org/project/tabulate/

Utilisation :
python3 demo_deps_trankit.py
'''

from trankit import Pipeline
from tabulate import tabulate


nlp = Pipeline(lang='french')
nlp.add('french-partut')
nlp.add('french-sequoia')
text1 = "Nicolas est un étudiant si charmant, tout le monde le trouve adorable. On ne dirait peut-être pas, mais c'est quelqu'un de très timide... Pourtant, il essaie d'aller vers les autres ! Son problème, c'est qu'il réfléchit trop, tout le temps, et qu'il a tendance à surinterpréter... Il a l'impression qu'il est lourd et qu'il embête tout le monde, alors que ce n'est pas forcément le cas..."
text2 = "Le chat du voisin dort"
doc = nlp(text2)

# Liste des phrases d'un itemn une phrase sera une liste de tokens
contenu = [
    {
        "ID": token.get('id', ''),
        "Token": token.get('text', ''),
        "Lemme": token.get('lemma', ''),
        "POS": token.get('upos', ''),
        "Gouverneur": token.get('head', ''),
        "Dépendance": token.get('deprel', '')
    } for sentence in doc['sentences'] for token in sentence['tokens']
]

# Utilisation de headers="key" pour les clés du dictionnaire
print(tabulate(contenu, headers="keys", colalign=("center",), tablefmt="simple_grid"))



