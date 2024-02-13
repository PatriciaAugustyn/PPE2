# Guide d'utilisation du programme extraire_lexique_bash.py

Ce programme vous offre trois optiosn différentes pour traiter le corpus, en fonction du choix de l'utilisateur.

**Attention** : La syntaxe attendu ressemble à :
- python3 extraire_lexique_bash.py <option> [corpus]

## Les options

### --choix1

Cette option, permet de lire un corpus comme une liste de fichiers en arguments :

```
python3 extraire_lexique_bash.py --choix1 ./Corpus/*.txt
```

### --choix2

Cette option permet de lire un corpus depuis l’entrée standard, en donnant le contenu d’un document sur chaque ligne :

```
cat Corpus/*.txt | python3 extraire_lexique_bash.py --choix2
```

### --choix2

Cette option permet de lister les chemins vers les fichiers du corpus sur l’entrée standard du programme en python :

```
ls Corpus/*.txt | python3 extraire_lexique_bash.py --choix3
```

