# Journal de Bord - TP9 Groupe 2

### Groupe :

- AUGUSTYN Patricia (Sorbonne Nouvelle) : Lien [GitHub](https://github.com/PatriciaAugustyn)
- Keming (INALCO)
- NGAUV Nicolas (INALCO)

## Séance du 27 mars 2024

## Keming :

#### Exo 1 :

La semaine dernière, j'ai déjà fini une partie de cet exercice. J'ai fait que les patterns avec `verb` et `noun`. Et cette semaine, le but est de généraliser pour tous les patterns.

1. J'ai envelé les flèches et le tiret dans la relation pour que ça soit plus propre.
2. J'ai ajouté la fonction de `sort` pour que le tableau s'affiche selon l'order d'IM.

#### Relecture : 

J'ai relu le script de Patricia. Tout est bon, sauf que dans la calculation d'IM, qui était une erreur de ma partie de la semaine dernière :

```python
for (predicate, argument), cooccur_count in cooccurrences.items():
        p_predicate = cooccur_count / total_matches
        p_argument = cooccur_count / total_matches
        p_cooccur = cooccur_count / total_matches
```

dans la formule, j'ai mis trois fois la même chose.

## Nicolas :

#### Informations :
Cf. partie du journal de Patricia ;)

**Exercice 1** :
- Pour éviter les répétitions inutiles et alourdir le contenu du journal artificiellement je ne vais pas détailler le contenu de l'exercice 1 : Patricia l'a très bien fait dans sa partie du journal !
- Je vais juste dire que Keming avait fait du bon travail pour l'exercice 9 au TP dernier : en effet il avait déjà commencé à travailler sur l'information mutuelle et regrouper toutes les informations importantes dans un fichier csv de manière organisée ! 
    - Son travail produisait un fichier csv avec ce qui était demandé (nommé `results.csv`), mais seulement pour le patron de relation simple `v --obj-> n`. 
- Notre travail pour cette semaine était donc de généraliser cela à l'ensemble des patrons.
    - Commande à lancer pour tester l'**exercice 1** de cette semaine (`corpus_analyzed.json` étant l'extrait de corpus analysé, disponible sur iCampus) : 
        - `python3 patterns.py -l json ./corpus_analyzed.json`.
        - Pour ma version de l'**exercice 1**, cela produit un fichier `resultats.csv` dans le dossier courant dans lequel sont enregistrés tous les résultats demandés.

**Exercice 2 et 3** :
- Relecture :
    - Mon tag de fin pour ma version de l'exercice 1 : `nn-s10exo1-fin`
    - J'ai relu la version de Keming (branche `ky-s10`): ça fonctionne, rien à dire ! J'y ai déposé le tag de relecture suivant : `ky-s10-relu`.
- Merge :
    - Pour le merge, on a comparé et discuté de nos différentes branches, et on a décidé que je ferai le merge de ma branche (`nn-s10`):
        - Keming et moi n'obtenons pas les mêmes valeurs que Patricia pour l'information mutuelle car nos formules diffèrent légèrement
        - Keming n'a pas gardé le sens des flèches des relations des patterns mais a classé les patterns selon une valeur décroissante de l'information mutuelle, permettant de voir plus facilement quel pattern a une IM élevée ou non ; quant à moi j'ai gardé les sens des flèches des relations des patterns (car le sens peut être différent selon les patterns capturés, et je ne veux pas perdre cette information) et je n'ai pas classé les patterns par ordre décroissant de la valeur de leur information mutuelle car ainsi, nous sommes capable de voir les patterns dans l'ordre de leur découverte.
- Difficultés et solutions : 
    - Pas de difficultés particulières cette semaine, car j'ai la chance d'avoir des camarades de groupe formidables, qui travaillent bien et communiquent beaucoup ! Merci à Patricia et Keming !!


## Patricia :

#### Information :
Avec les garçons, nous avons décidé de nous répartir les tâches comme ceci :
- Keming travaillera sur la branche `ky-s10`
- Nicolas travaillera sur la branche `nn-s10`
- Quant à moi, je travaillerai sur la branche `pa-s10`

**Exercice 1** :
La semaine dernière, Keming a travaillé sur le calcul de l'information mutuelle entre les prédicats et les arguments de notre corpus. Les résultats obtenus nous semblaient *corrects* car pendant le cours nous avons vérifié sur le site : http://redac.univ-tlse2.fr/voisinsdelemonde/infos/apropos.jsp, et les résultats étaient similaires à ceux obtenus à partir du script `patterns.py`.
Au début, nous avons été intrigués par les valeurs IM car elle étaient supérieures à 10. Mais, en comparant avec la formule mathématique et les IM du site, nous avons constaté qu'elles étaient totalement cohérentes.

Par ailleurs, Keming avait seulement testé avec un seul pattern `simple_rel("v -obj-> n", "VERB", "obj","NOUN")`. DOnc, nous avons décidé d'améliorer cela pour prendre tous nos patterns et obtenir un tableau *complet*. Pour cela, j'ai modifier la fonction `main()` pour modifier les colonnes prédicat, relation et catégorie dans notre sortie afin de correspondre à la structure du tableau.

Voici la partie que j'ai ajouté dans `patterns.py` :

```py
#[...]

    with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['prédicat', 'lemme', 'relation', 'categorie', 'lemme', 'frequence', 'IM']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        for match in all_matches:

        # On va extraire les informations de nos match

            relation = match.rule.split()[1]
            predicate_category = match.rule.split()[0]
            predicate_lemma = match.lemmes[0]
            argument_category = match.rule.split()[-1]
            argument_lemma = match.lemmes[1]
            frequency = cooccurrences[(predicate_lemma, argument_lemma)]
            im_value = im_results[(predicate_lemma, argument_lemma)]

            writer.writerow([predicate_category, predicate_lemma, relation, argument_category, argument_lemma, frequency, im_value])
#[...]
```

L'objectif de cette partie était d'extraire les informations de nos match avec le prédicat, le lemme, la relation, la catégorie, le lemme, la fréquence et l'IM afin de **stocker** les résultats un fichier CSV (pour nous permettre de visualiser nos résultats la semaine prochaine).

**Relecture** :
Mon tag de fin sur l'exercice 1 : `pa-s10-fin`

Par la suite, j'ai relu la branche de Nicolas sur la branche `nn-s10`, et le tag est sous le nom `nn-s10-relu`.

Comme d'habitude, le travail de mon camarade Nicolas est excellent :)

Par ailleurs, nous avons remarqué que notre résultat d'IM est différent. Par mesure de sécurité, je préfère faire confiance à Nicolas et Keming.
