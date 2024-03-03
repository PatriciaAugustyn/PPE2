# Journal de Bord - TP5 Groupe 6

### Groupe :

- AUGUSTYN Patricia (Sorbonne Nouvelle) : Lien [GitHub](https://github.com/PatriciaAugustyn)
- Zineb (Nanterre)

- Natalia (INALCO)
- Anastasiia (INALCO)

## Séance du 28 février 2024

### Patricia :

**Commentaire :**
Le journal de cette semaine se nomme :
>journal-s3.md

Nous avons décidé de le renommer comme ceci car les journaux précédant ont été appelé :
>journal.md
>journal-s2.md

Ensuite, pour le premier exercice, nous avons décidé de renommer nos branches :
>pa-s6-ex1   //   ZC-s6-exo1

Pour le deuxième exercice, nous avons décidé de les renommer :
>pa-s6-r3   //   ZC-s6-r2

**Exercice 1 :**

Cette semaine, nous avons repris le code du Groupe 6 pour le projet PPE2. Dans un premier temps, j'ai pris le temps de le comprendre et de m'assurer comment le lancer. Avec ma camarade Zina, nous avons rencontré des complications en cours pour exécuter le script, mais après avoir examiné le code plus attentivement chez nous, nous avons pu le comprendre et le lancer correctement.

Cependant, il est important de noter que le script présente des différences radicales en termes de format de sortie, et il est difficile de tout modifier pour correspondre à nos besoins. J'ai essayé d'apporter des modifications pour que le format de sortie soit correct.

En ce qui concerne l'exercice 1, j'ai rencontré des difficultés à comprendre comment faire fonctionner un script main.py avec trois scripts Python distincts (datastructures.py, rss_reader.py, rss_filtrage.py). Pour cela, je me suis renseignée en cherchant de la documentation, et voici comment nous pouvons faire :

```py
from rss_filtrage import parcourir_corpus, choix_filtrage, afficher_resultats
```

**Exercice 4** :

Difficultés :
Nous avons rencontré des problèmes liés au merge lors de l'exercice 1, comme Zina l'a expliqué précédemment. De plus, lorsque j'ai commencé à travailler sur l'exercice 2 pendant la semaine. Lors du push de ma partie sur ma branche, j'avais oublié d'enlever l'appel de mes fonctions, ce qui a compliqué le processus de merge.

Solutions :
Pour résoudre les problèmes liés au merge de l'exercice 1, Zina a supprimé le fichier rss_parcours.py pour laisser la même structure que dans le main (laissé par le groupe précédent). Ainsi, en ayant deux fichiers python (rss_reader.py et rss_filtrage.py), nous avons décidé que rss_parcours serait le document rss_filtrage.
En ce qui concerne mon oubli de l'appel de la fonction dans le main (r3), Zina a pu ajuster le code avant le merge, puis intégrer les changements avec le fichier principal.

Choix des merges :
Nous avons décidé de répartir les tâches en fonction de nos disponibilités. Comme je ne pouvais travailler que jusqu'à dimanche et Zina jusqu'à lundi, nous avons convenu que Zina serait responsable des merges. Ainsi, cela nous a permis de maximiser le temps de travail et d'assurer les rôles de chacune.

Conseils pour le groupe suivant :
- En ouvrant le fichier main.py vous trouverez des explications sur comment faire fonctionner le script avec des exemples
- Vous trouverez aussi ce journal pour compléter les explications

### Zina :
#### Exercice 1 :
Nous avons essayé de trouver la commande afin d'exécuter le script, on a fini par trouver avec help : 
python3 rss_filtre.py (--re | --etree | --feedparser) [--corpus CORPUS_PATH] [--date] [--date-debut DATE]
                       [--date-fin DATE] [--category CATEGORY]

exemple avec un filtre sur dates uniquement : python3 rss_filtrage.py --etree --corpus ../2024/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100" 

Comme demandé sur la feuille d'exercices, après différents tests, et notamment tests des différents filtres, nous nous sommes assurées que le code fonctionnait correctement (etree, re, feedparser, et filtre par date et catégorie),mais on a tout de même constaté que filtre sur la source ne fonctionnait pas

Cependant par rapport à la consigne "les parties non fonctionnelles ne doivent pas être proposées lors de l’appel à une fonction principale (à supprimer de l’ArgmentParser)", je ne sais pas si il faut supprimer le choix sur le filtre de source, ou si il faut le corriger, on a choisit de faire au mieux pour le corriger, et si ça ne marche toujours pas, on met le l'argmentparser concerné en commentaire.

Nous avons créé les différents fichiers séparément :
datastructures.py contenant les dataclass, a été implémenté par Patricia  
Les deux fichiers déjà présents sur le projet :  
- rss_reader.py contenant le code pour lire un unique fichier RSS 
- rss_parcours.py qui parcours l'arborescence de fichiers RSS + filtre selon le choix, où j'ai fait en sorte de faire foncrtionner le filtre par source
Et finalement, le main.py où les différentes fonctions seront appelées comme on appelle n'importe quel module/librairie sur python, et donc de cette façon :

    from lenomdufichierpython import lenomdelafonctionàutiliser 

en s'assurant bien que le fichier est dans le même répertoire 

Difficultés :
Cette fois-ci j'ai rencontré beaucoup de difficultés lors du merge des deux branches (PA et ZC), et après plusieurs tentatives (ratées) afin de résoudre le conflit, j'ai simplement fini par supprimer la source du conflit sur ma branche qui était le fichier rss_filtrage présent dans les deux branches 

Note importante : rss_filtrage est l'équivalent du fichier rss_parcours demandé dans les consignes, nous avons préféré ne pas le renommer car nous avios déjà deux fichiers sur le projet dont nous avons hérité : rss_filtrage et rss_reader, le recommer aurait créé des conflits à la fin.
De mon côté, je l'ai renommé au debut, et effectivement j'ai eu des soucis lors du merge avec Patricia

Modififcations des différents programmes après tests (principalement noms des variables), commande pour exécuter : 
python3 main.py --etree --corpus ../2024/ --date --date-debut "Fri, 29 Jan 2024 18:14:09 +0100" --date-fin "Mon, 12 Feb 2024 21:30:09 +0100" --category "nom catégorie" (source ne fonctionne pas, donc choix mis en commentaire)

On a choisi de fusionner avec ma branche afin que j'effectue les tests étant donné que le code de Patricia fonctionnait, mais que je devais ajouter la fonction de source.

### Anastasiia :

### Natalia :


### Remarque :

Cette semaine, il n'y a que ma camarade Zina et moi (Patricia) qui avons contribué au projet. Nous avons mis beaucoup d'efforts pour atteindre les objectifs fixés. Cependant, Anastasiia et Natalia n'ont pas participé, et malgré nos tentatives de communication via WhatsApp, aucune des deux nous ont répondu.

Dans notre démarche, nous avons veillé à répondre à chaque critère nécessaire, mais il est important de souligner que nous ne pouvons pas faire le travail des autres membres du groupe. Le manque de temps a également joué dans cette situation, car nous n'avons pas pu faire la fonction r1, qui était initialement assignée à Anastasiia et Natalia.

Malgré cette situation, avec Zina nous avons maintenu une cohésion de groupe. Comme nous avons déjà travaillé ensemble, nous nous sommes naturellemnt réparti les tâches et nous avons beaucoup discuté des choix à faire.
