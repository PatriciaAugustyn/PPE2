import networkx 
from pathlib import Path


@dataclass(frozen=True)
class Edge:
    pred: str
    arg: str
    count: int
    im: float





import argparse

parser = argparse.ArgumentParser

parser.add_argument("input_file", help="tableau avec les IM")
parser.add_argument("outpu_file", help="fichier de sortie gexf")
parser.add_argument("-c", help="noeud cible de départ")
parser.add_argument("-s", help="nbre de pas dans le grpahe", type=int)
parser.add_argument("-i", help="IM minimum", type=float)
parser.add_argument("-u", help="filtte les relations unique", action="store_true")
parser.add_argument("-f", help="filtre les feuilles", action="store_true")

args = parser.parse_args()

# python3 build_graphe.py ....tsv 
