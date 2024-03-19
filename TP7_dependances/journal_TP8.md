# Journal de Bord - TP8 Groupe 2

### Groupe :

- AUGUSTYN Patricia (Sorbonne Nouvelle) : Lien [GitHub](https://github.com/PatriciaAugustyn)
- Keming (INALCO)
- NGAUV Nicolas (INALCO)

## Séance du 13 mars 2024

## Keming :

**Important :** Les commandes du lancement de script sont tous indiqués au début du script. Et dans le dossier `fichiers test`, il y a des fichiers générés avec les scripts. `main.py` => `test.*` `analyzers.py` => `test_dep.*`

pour `patterns.py`, on peut choisir un ou plusieurs modèles (r1, r2, r3)

------

Je suis chargé du R2 et de faire le merge.

1. pour exo 3, vu qu'on a pris les scripts de correction, donc j'ai oublié de ajouter `depparse‘`, ce qui explique la raison que la dépendance avait été toujours une liste vide.
2. et pour faciliter le merge, j'ai suivi le modèle de Patricia sur le changement de dataclass
3. Pour le merge : étant donné de la différence de datastructure entre Nicolas et nous deux, j'ai dû modifier la fonction d'`analyze_trankit`.  Pour générer les fichiers avec dépendance, je n'ai pas mis `--save-serialized` au début, donc le fichier `pickle` était toujours sous format `json`, avant de merger, je n'y ai pas fait attention car je travaillais sur `json`. 
4. quant à la relecture, j'ai relu la branche de Patricia, tout va bien pour l'exo 1,2,3.
5. Pour exo 4,  Nicolas et moi avons tous fini les 3 patrons, j'ai pris le mien pour éviter faire le merge et modifier.
6. J'aimerais bien savoir comment eviter de télécharger le `cache` du trankit chaque fois, car il n'y a pas de wifi chez moi.

## Nicolas :

#### Changement de code :
Cf. partie de Patricia

Le code dont nous avons hérité ne faisait pas ce qui était nécessaire pour partir sur de bonnes bases cette semaine. Il y avait des erreurs, des oublis et tout simplement des fonctions qui ne nous donnaient pas les bons résultats, dans la forme (format et structure des objets et des données) comme dans le fond (pas les bonnes données)...
Nous avons donc décidé, après avoir passé 2 jours à essayer de corriger le code et d'avancer à partir de celui-ci, qu'il serait plus judicieux, que ce soit au niveau du temps et de la propreté de notre travail, de partir de la correction des professeurs.

#### Information :
Nous avons décidé de nous répartir les tâches comme ceci :
- Patricia s'occupe du rôle r1 et travaillera sur la branche `pa-s8-r1`
- Keming aura le rôle r2 et travaillera sur la branche `ky-s8-r2`
- Quant à moi, je serai responsable du rôle r3 et travaillera sur la branche `nn-s8-r3`

**Exercice 1 et 2** : 
Le fichier `demo_deps_trankit.py` utilise la bibliothèque ***trankit*** et affiche l'ID du token, le texte du token, son lemme, sa partie du discours, l'index du gouverneur et sa dépendance syntaxique. Pour cela, les informations sont stockées dans un tableau avec la librairie ***tabulate***. Ici on analyse des bouts de textes écrits en dur (mais en modifiant les arguments dans le script, on peut bien évidemment changer les textes avec lesquels on veut faire des tests : ici, il y a 2 textes au choix).

```py
'''
Installer la librairie tabulate :
pip install tabulate
Pour plus d'information sur la librairie tabulate : https://pypi.org/project/tabulate/

Utilisation :
- python3 demo_deps_trankit.py pour l'affichage dans le terminal
- python3 demo_deps_trankit.py > res.txt pour rediriger la sortie dans un fichier résultat
'''
```

**Exercice 3** : 
Dans `datastructure.py`, j'ai ajouté de nouveaux attributs pour les objets `Token`, on a donc maintenant :
```py
@dataclass
class Token:
    ID : str
    shape : str
    lemma : str
    pos : str
    head : str
    deprel : str
    head_shape : str
    head_lemma : str
    head_pos : str
```
Un token a donc pour attributs :
- son id
- sa forme
- son lemme
- sa partie du discours
- l'identifiant de son gouverneur
- sa relation de dépendance
- la forme de son gouverneur
- le lemme de son gouverneur
- la partie du discours de son gouverneur

Mise à jour de la fonction `analyze_trankit(parser, article: Item)` pour prendre en compte les nouveaux attributs considérés pour chaque token.
```py
def analyze_trankit(parser, article: Item) -> Item:
    result = parser( (article.title or "" ) + "\n" + (article.description or ""))
    output = []
    for sentence in result['sentences']:
        for token in sentence['tokens']:
            head_shape = ""  # Initialisation avec une valeur par défaut
            head_lemma = ""
            head_pos = ""
            if 'expanded' not in token.keys():
                token['expanded'] = [token]
            head_index = token.get('head', -1)  # Index du head
            if head_index > 0:  # Vérifie si le token a un head
                head_token = next(t for t in sentence['tokens'] if t['id'] == head_index)
                if head_token :
                    head_lemma = head_token['lemma']  # Lemme du head
                    head_shape = head_token['text']  # Forme du head
                    head_pos = head_token['upos']
            for w in token['expanded']:
                output.append(Token(w['id'], w['text'], w['lemma'], w['upos'], w['head'], w['deprel'], head_shape, head_lemma, head_pos))
    article.analysis = output
    return article
```

Voici les commandes :
```
python3 analyzers.py output_file.json -l json -a trankit -s json -o res_trankit.json
python3 analyzers.py output_file.xml -l xml -a trankit -s xml -o res_trankit.xml
python3 analyzers.py output_file.pickle -l pickle -a trankit -s pickle -o res_trankit.pickle
```

**Exercice 4** :
Pour l'exercice 4, voici les 3 fonctions d'extraction de patterns :
```py
def extract_dependancy_pattern_r3(article: Item) -> List[str]:
    """
    Extrait le patron pour recueillir les compléments du nom présents dans l'article donné.
    """
    patterns = []
    for token in article.analysis:
        if ( (token.pos == "NOUN") and  (token.deprel == "nmod") and (token.head_pos == "NOUN") ):
            patterns.append(f"{token.lemma} --{token.deprel}-> {token.head_lemma}")
    return patterns

def extract_dependancy_pattern_r2(article: Item) -> List[str]:
    """
    Extrait le patron pour recueillir les verbes et les noms qu'ils ont pour sujets, présents dans l'article donné.
    """
    patterns = []
    for token in article.analysis:
        if ( (token.pos == "VERB") and  (token.deprel == "nsubj") and (token.head_pos == "NOUN") ):
            patterns.append(f"{token.lemma} --{token.deprel}-> {token.head_lemma}")
    return patterns

def extract_dependancy_pattern_r1(article: Item) -> List[str]:
    """
    Extrait le patron pour recueillir les verbes et les noms qu'ils ont pour objets, présents dans l'article donné.
    """
    patterns = []
    for token in article.analysis:
        if ( (token.pos == "VERB") and  (token.deprel == "obj") and (token.head_pos == "NOUN") ):
            patterns.append(f"{token.lemma} --{token.deprel}-> {token.head_lemma}")
    return patterns
```

Ces fonctions d'extraction des patterns, pouvant bien évidemment être utilisées indépendemment du type de format de fichier désérialisé (`XML`, `JSON` ou `pickle`) et du module utilisé (`Spacy`, `Stranza` ou `Trankit`).

Voici des exemples de commandes avec `trankit` utilisant différents formats de fichiers sérialisés en entrée et avec des motifs de patrons à extraire différents :
```
python3 patterns.py res_trankit.json -l json -o patrons_r3_json.csv -p nmod
python3 patterns.py res_trankit.xml -l xml -o patrons_r3_xml.csv -p nmod
python3 patterns.py res_trankit.pickle -l pickle -o patrons_r3_pickle.csv -p nmod

python3 patterns.py res_trankit.json -l json -o patrons_r3_json.csv -p obj
python3 patterns.py res_trankit.xml -l xml -o patrons_r3_xml.csv -p obj
python3 patterns.py res_trankit.pickle -l pickle -o patrons_r3_pickle.csv -p obj

python3 patterns.py res_trankit.json -l json -o patrons_r3_json.csv -p nmod
python3 patterns.py res_trankit.xml -l xml -o patrons_r3_xml.csv -p nmod
python3 patterns.py res_trankit.pickle -l pickle -o patrons_r3_pickle.csv -p nmod
```

**Exercice 5 et 6** :
J'ai relu la branche de Keming : `ky-s8-r2`.
Tout est ok !!
Difficultés :
- Prise en main du code du groupe précedent qui ne fonctionnait pas
- Travail de la semainde EXTRÊMEMENT chronophage
Solutions :
- S'aider de la correction des professeurs
- Pas le choix, un travail chronophage reste un travail à faire... Alors je le fais~
Merge :
- C'est Keming qui s'occupera du merge : j'ai travaillé non stop PPE depuis jeudi, je dois aussi travailler les autres matières. Mais bien évidemment, on reste à disposition pour aider Keming au besoin ! 



### Patricia :

#### Changement de code :

Pendant le cours, nous nous sommes familiarisés avec le code des groupes précédents et nous avons tenté de comprendre son fonctionnement. A première vue, le code semblait plutôt propre, mais en le lançant nous avons rencontré des erreurs :
- le code utilisait seulement trankit et installait spacy et stanza en même temps
- dans les tokens il n'y avait aucune analyse avec les POS, lemmes et formes
- il y avait beaucoup de listes vides
- le fichier main.py fonctionnait uniquement avec la commande indiquée, mais pas avec d'autres options

Nous nous sommes laissés jusqu'au jeudi soir pour corriger le code, mais nous avons rapidement remarqué que cela demandait trop d'effort pour corriger l'ensemble. Sinon, cela nous prendrait beaucoup trop de temps, et le TP est déjà assez long. Mais aussi, cela nous demandait de corriger à partir des fichiers rss_readear.py et rss_parcours.py, ce qui remonte à quelques semaines auparavant. Ainsi, unanimement nous avons décidé de prendre pour la première fois la correction des professeurs car on allait pouvoir commencer sur de bonne base.


#### Information :
Avec les garçons, nous avons décidé de nous répartir les tâches comme ceci :
- Keming aura la fonction r2 et travaillera sur la branche `ky-s8-r2`
- Nicolas aura la fonction r3 et travaillera sur la branche `nn-s8-r3`
- Quant à moi, j'aurai la fonction r1 je travaillerai sur la branche `pa-s8-r1`

**Exercice 1 et 2** : Le fichier `demo_deps_spacy.py` utilise la bibliothèque ***spacy*** et affiche l'ID du token, le texte du token, sa partie du discours, l'index du gouverneur et sa dépendance syntaxique. Pour cela, les informations sont stockées dans un tableau avec la librairie ***tabulate***.

```py
'''
Attention : faite la commande pour installer la librairie tabulate :
pip install tabulate
Pour plus d'information sur la librairie tabulate : https://pypi.org/project/tabulate/

Utilisation :
- python3 demo_deps_spacy.py
- python3 demo_deps_spacy.py > result.txt
'''
```

**Exercice 3** : Dans `datastructure.py`, j'ai créé une nouvelle class de test pour reprendre le même principe avec le TP7 sur la class Token et Item :
```py
@dataclass
class TestDependance:
    text : str
    lemma : str
    pos : str
    dependancies : str

@dataclass
class Token:
    shape : str
    lemma : str
    pos : str
    dependencies: list[TestDependance] = field(default_factory=list)
```
Ensuite, dans la fonction `analyze_spacy()`, nous avons seulement intégré les informations demandées avec spacy à l'aide de notre class :
```py
#[...]
            dependencies = [
                TestDependance(dep.text, dep.lemma_, dep.pos_, dep.dep_)
                for dep in token.children
            ]
#[...]
```

Malheureusement, dès le début `analyzers.py` a eu un problème avec les fichiers XML et PKL :

```py
'''
Attention : Pour XML, cela génère un fichier JSON dans resultats.py

Utilisation :
1) R1
Pour intégrer les dépendances syntaxiques fournies par Spacy et mettre à jour la sérialization XML :
- python3 analyzers.py input_file.xml -l xml -a spacy -o resultats.xml
'''
```


**Exercice 4** :
Pour l'exercice 4, j'ai rencontré des difficultés à faire la partie *r1*. Cette fonction consistait à extraire un patron de dépendances verbe --obj-> nom pour recueillir les verbes et les noms qu’ils ont pour objet. Malgré mes efforts, je n'ai pas réussi à comprendre comment extraire ces informations à partir de l'analyse syntaxique fournie dans le corpus. Mon code contient les trois parties demandées, mais je n'arrive pas du tout à le coder :

1) extraire le patron de dépendances verbe --obj-> nom pour recueillir les verbes et les noms qu'ils ont pour objet
2) compter les instances avec Counter
3) écrire les résultats dans un fichier avec tabulate pour le tableau


J'ai essayé d'analyser les tokens et leurs dépendances, mais je n'ai pas réussi à identifier correctement les verbes et les noms qui ont une relation de dépendance directe objet. Pour cela, j'ai ajouté ma partie en commentaire et les commandes que j'ai utilisé.


**Relecture** :
Pour la fin de l'exercice 4, le tag de fin se nomme `pa-s8r1-fin`.

Par la suite, j'ai relu le rôle r3 de Nicolas sur la branche `nn-s8-r3`, et le tag est sous le nom `nn-s8r3-relu`.

Comme j'ai eu des difficultés à faire l'exercice 3 et 4, Nicolas m'a beaucoup aidé. Nous avons pris beaucoup de temps à tenter de faire ces exercices. Pour cela, Nicolas a corrigé ce que j'avais fait pour les 2 parties : en sérialisant les 3 formats et les 3 patrons, vu les dépendances des 3 rôles.
Pour l'exercice 4, on regardé les patterns mais ils ne s'écrivent pas sur spacy donc cela nous paraissait bizarre.

J'ai voulu comprendre comment Nicolas a fait, et j'ai pris du temps à relire ses fonctions pour voir comment cela fonctionnait et marchait.





