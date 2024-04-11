"""
@author AUGUSTYN Patricia - BRISSET Lise

Guide d'utilisation :
Pour lancer la fonction, vous pouvez copier cette ligne de commande :
python3 visualisation.py -c exemple-information_mutuelle.tsv -n VERB-prendre-obj -s 5 -lu oui -ha oui

"""

import argparse
import csv


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


def filtre_seuil(corpus, seuil) -> list:
    """
    Fonction qui prend en entrée le corpus et applique un filtre sur les seuil des IMs.
    """

    liste_items_seuil = []

    for item in corpus:
        if float(item["IM"]) >= seuil:
            liste_items_seuil.append(item)

    return liste_items_seuil


def filtre_hapax(corpus, hapax) -> list:
    """
    Fonction qui prend en entrée la liste d'item, chaque item étant un dictionnaire.
    Ce qui est renvoyé est une liste de la même forme avec un filtrage des hapax.
    La fonction calcule aussi la fréquence de chaque lemme. Il est possible de retourner ces informations
    sous forme de liste de dictionnaire liste_frequence_dep et liste_frequence_gov.
    """

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


def filtre_lien_unique(corpus, lu) -> list:
    """
    Fonction qui filtre les données du corpus sur les liens uniques.
    """

    liste_items_lu = []

    for item in corpus:
        if int(item["compte"]) > 1:
            liste_items_lu.append(item)

    return liste_items_lu

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

        # On construit les noeuds
        f.write('    <nodes>\n')
        node_id = 0
        node_ids = {}  # On va stocker les id des noeuds déjà rencontrés
        for item in corpus_filtre:
            for lemme in [item["lemme_gov"], item["lemme_dep"]]:

                # On vérifie la catégorie et le lemme du nœud, sinon cela nous affiche une erreur
                if lemme == item["lemme_gov"]:
                    gov = item['categorie_gov']
                    lemme = item['lemme_gov']
                else:
                     gov = item['categorie_dep']
                     lemme = item['lemme_dep']

                # On va créer la catégorie, le lemme et la relation du nœud
                cat_mot_relation = label = f"{gov}-{lemme}-{item['relation']}"

                if lemme not in node_ids:
                    f.write(f'      <node id="{cat_mot_relation}" label="{label}">\n') # On remplit l'id et le label par le lemme
                    f.write('        <attvalues>\n')
                    f.write('          <attvalue for="0" value="1" />\n')  # On reprend les valeurs que dans l'exemple donné
                    f.write('        </attvalues>\n')
                    f.write('      </node>\n')
                    node_ids[lemme] = node_id
                    node_id += 1
        f.write('    </nodes>\n')

        # On construit les edges
        f.write('    <edges>\n')
        edge_id = 0 # On initialise l'id de l'edge
        for item in corpus_filtre:
            source_id = f"{item['categorie_gov']}-{item['lemme_gov']}-{item['relation']}"
            target_id = f"{item['categorie_dep']}-{item['lemme_dep']}-{item['relation']}"
            f.write(f'      <edge source="{source_id}" target="{target_id}" id="{edge_id}" />\n') # Comme dans les noeuds on reprend les valeurs
            edge_id += 1
        f.write('    </edges>\n')

        f.write('  </graph>\n')
        f.write('</gexf>')

    print("Le fichier graph_raw.gexf a été créé avec succès.")


def main():
    parser = argparse.ArgumentParser(
        description="Retourne les données sous format graphe."
    )

    parser.add_argument(
        "-c",
        "--corpus",
        type=str,
        help="Indiquer le corpus d'entrée sous format tsv.",
        default=None
    )

    parser.add_argument(
        "-n",
        "--noeud",
        type=str,
        help="Indiquer le noeud principal du graphe souhaité. Veuillez l'indiquer sous la forme POS-lemme-relation, ex : NOUN-avion-nmod ou VERB-lutter-contre",
        default=None
    )

    parser.add_argument(
        "-s",
        "--seuil",
        type=int,
        help="Indiquer le seuil minimum d'information mutuelle."
    )

    parser.add_argument(
        "-ha",
        "--hapax",
        choices=["oui", "non"],
        type=str,
        help="Indiquer si on souhaite prendre les hapax (lemme présent qu'une seule fois dans le corpus). 'oui' indique la présence d'hapax, 'non' l'inverse."
    )

    parser.add_argument(
        "-lu",
        "--lien-unique",
        choices=["oui", "non"],
        type=str,
        help="Indiquer si on souhaite prendre les patterns présents qu'une seule fois. 'oui' indique la présence de lien unique, 'non' l'inverse."
    )

    args = parser.parse_args()
    #print(args)

    corpus = tsv_to_list(args.corpus)  # on convertit les données du tsv en données manipulables par nos fonctions
    filtrage_noeud = filtre_noeud_voisin(corpus, args.noeud)  # filtrage sur le noeud principal
    filtrage_seuil = filtre_seuil(filtrage_noeud, args.seuil)  # filtrage sur le seuil IM min
    filtrage_hapax = filtre_hapax(filtrage_seuil, args.hapax)  # filtrage sur la présence d'hapax ou non
    corpus_filtre = filtre_lien_unique(filtrage_hapax, args.lien_unique)  # filtrage sur la présence de lien unique ou non

    # Conversion des données filtrées en graphe au format XML
    text_to_graph(corpus_filtre)


if __name__ == '__main__':
    main()

