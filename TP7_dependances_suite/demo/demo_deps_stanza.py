import stanza
from tabulate import tabulate

#stanza.download('fr') si nécessaire

# Initialisation du pipeline de traitement en français
nlp = stanza.Pipeline('fr')

chemin_fichier = "./test.txt"
with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
    texte = fichier.read()

# Traitement du texte
doc = nlp(texte)

# Préparation des données pour tabulate
donnees = []

for sent in doc.sentences:
    for word in sent.words:
        donnees.append([word.id, word.text, word.head, word.deprel])

# Utilisation de tabulate pour afficher les résultats
entetes = ['ID', 'Token', 'Gouverneur', 'Dépendance']
print(tabulate(donnees, headers=entetes, tablefmt='grid'))
