#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 22:53:28 2024

@author: lydia
"""

import argparse
import csv
from dataclasses import dataclass
from typing import List, Dict
import networkx as nx

@dataclass
class Occurrence:
    categorie_gov: str
    lemme_gov: str
    relation: str
    categorie_dep: str
    lemme_dep: str
    compte: int
    IM: float

@dataclass
class Data:
    occurrences: List[Occurrence]

def tsv_to_data(fichier) -> Data:
    with open(fichier, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)  # Skip header
        occurrences = []
        for row in reader:
            if len(row) == 7:
                occurrence = Occurrence(
                    categorie_gov=row[0],
                    lemme_gov=row[1],
                    relation=row[2],
                    categorie_dep=row[3],
                    lemme_dep=row[4],
                    compte=int(row[5]),
                    IM=float(row[6])
                )
                occurrences.append(occurrence)
    return Data(occurrences)

def filtre_seuil(data: Data, seuil: float) -> Data:
    return Data([o for o in data.occurrences if o.IM >= seuil])

def filtre_noeud_voisin(data: Data, noeud_str: str) -> Data:
    categorie, lemme, relation = noeud_str.split("-")
    liste_items_voisins = [o for o in data.occurrences if
                           o.categorie_gov == categorie and
                           o.lemme_gov == lemme and
                           o.relation == relation]
    return Data(liste_items_voisins)

def filtre_hapax(data: Data) -> Data:
    lemme_compte: Dict[str, int] = {}
    for o in data.occurrences:
        lemme_compte[o.lemme_gov] = lemme_compte.get(o.lemme_gov, 0) + 1
        lemme_compte[o.lemme_dep] = lemme_compte.get(o.lemme_dep, 0) + 1
    return Data([o for o in data.occurrences if lemme_compte[o.lemme_gov] > 1 and lemme_compte[o.lemme_dep] > 1])

def filtre_liens_uniques(data: Data) -> Data:
    relation_compte: Dict[tuple, int] = {}
    for o in data.occurrences:
        cle = (o.lemme_gov, o.lemme_dep, o.relation)
        relation_compte[cle] = relation_compte.get(cle, 0) + 1
    return Data([o for o in data.occurrences if relation_compte[(o.lemme_gov, o.lemme_dep, o.relation)] > 1])

def construire_graphe_etendu(data: Data, output_path: str):
    G = nx.Graph()
    for occ in data.occurrences:
        id_gov = f"{occ.categorie_gov}-{occ.lemme_gov}-{occ.relation}"
        id_dep = f"{occ.categorie_dep}-{occ.lemme_dep}-{occ.relation}"
        if id_gov not in G:
            G.add_node(id_gov, categorie=occ.categorie_gov, lemme=occ.lemme_gov, relation=occ.relation)
        if id_dep not in G:
            G.add_node(id_dep, categorie=occ.categorie_dep, lemme=occ.lemme_dep, relation=occ.relation)
        G.add_edge(id_gov, id_dep)
    nx.write_gexf(G, output_path)
    print(f"Le graphe a été sauvegardé dans {output_path}.")

def main():
    parser = argparse.ArgumentParser(description="Analyse linguistique et génération de graphe.")
    parser.add_argument("-c", "--corpus", required=True, help="Chemin vers le fichier corpus TSV.")
    parser.add_argument("-s", "--seuil", type=float, default=0.0, help="Seuil minimum d'information mutuelle.")
    parser.add_argument("--hapax", action='store_true', help="Appliquer le filtre hapax.")
    parser.add_argument("--lien-unique", action='store_true', help="Appliquer le filtre de liens uniques.")
    parser.add_argument("-o", "--output", required=True, help="Chemin du fichier de sortie GEXF.")
    parser.add_argument("-n", "--noeud", required=True, help="Noeud central sous forme CATEGORIE-LEMME-RELATION.")

    args = parser.parse_args()

    data = tsv_to_data(args.corpus)
    if args.hapax:
        data = filtre_hapax(data)
    if args.lien_unique:
        data = filtre_liens_uniques(data)
    data = filtre_noeud_voisin(data, args.noeud)
    data = filtre_seuil(data, args.seuil)

    construire_graphe_etendu(data, args.output)



if __name__ == '__main__':
    main()

