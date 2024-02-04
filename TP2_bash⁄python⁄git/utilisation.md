# Guide d'utilisation du programme extraire_lexique.py 

Bienvenue dans ce guide d'utilisation :)
Pour garantir une expérience optimale, suivez ces étapes pour configurer l'environnement virtuel et installer les librairies nécéssaire ! 

## Étape 1 : Recommandation

Pour créer un environnemement virtuel, vous pouvez exécuter ces commandes :

```
python3 -m venv ven
```
Puis, activez l'environnement virtuel : 

```
source venv/bin/activate
```

## Étape 2 : Installation de Pretty Table

Une fois l'environnement virtuel activé, vous pouvez utilisé la commande suivante pour installer Pretty Table : 
```
pip install prettytable
```

Pretty Table est une librairie Python qui permet d'afficher des données sous forme de tableau. Pour notre cas, on veut afficher le lexique du corpus sur trois colonnes : 
- le mot
- le nombre d’occurrences total
- le nombre de documents où il apparaît

## Étape 3 : Lancement de la fonction dans le terminal

Maintenant vous pouvez lancer la fonction dans le terminal en utilisant : 
```
python3 extraire_lexique.py
```








