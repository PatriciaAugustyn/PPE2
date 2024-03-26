# Journal de Bord - TP9 Groupe 2

### Groupe :

- AUGUSTYN Patricia (Sorbonne Nouvelle) : Lien [GitHub](https://github.com/PatriciaAugustyn)
- Keming (INALCO)
- NGAUV Nicolas (INALCO)

## Séance du 13 mars 2024

## Keming :

J'ai continué sur l'exo 8 et 9.

**Exercice 8:** au début, j'ai réussi à sortir des données sous les trois formats du `read_corpus.py` prêts à passer à `analyzers.py`, mais malheureusement j'ai commité le `corpus_analyzed.json`, donc ça a crushé mon dépôt en local. J'ai essayé plusieurs façons par exemple `git revert` mais ça n'a rien changé, de plus j'ai perdu mon script (oui je ne l'ai pas sauvegardé :( , donc finalement au cours de merge, j'ai pris les scripts de Nicolas.

**Exercice 9:** heureusement, ce script n'a été perdu. Et la commande pour le lancer est : `python3 patterns.py -l json ./corpus_analyzed.json`, il faut d'abord télécharger le corpus sur iCampus.



## Nicolas :
**Informations et explications de l'exercice 7** : cf. partie du journal de Patricia ! Elle a très bien rédigé ;)

**Exercice 8** : 

Pour l'exercice 8, il a fallu réarranger le contenu des fichiers `analyzers.py` et `main.py` pour mieux distinguer leur rôles respectifs :
1. Comme indiqué dans la consigne, `main.py` se nomme donc maintenant `read_corpus.py` (mais j'ai décidé de laisser également une copie de `main.py`, au cas où... Au pire, à supprimer à la fin du TP !)
2. `analyzers.py` et `read_corpus.py` ont donc été modifiés pour permettre de combiner les deux tâches dans une *pipeline bash* à travers une commande de la forme : `python read_corpus.py <...> | python analyzers.py <...>` :
3. Voici un exemple de commandes :
    - `python3 read_corpus.py ../../Corpus/2024/01 -r etree -i glob -s 2024-01-26 -e 2024-01-29 -z pickle | python3 analyzers.py -s pickle -o test_s9_v2_spacy.pickle -a spacy`
    - Puis pour tester et voir que cela donne bien les résultats attendus :
        - `python3 patterns.py test_s9_v2_spacy.pickle -l pickle` pour un affichage des résultats dans le terminal
        - `python3 patterns.py test_s9_v2_spacy.pickle -l pickle > res_spacy.txt` pour rediriger la sortie standard dans un fichier
4. Je me suis occupé au début du format `pickle` avec le module `spacy` : cela fonctionne PARFAITEMENT (voir juste au dessus pour les exemples de commandes !) !!
5. Une fois cela fait, j'ai essayé de généraliser cela à tous les formats et tous les modules, pour par exemple pouvoir lancer des commandes comme :
    - `python3 read_corpus.py ../../Corpus/2024/01 -r etree -i glob -s 2024-01-26 -e 2024-01-29 -z pickle | python3 analyzers.py -s pickle -o test_s9.pickle -a trankit`
    - `python3 read_corpus.py ../../Corpus/2024/01 -r etree -i glob -s 2024-01-26 -e 2024-01-29 -z json | python3 analyzers.py -s json -o test_s9.json -a stanza`
    - `python3 read_corpus.py ../../Corpus/2024/01 -r etree -i glob -s 2024-01-26 -e 2024-01-29 -z xml | python3 analyzers.py -s xml -o test_s9.xml -a spacy`
    - Mais malheureusement, il y a pour le moment des erreurs (sans doute bêtes) que je n'arrive pas à corriger...
        - A la rigueur, on peut utiliser `pickle` avec les autres modules (`stanza` et `trankit`)  car les commandes suivantes fonctionnent (et c'est ce qui était demandé !!)
            - `python3 read_corpus.py ../../Corpus/2024/01 -r etree -i glob -s 2024-01-26 -e 2024-01-29 -z pickle | python3 analyzers.py -s pickle -o test_s9_v2_stanza.pickle -a stanza`
            - `python3 read_corpus.py ../../Corpus/2024/01 -r etree -i glob -s 2024-01-26 -e 2024-01-29 -z pickle | python3 analyzers.py -s pickle -o test_s9_v2_trankit.pickle -a trankit`
            - Mais c'est après qu'on peut avoir des problèmes, car ces commandes ne fonctionnent pas :
                - `python3 patterns.py test_s9_v2_stanza.pickle -l pickle`
                - `python3 patterns.py test_s9_v2_stanza.pickle -l pickle > res_stanza.txt`
                - `python3 patterns.py test_s9_v2_trankit.pickle -l pickle`
                - `python3 patterns.py test_s9_v2_trankit.pickle -l pickle > res_trankit.txt`
   - Pour s'assurer de résultats 100% fonctionnels, il vaut donc mieux utiliser le format `pickle` avec le module `spacy` (cf. les premiers exemples de commandes plus haut) car comme ça, tout est OK !


**Exercice 9** :

Cf. partie du journal :
- de Patricia (**Exercice 8 et 9**) 
- et de Keming
                


## Patricia :

#### Information :
Avec les garçons, nous avons décidé de nous répartir les tâches comme ceci :
- Keming travaillera sur la branche `ky-s9`
- Nicolas travaillera sur la branche `nn-s9`
- Quant à moi, je travaillerai sur la branche `pa-s9`

**Exercice 7** :

Pendant le cours, nous avons réalisé qu'il était important d'élargir notre code dans `patterns.py` pour capturer des relations plus complexes au sein de l'analyse `corpus_analyzes.json`.

Les patrons que nous avons extrait étaient efficaces pour capturer des relations simples. Par exemple, nous nous sommes concentrés sur **3** relations simples :

- "v -obj-> n", "VERB", "obj","NOUN"
- "n <-nsubj- v", "VERB", "nsubj", "NOUN"
- "n -nmod-> n", "NOUN","nmod", "NOUN"

Cependant, dans notre analyse il existe de nombreuses constructions syntaxiques qui sont considérées comme "*complexes*". Par exemple, avec des phrases ponctuelles, les subordonnées, les passives, etc...

sont courantes dans le langage naturel mais difficiles à capturer avec des patrons simples.
Approche adoptée

Pour cela, nous avons adopté une approche qui nous semblait correspondre à la continuité de ce que les professeurs nous sont expliqué. Cette fois-ci, nous ne sommes plus limiter à une seule relation de dépendance, mais plusieurs. Pour cela, nous avons ajouté une nouvelle fonction `complex_rel`, qui prend en compte un nombre d'élément :
```py
def complex_rel(rule_name: str, pos1: str,
                deprel1: str,
                pos2: str,
                deprel2: str,
                pos3: str
                ):
```
Comme en cours, nous avons commencé à chercher la structure illustré sur Grew Match. Lorsque, nous avons réussi, nous avons généralisé la structure de notre fonction comme dans `simple_rel`.
Ainsi, cela nous permet de spécifier des schémas de relations comme :
```py
# [...]
PATTERNS = [
        simple_rel("v -obj-> n", "VERB", "obj","NOUN"),
        simple_rel("n <-nsubj- v", "VERB", "nsubj", "NOUN"),
        simple_rel("n -nmod-> n", "NOUN","nmod", "NOUN"),
        complex_rel("v -xcomp-> v -mark-> adp", "VERB", "xcomp", "VERB", "mark", "ADP"),
        complex_rel("n -amod-> adj -nmod-> n", "NOUN", "amod", "ADJ", "nmod", "NOUN"),
        complex_rel("v -advmod-> adv -nmod-> n", "VERB", "advmod", "ADV", "nmod", "NOUN"),
        complex_rel("v -obl-> n -case-> adp", "VERB", "obl", "NOUN", "case", "ADP")
        ]
#[...]
```

**Exercice 8 et 9** :

Malheureusement, je n'ai pas réussi à faire les exercices 8 et 9 cette semaine. Cependant, Nicolas a repris le relai pour l'exercice 8 et Keming l'exercice 9 en se basant sur ce que nous avions fait en amont.
Heureusement, nous avons une excellente communication entre nous. Avec les garçons, cela s'est très bien passé car nous nous entraidons mutuellement. L'objectif est que chacun puisse progresser, et il n'est pas grave si nous n'avons pas réussi immédiatement, car si nous réussissions tout du premier coup, nous n'aurions pas besoin de nos professeurs. Je me sens ainsi plus à l'aise car cette état d'esprit me correspond mieux et n'est pas anxiogène.

Pour finir, nous avons continuer a avoir le même processus :

- j'ai commencé à réfléchir sur le premier exo
- Nicolas peut continuer sur cette lancée et corriger si besoin
- Keming qui peut finir l'exercice et faire le merge final







