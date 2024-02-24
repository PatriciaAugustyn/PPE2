# Journal de Bord - TP5 Groupe 14

### Groupe :

- AUGUSTYN Patricia (Sorbonne Nouvelle)
- SHEN Yuntian \(INALCO\) [Page Gitlab](https://gitlab.com/shenyuntian0)
- COSTANTINE Jeanne (Nanterre)

## Séance du 21 février 2024 (semaine de pause)

### Patricia :

***Exercice 1 :***

```py
# Ajout des commentaires sur la fonction r2

def lecture_fichier_flux_r2(path):
    '''Cette fonction utilise le module etree et permet d'extraire les métadonnées à partir d'un fichier XML'''

    tree = ET.parse(path)
    root = tree.getroot()

    # Déclaration de liste vide pour stocker les données de chaque catégorie
    title = []
    description = []
    date = []
    category = []

    # Trouver/Chercher les balises entre <channel></channel>
    for channel in root.findall('channel'):
        # On va parcourir entre les balises <item></item> dans le "channel"
        for item in channel.findall('item'):
            # On va ajouter les données <pubDate> à la liste "date"
            date.append(item.findtext('pubDate'))

            # On va ajouter les données <title> à la liste "title"
            title.append(item.findtext('title'))

            # On va ajouter les données <category> à la liste "category"
            category.append(item.findtext('category'))

            # On va ajouter les données <description> à la liste "description"
            description.append(item.findtext('description'))

        # A la fin du parcours on affiche la liste category
        print(category)

    # On retourne les listes : channel, title, category, description
    return channel, title, category, description

```

En ayant travaillé sur ce projet la semaine dernière, je trouve que ma camarade a très bien réalisé ce code. J'ai pu voir tout le processus de la création de ce code, c'est pour cela que je le comprends parfaitement.
Par ailleurs, si je devais l'améliorer je pourrais :
- ajouter plus de commentaires parce que il n'y en avait aucun avant que je n'en rajoute. Pour ce cours, je trouve que les commentaires sont importants pour nos camarades afin de comprendre la vision et le code de la personne.
- ajouter une gestion des erreurs, en particulier pour la lecture du fichier XML. Actuellement, si le fichier n'existe pas ou n'est pas au format XML valide, cela pourrait entraîner des erreurs non gérées.

La semaine dernière, avec Jeanne, nous avons travaillé sur le fonction r1. Ainsi, nous avons décidé de nous répartir les tâches comme ceci :
- lecture de la fonction r1 : Jeanne
- lecture de la fonction r2 : Patricia
- lecture de la fonction r3 : Yuntian

### Journal - Commentaire

J'ai travaillé sur le TP qui portait sur l'utilisation du module os en Python, en particulier os.listdir et os.path. La consigne était de créer une fonction, r1, qui propose l'option de filtrer les fichiers en fonction de la date, affichant ainsi les articles parus depuis une date spécifiée jusqu'à une date spécifiée.

Malheureusement, j'ai rencontré des difficultés à comprendre certains concepts. La partie la plus complexe pour moi était d'ajouter une fonctionnalité permettant de filtrer les fichiers en fonction de la date de début et de fin, mais cela n'a pas pu aboutir.J'ai consacré beaucoup de temps à essayer de résoudre ce problème, mais je n'ai pas réussi faire fonctionner mon programme correctement.

Heureusement, vers la fin du TP, Yuntian et Jeanne m'ont aider pour trouver une solution.

### Exercice 4

**Difficultés**

La principale difficulté rencontrée cette semaine était liée à la gestion des fonctions. Nous avons eu du mal à nous assurer que le format de sortie correspondait correctement. Mais aussi, j'ai trouvé qu'il était difficile  de filtrer les fichiers et aboutir à un résultat dans format correct sans modifier les fonctions précédentes. J'ai consacré beaucoup de temps à essayer de résoudre ce problème, mais je n'ai pas réussi à faire fonctionner mon programme correctement sans modifier cela.

La collaboration avec mes camarades a été cruciale pour résoudre ce problème.

**Solutions**

Pour résoudre mon problème Yuntian a apporté des améliorations significatives et en me conseillant de faire mon rôle sous plusieurs fonction et pas en une. Par exemple, on a pu filtrer au niveau des dates et faire une gestion au niveau des erreurs.

```py
def filtre(item: dict) -> bool:
    '''Fonction de filtre pour voir si un élément a une date ou non'''
    if "date" in item :
        return True
    else :
        return False

def filtre_date(rssFile:list):
    '''Cette fonction permet de filtrer les éléments qui ont une date en prenant en entrée une liste d'élément RSS'''

    # On initialise le dictionnaire qui nous servira en sortie
    filted_by_date = {}

    # On va parcourir tous les éléments dans la liste donnée
    for item in rssFile :

      [....]

        else :
            none_date = "Cette date est absente !"
            if none_date not in filted_by_date :
                filted_by_date[none_date] = []
            filted_by_date[none_date].append(item)
    return filted_by_date

```

**Choix lors des merges**

Pour le choix de merge, nous avons décidé de confier à Yuntian la responsabilité de fusionner avec les trois fonctions, comme cela avait été fait la semaine précédente. Ensuite nous avons ajuster la fonction main afin que notre programme puisse prendre en compte toutes nos fonctions. Par la suite, Yuntian a commit cela et ajouter le tag final "gp14-s4rss2-fin".



### Jeanne :

***Exercice 1 :***

```py
# Ajout des commentaires sur la fonction r1

def lecture_fichier_flux_r1(path):
    '''Cette fonction permet de lire le fichier xml dont le chemin est donné en
    argument, et qui retourne le texte et les métadonnées des item du flux RSS.'''

    # Ouvre le fichier XML en mode lecture avec l'encodage UTF-8
    with open(path, "r", encoding="utf-8") as fichier:
        # Lit tout le contenu du fichier XML
        xml = fichier.read()

        # On veut cibler notre regex sur ce qui est seulement a l'intérieur des balises <title></title>
        regex_titre = re.findall(r"<title>(.*)</title>", xml)
        
        # Utilise des expressions régulières pour extraire le texte entre les balises <description></description>
        regex_description = re.findall(r"<description>(.*)</description>", xml)

        # Les résultats : rendre la visualisation des données plus visible
        print("\nLe texte entre les balises <title></title> :\n")
        for titre in regex_titre:
            print(titre.strip())

        # Affiche les résultats pour les balises <description>
        print("\nLe texte entre les balises <description></description> :\n")
        for description in regex_description:
            print(description.strip())

        # Bonus : Extraction et affichage des données pour d'autres balises telles que <pubDate>, <link>, et <category>
        regex_date = re.findall(r"<pubDate>(.*)</pubDate>", xml)
        regex_lien = re.findall(r"<link>(.*)</link>", xml)
        regex_categorie = re.findall(r"<category>(.*)</category>", xml)

        print("\nLe texte entre les balises <pubDate></pubDate> :\n")
        for date in regex_date:
            print(date.strip())

        print("\nLe texte entre les balises <link></link> :\n")
        for lien in regex_lien:
            print(lien.strip())

        print("\nLe texte entre les balises <category></category> :\n")
        for categorie in regex_categorie:
            print(categorie.strip())
```

J'ai travaillé sur la fonction r1 la semaine dernière, et je trouve que cette version est plus concise et offre une meilleur expérience pour l'utilisateur. De plus le script était déjà beaucoup commenté, ce qui facilite a compréhension et la prise en main. 




### Yuntian :

***Exercice 1 :***

```python
# Ajout des commentaires sur la fonction r3

def lecture_fichier_flux_r3(path):
    try:
        # Analyse le fichier de flux RSS situé à l'emplacement spécifié par 'path'
        feed = feedparser.parse(path)

        # Affiche le contenu entre les balises <title></title>
        print("\nLe texte entre les balises <title></title> :\n")
        for entry in feed.entries:
            print(entry.title.strip())

        # Affiche le contenu entre les balises <description></description>
        print("\nLe texte entre les balises <description></description> :\n")
        for entry in feed.entries:
            print(entry.description.strip())

        # Affiche le contenu entre les balises <pubDate></pubDate>
        print("\nLe texte entre les balises <pubDate></pubDate> :\n")
        for entry in feed.entries:
            print(entry.published.strip())

        # Affiche le contenu entre les balises <link></link>
        print("\nLe texte entre les balises <link></link> :\n")
        for entry in feed.entries:
            print(entry.link.strip())

        # Affiche le contenu entre les balises <category></category>
        print("\nLe texte entre les balises <category></category> :\n")
        for entry in feed.entries:
            if 'tags' in entry:
                for tag in entry.tags:
                    print(tag.term.strip())

    except Exception as e:
        # En cas d'erreur lors de l'exécution du code contenu dans le bloc try,
        # cette section sera exécutée pour gérer l'erreur.
        print(f"Une erreur s'est produite : {e}")

```

Dans mon travail précédent j'étais responsable de la partie de r2, à travers l'étude de ce code j'ai trouvé que la module **feedparser** a un haut degré d'intégration de l'analyse des fichiers RSS, que j'ai précédemment utilisé pour se référer à la module **etree** pour les fichiers xml pour utiliser le code est plus concis.
Et ce code prend en compte la gestion des erreurs, ce qui est un aspect que je n'avais pas envisagé auparavant.

Cependant, cette fonction **n'a pas de valeur** de retour et se contente d'afficher le contenu extrait sur le terminal, ce qui n'est pas pratique pour notre prochain travail, c'est pourquoi j'y ai apporté les modifications suivantes :

```python
def lecture_fichier_flux(path):
    try:
        # Parser le fichier RSS
        feed = feedparser.parse(path)

        # Initialisation de la liste pour stocker les données
        xmlData = []
        
        for entry in feed.entries:
            itemData = {}

            # Récupérer le titre si présent
            if 'title' in entry:
                itemData["titre"] = entry.title.strip()

            # Récupérer la description si présente
            if 'description' in entry:
                itemData["description"] = entry.description.strip()

            # Récupérer la date de publication si présente
            if 'published' in entry:
                try:
                    # Essayer de parser la date selon le premier format
                    format_date = "%a, %d %b %Y %H:%M:%S %z"
                    published_datetime = datetime.strptime(entry.published.strip(), format_date)
                    itemData["date"] = published_datetime
                except ValueError:
                    pass
                try:
                    # Essayer de parser la date selon le deuxième format
                    format_date = "%a, %d %b %Y %H:%M:%S %Z"
                    published_datetime = datetime.strptime(entry.published.strip(), format_date)
                    itemData["date"] = published_datetime
                except ValueError:
                    pass
            # Récupérer les catégories si présentes
            if 'tags' in entry:
                itemData["categories"] = []
                for tag in entry.tags:
                    itemData["categories"].append(tag.term.strip())

            if 'link' in entry:
                link = entry.link
                pattern = r'https?://(?:www\.)?(?:[^./]+\.)?([^./]+)\.'
                try:
                    source = re.match(pattern, link).group(1)
                except Exception as e:
                    link = feed.feed.link
                    pattern = r'https?://(?:www\.)?(?:[^./]+\.)?([^./]+)\.'
                    source = re.match(pattern, link).group(1)
                
                itemData["source"] = source
                
            # Ajouter les données de l'entrée à la liste
            xmlData.append(itemData)
        
        # Retourner les données
        return xmlData

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


```

***Exercice 2 :***

> Alors que dans l'exercice 1 j'étais responsable de r2 (vérifiant le code pour le dernier groupe de r3), dans l'exercice 2 j'ai écrit le code pour r3.

Pour parcourir les fichiers, j'utilise la fonction `glob()` par le module **pathlib** et je remplis l'argument avec un caractère de remplacement pour le nom de fichier.

Parce que la cible est tous les fichiers xml dans ce dossier, le paramètre est donc : `**/*.xml`

Et mon code de parcour est :
```python
    for filePath in path.glob('**/*.xml'):
        #...
```

Il s'agit ensuite de filtre tous les articles par catégorie. Comme la catégorie est stockée dans une list\[str\] et que les listes ne peuvent pas être utilisées comme clés de dictionnaire, elles sont converties en tuples lors de le filtre.

Conseils pour d'autres rôles dans Relu

- r1: Pour faciliter la comparaison des dates, celles-ci sont converties en **datetime** plutôt que d'être stockées sous forme de chaînes de caractères.

- r2: Ces fichiers rss ne semblent pas contenir de balises de source distinctes, et la solution alternative consiste à obtenir des noms de domaine intermédiaires pour les liens vers les sources d'information, qui sont généralement les noms des journaux ou des sites web sources.

### les choix lors des merges

Finalement, nous avons décidé d'utiliser la version de Shen Yuntian(branche s4-r3) pour la fusionner avec la version principale.

