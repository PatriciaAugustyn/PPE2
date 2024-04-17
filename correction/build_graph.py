from typing import Optional
from dataclasses import dataclass
from collections import Counter
import sys

import networkx as nx
from pathlib import Path

@dataclass(frozen=True)
class Edge:
    pred: str
    arg: str
    count: int
    im: float

def load_data(path:Path, filter_im=None, filter_unique=None):
    lines = [tuple(l.split("\t")) for l in path.read_text().splitlines()[1:]]
    edges = [ Edge("-".join(l[0:3]), "-".join(l[3:5]), int(l[5]), float(l[6])) for l in lines]
    if filter_im:
        edges = [e for e in edges if e.im > filter_im]
    if filter_unique:
        edges = [e for e in edges if e.count > 1]
    return edges




def select(edges:list[Edge], 
           cible: str, 
           l_max:int=2, 
           v_max: Optional[int]=None, 
           acc:Optional[set[Edge]]=None, 
           nodes: Optional[set[str]]=None):
    acc = acc or set()
    nodes = nodes or {cible,}
    print(l_max, len(nodes))
    if l_max == 0 or (v_max and v_max < len(nodes)):
        return acc
    else:
        nodes_to_add = set()
        for e in edges:
            if (e.pred in nodes) or (e.arg in nodes):
                nodes_to_add.add(e.pred)
                nodes_to_add.add(e.arg)
                acc.add(e)
        nodes = nodes.union(nodes_to_add)
        return select(edges, cible, l_max-1, v_max, acc, nodes)

def remove_feuilles(edges: list[Edge])->list[Edge]:
    pred_counter = Counter([e.pred for e in edges])
    arg_counter = Counter([e.arg for e in edges])
    return [e for e in edges if pred_counter[e.pred] > 1 or arg_counter[e.arg] > 1]


def nx_analysis_and_save(edges: list[Edge], output_file: str):
    g = nx.Graph()
    for e in edges:
        g.add_edge(e.pred, e.arg, weight=e.im)
        g.nodes[e.pred]['class'] = "pred"
        g.nodes[e.arg]['class'] = "arg"

    louvain = nx.community.louvain_communities(g)
    for i, nodes in enumerate(louvain):
        for node_id in nodes:
            g.nodes[node_id]["louvain"] = str(i)

    layout = {}
    layout = nx.spring_layout(g, scale=1000)
    pagerank = nx.link_analysis.pagerank(g)
    for node_id, position in layout.items():
        g.nodes[node_id]["viz"] = {"position": {"x":position[0], "y":position[1]}}
        g.nodes[node_id]["pagerank"] = pagerank[node_id]
    nx.write_gexf(g, output_file)


def main(input_file, output_file, cible, steps=3, filter_im=1.0, filter_unique=False, filter_feuilles=False):
    data = load_data(Path("./output-semifull-spacy.tsv"), filter_im, filter_unique)
    edges = select(data,cible, steps)
    if filter_feuilles:
        edges = remove_feuilles(edges)
    nx_analysis_and_save(edges, output_file)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="tableau avec les IM")
    parser.add_argument("output_file", help="fichier de sortie en gexf")
    parser.add_argument("-c", help="nœud cible de départ")
    parser.add_argument("-s", help="nombre de pas dans le graphe (steps)", type=int)
    parser.add_argument("-i", help="information mutelle minimum", type=float)
    parser.add_argument("-u", help="filtre les relations uniques", action='store_true') 
    parser.add_argument("-f", help="filtre les feuilles", action='store_true')
    
    args = parser.parse_args()
    main(
            args.input_file,
            args.output_file,
            args.c,
            args.s,
            args.i,
            args.u,
            args.f
            )


