# extraire_lexique.py

import os
from collections import defaultdict
import string
from prettytable import PrettyTable

#r1

def contenu_corpus():
    '''Cette fonction permet de construire une liste de chaînes (List[str]), 
    où chaque chaîne correspondra au contenu texte d’un fichier 
    du dossier ./Corpus.'''
    
    nch = []
    path_corpus = "./Corpus"

    for doc in os.listdir(path_corpus):
        fichiers = os.path.join(path_corpus, doc)

        if os.path.isfile(fichiers) and doc.endswith(".txt"):
            with open(fichiers, 'r', encoding='utf-8') as file:
                contenu = file.read()
                nch.append(contenu)

    return nch
#print(contenu_corpus())

# r2 

def compter_occurrences(li):
    path_corpus = './Corpus'  
    occurrences = {mot: 0 for mot in li}

    for doc in os.listdir(path_corpus):
        fichiers = os.path.join(path_corpus, doc)
        
        with open(fichiers, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()
            for mot in li:
                occurrences[mot] += contenu.split().count(mot)

    return occurrences


"""Test d'exécution
li = ['voisinage', 'voisin', 'Napisano']  
nb_occurences = compter_occurrences(li)
print(nb_occurences)"""

#r3

def compter_documents_par_mot(corpus):
    '''Cette fonction prend une liste de chaînes
    et retourne un dictionnaire associant chaque mot au nombre de documents dans lequel il apparaît.'''
    
    occurrences_documents = defaultdict(int)
    
    for document in corpus:
        mots_document = set()
        
        document = document.translate(str.maketrans('', '', string.punctuation)).lower()
        
        mots_document = set(document.split())
        
        for mot in mots_document:
            occurrences_documents[mot] += 1
    
    return occurrences_documents

def afficher_tableau():
    corpus = contenu_corpus()
    nb_occurences = compter_documents_par_mot(corpus)
    
    tableau = PrettyTable(["Mot", "Occurrence(s)", "Document(s)"])

    for mot, occurrences_total in nb_occurences.items():
        documents_apparition = nb_occurences[mot]

        tableau.add_row([mot, occurrences_total, documents_apparition])

    print(tableau)

    #with open("tableau.txt", "w") as file:
        #file.write(str(tableau))

print(afficher_tableau())

