# Journal de Bord - TP4 Groupe 14

### Groupe :

- AUGUSTYN Patricia (Sorbonne Nouvelle)
- SKRZYNIARZ Agata (INALCO)
- VIENOT Alix (Nanterre)

## Séance du 14 février 2024

### Patricia :

Pour ce TP, nous avons début par créer une branche doc et ajouté notre journal. Par la suite, nous nous sommes réparti les tâches comme ceci :

- r1 : Patricia utilisera le module **re** et des expressions régulières
- r2 : Alix utilisera le module **etree**
- r3 : Agata utilisera le module **feedparser**

Après la répartition des tâches et d'une discussion sur l'organisation générale, nous avons cherché de la documentation sur l'utilisation de nos modules.
Ainsi, nous avons continué le travail chez nous en communiquant régulièrement sur le groupe WhatsApp afin de nous tenir au courant de nos avancées, ou de discuter des éventuels obstacles rencontrés et proposé des solutions. Par exemple, nous avons eu des complications pour définir les métadonnées. Pendant le cours, nous avons voulu nous concentrer sur les balises < title></ title> et < description>< /description>, mais après une discussion nous avons améliorer la fonction en prenant en compte < pubDate></ pubDate>, < link></ link> et < category></ category>.

De plus, pour l'étape finale nous avons travaillé ensemble. Pour cela, nous avons décidé de merger unanimement la branche r1 et créé la fonction finale.

Nous avons beaucoup communiquer et nous avons réalisé un travail régulier jusqu'à présent. En résumé, notre travail en groupe sur ce nouveau TP a été très satisfaisant, grâce à une organisation claire, une répartition efficace des tâches et une communication constante.

### Agata :

Dans cette tâche, j'étais responsable de la fonction r3 (module feedparser), que j'ai créée en utilisant la documentation qui nous a été donnée. Après avoir fusionné toutes les fonctions, les filles et moi nous sommes réunies pour créer ensemble la fonction finale.

### Alix :
Pour la fonction r2 avec etree, j'ai choisi d'utiliser deux boucles, qui permettent d'itérer sur les < item> et de trouver les balise < title>, < description>, < category> et < pubDate>. A partir de là la ```fonction item.findtext('pubDate')```du module etree est utilisé pour récupérer le contenu textuel de la balise.
Le contenu des balises est rajouté a une liste qui reprend les différents types de renseignement présent dans les balises. Comme la liste category qui contient toutes les catégories présentes dans le document. 
Pour traiter les corpus avec etree : il faut utiliser 
```tree = ET.parse('Corpus/sample.xml') root = tree.getroot()```
