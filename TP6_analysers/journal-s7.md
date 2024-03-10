# Journal de Bord - TP5 Groupe 18

### Groupe :

- AUGUSTYN Patricia (Sorbonne Nouvelle) : Lien [GitHub](https://github.com/PatriciaAugustyn)
- Clara (Nanterre)
- NGAUV Nicolas (INaLCO)

## Séance du 06 mars 2024

### Clara :

## NGAUV Nicolas
- Exercice 1 : Prise en main de trankit (utilisation de Trankit pour l'analyse de texte en utilisant le modèle pré-entrainé pour le français) :
    - Importation de la classe `Pipeline` de Trankit :
        - avec `from trankit import Pipeline`
        - utilisée pour charger et utiliser les modèles de traitement du langage naturel pré-entraînés
    - Chargement du modèle Trankit pour le français :
        - avec `nlp = Pipeline(lang='french', gpu=False)`
            - création d'une instance de la classe `Pipeline` en spécifiant la langue (`lang='french'`) pour utiliser le modèle Trankit entraîné pour le français. L'argument `gpu=False` indique que le GPU n'est pas utilisé pour le traitement, et qu'on utilise le CPU (mais on peut l'utiliser si on veut, selon notre matériel)
    - Analyse du texte avec Trankit:
        - avec `data = nlp(text)`
        - si par exemple, `text = '''Hello! This is Trankit.'''`, alors on a un dictionnaire python avec la structure suivante (on utilise `[...]` pour une meilleure visibilité) :
            ```py
            {
                    'text': 'Hello! This is Trankit.',  # input string
                    'sentences': [ # list of sentences
                        {
                        'id': 1, 'text': 'Hello!', 'dspan': (0, 6), 'tokens': [...]
                        },
                        {
                        'id': 2,  # sentence index
                        'text': 'This is Trankit.',  'dspan': (7, 23), # sentence span
                        'tokens': [ # list of tokens
                            {
                            'id': 1, # token index
                            'text': 'This', 'upos': 'PRON', 'xpos': 'DT',
                            'feats': 'Number=Sing|PronType=Dem',
                            'head': 3, 'deprel': 'nsubj', 'lemma': 'this', 'ner': 'O',
                            'dspan': (7, 11), # document-level span of the token
                            'span': (0, 4) # sentence-level span of the token
                            },
                            {'id': 2...},
                            {'id': 3...},
                            {'id': 4...}
                        ]
                        }
                    ]
                }
            ```
    - Récupération des informations qui nous intéresse pour chaque token :
        - avec
         ```py
         # Parcourir chaque phrase dans 'sentences'
            for sentence in data['sentences']:
                # Parcourir chaque token dans 'tokens'
                for token in sentence['tokens']:
                    # Récupérer les valeurs 'text', 'lemma' et 'upos' pour chaque token
                    token_text = token['text']
                    token_lemma = token['lemma']
                    token_upos = token['upos']
            # Parcours de chaque token dans le dictionnaire retourné par Trankit, et extraction de sa forme, de son lemme et de sa partie du discours.
         ```
- Exercice 2 :
    - pour utiliser `demo_trankit.py` :
        ```
        python3 demo_trankit.py <chemin_du_fichier_à_analyser> <chemin_du_fichier_resultat>
        ```
        - exemple :
        ```
        python3 demo_trankit.py test.txt test_res.txt
        ```
- Exercice 3 :
    - Beaucoup de problèmes par rapport au format de données, surtout concernant les fichiers au format pickle.
    - Petite aide à l'utilisation et au test (les fichiers `corpus_filtered` sont des corpus précédemment sauvegardé qu'on veut charger pour l'analyse : à remplacer par vos propres fichiers de corpus si vous voulez tester les vôtres):
        ```
        python analyzers.py -i corpus_filtered.json -t trankit -o res_trankit.json
        python analyzers.py -i corpus_filtered.xml -t trankit -o res_trankit.xml
        python analyzers.py -i corpus_filtered.pickle -t trankit -o res_trankit.pickle
        ```
    - L'analyse avec trankit n'a pas de problème pour les fichiers au format xml et json : pour le format pickle, c'est plus compliqué...
        - Il faut bien s'assurer que le corpus sauvegardé sous format pickle et utilisé comme fichier entrant pour l'analyse (ici `corpus_filtered.pickle` par exemple) est bien un objet `Corpus` : une petite précision qui a son importance !
            - En effet le problème s'est posé pour moi : le contenu du fichier n'était pas reconnu comme un objet `Corpus` mais comme une liste d'objets... Ce qui a posé problème car une liste d'objets n'a pas d'attributs `items`...
        - J'ai testé avec un fichier contenant réellement un corpus sous format pickle, et là l'analyse ne présente aucun problème, et on a les bons résultats, comme avec les corpus au format xml et json.
    - A noter qu'on peut également changer de format : le format du fichier de sortie n'a pas à être celui du fichier d'entrée !
        - Cela évite les déconvenues nommées précédemment...
        - Exemple : `python3 analyzers.py -i corpus_filtered.json -t trankit -o res_trankit.pickle`

### Patricia :

**Commentaire** :

Pendant le cours, nous avons décidé de se répartir les tâches :
- Clara a décidé de travailler avec la bibliothèque Stanza.
- Nicolas travaillera avec la bibliothèque Trankit.
- Quant à moi, j'ai décidé de me concentrer sur la bibliothèque Spacy.

Ayant déjà utilisé Spacy dans d'autres cours, je me sens plus à l'aise avec cette bibliothèque et maîtrise mieux ses fonctionnalités. De plus, pour l'exercice 1, où l'objectif est d'analyser un texte donné en argument en lemmes, part of speech et tokens, je trouve que Spacy est plus simple d'utilisation.

Pour ceux qui souhaitent utiliser le fichier demo_spacy.py, voici comment le lancer :
```py
python3 demo_spacy.py <chemin_du_fichier_à_analyser>

# Exemple : python3 demo_spacy.py bonheur.txt
```

Attention : il faut remplacer <chemin_du_fichier> par le chemin complet de votre fichier. Cette commande lancera le script et fournira les résultats d'analyse du texte (token, lemme, et parties du discours).

**Exercice 3** :
Pour l'exercice 3, j'ai consacré énormément de temps sur ma partie car j'ai dû débugger des erreurs liées au format de sortie. Après quelques jours d'efforts, j'ai réussi à enrichir le fichier avec le résultat de l'analyse en utilisant XML et JSON, mais pas PKL.

```py
'''
Attention : dans demo_spacy n'oubliez pas de changer resultat_spacy.json en .pkl ou .xml ;)

Utilisation :

1) JSON :
- il faut faire la commande pour obtenir un fichier : python3 demo_spacy.py corpus.json
Ensuite, vous obtiendrez un document resultat_spacy.json avec l'annotion en pos, token et lemme

- python analyzers.py -f corpus.json -t spacy -o resultat_spacy.json
Sur le même document resultat_spacy.json vous aurez le document enrichi avec le résultat de l'analyse

2) XML
- il faut faire la commande pour obtenir un fichier : python3 demo_spacy.py corpus.xml
Ensuite, vous obtiendrez un document resultat_spacy.xml avec l'annotion en pos, token et lemme

- python analyzers.py -f corpus.xml -t xml -o resultat_spacy.xml
Sur le même document resultat_spacy.xml vous aurez le document enrichi avec le résultat de l'analyse

3) Malheureusement, le format PKL ne fonctionne pas :(
- il faut faire la commande pour obtenir un fichier : python3 demo_spacy.py corpus.pkl
Ensuite, vous obtiendrez un document resultat_spacy.pkl avec l'annotion en pos, token et lemme

- python analyzers.py -f corpus.pkl -t pickle -o resultat_spacy.pkl
Sur le même document resultat_spacy.pkl vous aurez le document enrichi avec le résultat de l'analyse
'''
```
Pour conclure, ce TP a été particulièrement difficile en raison de ces problèmes. J'ai passé beaucoup de temps à comprendre les erreurs, à chercher des solutions en ligne, mais malheureusement, je n'ai pas pu réussir avec le format PKL. C'était extrêmement frustrant de ne pas savoir d'où venait le problème et de rester bloqué à la première étape. Mais en persévérant, j'ai réussi à rendre le script fonctionnel.


**Exercice 4** : Cette semaine, j'ai relu le code de mon camarade Nicolas. Pour le choix du tag, je l'ai écrit sous ce nom :  `nn-s7-relu`.

Pour lancer le programme de Nicolas, nous pouvons utiliser les commandes suivantes :

- Pour le format JSON :
```
python analyzers.py -i corpus_filtered.json -t trankit -o res_trankit.json
```
- Pour le format XML :
```
python analyzers.py -i corpus_filtered.xml -t trankit -o res_trankit.xml
```

**Exercice 5** :


***Difficultés*** : Cette semaine, nous avons réussi à rendre le code fonctionnel pour les formats JSON et XML, mais pas pour le formar pickle. Nous avons essayé de résoudre le problème, mais cela nous renvoie toujours la même erreur.
Pour ma part, j'ai passé trois jours à résoudre les problèmes de mon code et à modifier le fichier datastructure.py. Dès que je lançais le programme, de nouveaux problèmes survenaient, et cela a duré pendant 3 jours. Cela devenait frustrant, et je me demandais si j'avais bien compris les consignes.

***Solutions*** : Mes camarades m'ont beaucoup aidé car tous les jours ils m'expliquaient ce qu'il fallait faire exactement et le résultat attendu.
De plus, en discutant entre nous, nous avons fait en sorte de nous simplifier les tâches. Tout d'abord, comme j'ai été la première à avoir finit l'exercice, j'ai partagé mon code à Nicolas et à Clara. Ainsi, ils ont pu reprendre la base de mon travail pour que l'on puisse avoir la même structure et faciliter l'étape du merge.


***Choix des merges*** : Pour le choix du merge, Clara et Nicolas ont repris le relais car malheureusement je ne peut travailler jusqu'à dimanche. Ainsi, comme ils ont terminé un peu plus tard, ils ont pu peaufiner notre fonction effectuer le merge.
