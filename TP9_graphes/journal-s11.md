# Journal de Bord - TP9 Groupe 6

### Groupe :

- AUGUSTYN Patricia (Sorbonne Nouvelle) : Lien [GitHub](https://github.com/PatriciaAugustyn)
- BRISSET Lise (Sorbonne Nouvelle)
- BELHOUT Lydia (Nanterre)

--------------------------

## Séance du 03 avril 2024

### Lise

Mon rôle était le 1. Il constituait à mettre en place l'interface du script, les arguments et options et le filtrage des données d'entrées pour la constitution des graphes.

Nous avons discuté et constaté qu'il nous fallait quatres arguments lors du lancement du programme.
Nous avons choisi de manipuler facilement les données avec une liste de dictionnaires plutôt qu'avec des dataclasses car nous avions un peu de mal à visualiser au départ les informations qui allaient être nécessaires et manipulées lors de la création des graphes.

Voici les arguments, et les fonctions liées à ces derniers :

- __-c ou --corpus__  : permet d'indiquer le corpus d'entrée en format tsv.
La fonction rattachée à cet argument est la suivante :

```py
def tsv_to_list(fichier) -> list:
    """
    Fonction qui prend en entrée le fichier tsv et retourne toutes ses informations sous forme d'une liste de dictionnaires,
    chaque dictionnaire contient les informations d'une ligne du tsv.
    """
    liste_items = []

    with open(fichier) as f:
        fichier_tsv = csv.reader(f, delimiter="\t")

        for ligne in fichier_tsv:
            ligne_en_dico = {}
            ligne_en_dico["categorie_gov"] = ligne[0]
            ligne_en_dico["lemme_gov"] = ligne[1]
            ligne_en_dico["relation"] = ligne[2]
            ligne_en_dico["categorie_dep"] = ligne[3]
            ligne_en_dico["lemme_dep"] = ligne[4]
            ligne_en_dico["compte"] = ligne[5]
            ligne_en_dico["IM"] = ligne[6]
            liste_items.append(ligne_en_dico)

    liste_items.pop(0)  # on retire la première ligne d'entête
    return liste_items
```

Cette fonction permet de récupérer les données du fichier tsv d'entrée et de les mettre dans une liste de dictionnaires. Chaque dictionnaire contient les éléments présents dans chaque ligne.

- __-n ou --noeud__ : permet d'indiquer quel est le noeud principal du graphe. Il est necessaire de l'indiquer de la manière suivante "POS-lemme-relation".

```py
def filtre_noeud_voisin(corpus, noeud) -> list:
    """
    Fonction qui filtre les données du corpus en fonction du noeud principal.
    """

    # exemple : NOUN-avion-nmod
    noeud = noeud.split("-")  # liste de trois éléments
    categorie = noeud[0]
    lemme = noeud[1]
    relation = noeud[2]
    liste_items_voisins = []

    # Nous prenons les voisins, c'est à dire tous les items qui ont le même le même gouverneur (ex: NOUN-avion) et la même relation de dépendance (ex : "nmod").
    for item in corpus:
        if item["categorie_gov"] == categorie and item["lemme_gov"] == lemme and item["relation"] == relation:
            liste_items_voisins.append(item)

    return liste_items_voisins
```

Cette fonction filtre la liste de dictionnaires et ne garde que le noeud et ses voisins. Les voisins sont concidéré ici comme les items qui ont le même lemme gouverneur et la même relation de dépendance avec son dépendant. Seul les dépendand change.

- __-s ou --seuil__ : permet d'indiquer un seuil minimal d'information mutuelle.

```py
def filtre_seuil(corpus, seuil) -> list:
    """
    Fonction qui prend en entrée le corpus et applique un filtre sur les seuil des IMs.
    """

    liste_items_seuil = []

    for item in corpus:
        if float(item["IM"]) >= seuil:
            liste_items_seuil.append(item)

    return liste_items_seuil
```

Cette fonction retourne la liste de dictionnaires filtré en fonction du seuil demandé, on ne garde que les items qui ont la valeur IM supérieur ou égal au seuil.

- __-ha ou --hapax__ : permet d'indiquer si on souhaite des hapax (avec "oui") ou si on ne les veut pas (avec 'non').

Cette fonction a été la plus compliquée à mettre en place car les information sur la fréquence de chaque lemme n'était pas présente dans le fichier d'entrée. Il m'a fallu donc calculer la fréquence de chaque lemme. Ils ont été calculer les gouverneurs et dépendants séparement.

```py
# On récupère tous les lemmes du corpus, en séparant le compte des lemmes gouverneurs et dépendants.
    liste_lemme_gov = []
    liste_lemme_dep = []
    for item in corpus:
        liste_lemme_gov.append(item["lemme_gov"])
        liste_lemme_dep.append(item["lemme_dep"])

    # On calcule la fréquence de chaque lemme pour les gov et dep.
    liste_frequence_gov = []
    liste_frequence_dep = []
    for lemme in liste_lemme_gov:
        dico_lemme = {}
        dico_lemme['lemme'] = lemme
        dico_lemme["frequence"] = liste_lemme_gov.count(lemme)
        liste_frequence_gov.append(dico_lemme)
    for lemme in liste_lemme_dep:
        dico_lemme = {}
        dico_lemme['lemme'] = lemme
        dico_lemme["frequence"] = liste_lemme_dep.count(lemme)
        liste_frequence_dep.append(dico_lemme)
```

Il a fallu ensuite dans une boucle vérifier si pour chaque item le gouverneur ET son dépendant sont présents plus d'une fois dans les données.

```py
# On applique le filtre.
    liste_items_hapax = []
    for item in corpus:
        if hapax == "non":
            for dico_lemme_gov in liste_frequence_gov:
                if dico_lemme_gov["lemme"] == item["lemme_gov"] and dico_lemme_gov["frequence"] > 1:
                    for dico_lemme_dep in liste_frequence_dep:
                        if dico_lemme_dep["lemme"] == item["lemme_dep"] and dico_lemme_dep["frequence"] > 1:
                            liste_items_hapax.append(item)
            return liste_items_hapax

        elif hapax == "oui":
            return corpus  # dans ce cas on n'applique pas le filtre
            # Cette option ne marche pas !!! Elle renvoie une liste vide.
```

Dans le cas où on souhaite garder les hapax alors on retourne le corpus sans filtre. Cependant cette option ne marche pas comme attendue et renvoie une liste vide.

- __-lu ou --lien-unique__ : permet d'indiquer si on souhaite avoir les items qui sont présent une fois (avec 'oui') ou plus d'une fois (avec 'non').

```py
def filtre_lien_unique(corpus, lu) -> list:
    """
    Fonction qui filtre les données du corpus sur les liens uniques.
    """

    liste_items_lu = []

    for item in corpus:
        if int(item["compte"]) > 1:
            liste_items_lu.append(item)

    return liste_items_lu
```

Voici un exemple de comment lancer le programme depuis le terminal :

`python3 visualisation.py -c exemple-information_mutuelle.tsv -n VERB-prendre-obj -s 5 -lu oui -ha oui`

Ici on souhaite prendre les relation de type VERB-prendre-obj, qui ont un IM supérieur ou égal à  avec liens uniques et hapax.



--------------------------

### Lydia
j'ai eu le role R3 qui consiste à explorer la bibliothèque python networkx 2 pour trouver des alternatives aux solutions de R1 et R2.
j'ai eu du mal à comprendre la logique d'implémentation des noeuds et des arrêtes puisque j'obtenais soit un graphe vide ou au contraire un graphe géant.
Mais je suis parvenu à un résultat satisfaisant à la fin.
voici la commande pour tester le script:
python3 visudernier.py -c /home/lydia/Desktop/finalppe2/exemple-information_mutuelle.tsv -s 0.5 -o mon_graphe2.gexf -n VERB-prendre-obj
##la relcture
je suis chargée de faire la relecture de R1 fait par Lise, j'ai trouver sa logique d'implémentation cohérente est trés simple à comprendre d'ailleurs je l'ai reprise moi même dans l'implémentation de R3.

--------------------------

### Patricia

#### Information :
Avec les filles, nous avons décidé de nous répartir les tâches comme ceci :

- Lise travaillera sur la branche `lb-s11r1` et aura le rôle `r1`
- Lydia travaillera sur la branche `BLy-S11-R3` et aura le rôle `r3`
- Quant à moi, je travaillerai sur la branche `pa-s11r2` et j'aurais le rôle `r2`

L'objectif de mon rôle est de produire une sortie XML à partir des données filtrées par Lise.
Pour cela, avec ma camarade Lise, nous avons eu un excellente communication pour discuter de notre approche et du rendu final. De plus, Lise maîtrise mieux les arguments et les filtres à appliquer, donc nous avons décidé qu'elle travaillerait sur le rôle `r1` afin que l'on puisse avoir un fondement solide et une bonne arborescence.

Lorsqu'elle a terminé, j'ai pu continuer sur la base de son travail en implémentant la fonction. Cependant, j'ai rencontré des difficultés car j'ai remarqué qu'il y avait un manque de documentation. Par exemple, en cherchant sur internet je trouvais seulement de la documentation pour `NetworkX`.

Après avoir exploré quelques pistes, j'ai décidé d'utiliser la librairie `etree` pour créer la sortie en XML. Par ailleurs, j'ai rapidement réalisé que cette approche devenait extrêmement complexe pour produire une sortie compatible avec le logiciel [Gephi Lite](https://gephi.org/gephi-lite/) .

Après beaucoup de tentative, je me suis souvenu du cours de Mme. Taravella, et j'ai préféré créer un document et écrire dessus avec l'option `write`.
> Tout en récoltant les valeurs récupérées au préalable !

Par exemple, voici le début de la fonction `text_to_graph` du script `visualisation.py` :

```py

# [...]
def text_to_graph(corpus_filtre):
    """
    Fonction qui prend en entrée le corpus filtré sur les arguments donnés en entrée de commande.
    Elle renvoie un fichier de type XML .gexf.
    """

    # Créer la sortie du fichier XML : graph_raw.gexf
    # Attention : vous pouvez changer le titre (ici et au print() à la fin de la fonction)
    with open("graph_raw.gexf", "w") as f:

        # On construit l'arborescence générale du fichier
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<gexf xmlns="http://www.gexf.net/1.2draft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2">\n')
        f.write('  <meta>\n')
        f.write('    <creator>Script Python - Rôle R1 et R2</creator>\n')
        f.write('  </meta>\n')
        f.write('  <graph defaultedgetype="undirected" mode="static" name="">\n')
# [...]
```

**Relecture** :
Pour la fin de l'exercice 1 et 2, le tag de fin se nomme `pa-s11r2-fin`.

Par la suite, j'ai relu le rôle r3 de Lydia sur la branche `BLy-S11-R3`, et le tag est sous le nom `BLy-s11r3-relu`.

Comme nous avons beaucoup discuté entre nous, nous n'avons pas eu besoin de modifier le script de chacune. À la fin, nous avons décidé de renommer le fichier de Lydia afin que sa fonction ne se mélange pas avec la nôtre. Donc, j'ai seulement supprimé le fichier `visualisation.py`, et j'en ai créé un nouveau `visualisation_networkx.py`.


**Fin** :
Je suis très satisfaite de notre groupe car nous discutons énormément de nos choix et nous aidons mutuellement :)

La seule difficulté que nous avons rencontré c'est de trouver les *voisins des voisins* :(


