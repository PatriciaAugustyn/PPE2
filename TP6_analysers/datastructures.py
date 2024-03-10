#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree
import feedparser
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass, field, asdict
from rss_reader import read_rss_etree, read_rss_feedparser, read_rss_re
import json
import pickle

@dataclass
class Token:
    forme: str
    lemme: str
    pos:str

@dataclass
class Item:
    title: str
    description: str
    pubDate: str
    category: List[str]
    source: str
    tokens: list[Token] = field(default_factory=list)


    def as_dict(self) -> dict:
        """
        Convertir Item en un dictionnaire.
        """
        return {
            'title': self.title,
            'description': self.description,
            'pubDate': self.pubDate,
            'category': self.category,
            'source': self.source,
            "analyse": (self.tokens.forme, self.tokens.lemme, self.tokens.pos)
        }


@dataclass
class Corpus:
    #folder: str | Path
    items: list[Item] = field(default_factory=list)

    def iterate_pathlib_glob(self) -> list:
        return sorted(Path(self.folder).glob("**/*.xml"))

    def read_rss_re(self, filename: str | Path) -> list[dict]:
        return read_rss_re(filename)

    def read_rss_etree(self, filename: str | Path) -> list[dict]:
        return read_rss_etree(filename)

    def read_rss_feedparser(self, filename: str | Path) -> list[dict]:
        return read_rss_feedparser(filename)

    def __iter__(self):
        return iter(self.items)


# fonctions sauvegarde et chargement

def save_json(corpus: Corpus, output_file: Path) -> None:
    output_file = Path(output_file)
    """Sauvegarder sous le format json"""
    try:
        with output_file.open('w', encoding='utf-8') as f:
            json.dump([asdict(item) for item in corpus.items], f, ensure_ascii=False, indent=4)
            print("Les données ont été enregistrées sous le format JSON")
    except Exception as e:
        print(f"Erreur : {e}")


def load_json(input_file: Path) -> Corpus:
    with open(input_file, 'r') as f:
        corpus = json.load(f)
    return Corpus(items=[Item(**item) for item in corpus])


def save_pickle(corpus: Corpus, output_file: Path) -> None:
    """Sauvegarde le corpus dans un fichier au format pickle."""
    with open(output_file, 'wb') as f:
        pickle.dump(corpus, f)

def load_pickle(input_file: Path) -> Corpus:
    """Charge le corpus depuis un fichier au format pickle."""
    with open(input_file, 'rb') as f:
        corpus = pickle.load(f)
        for item in corpus.items:
            if not hasattr(item, 'pubdate'):
                item.pubDate = ''
            if not hasattr(item, 'category'):
                item.category = ''
    return corpus

#fonction save_xml et load_xml
def save_xml(corpus: Corpus, fichier_sortie: str):
    racine = ET.Element("data")
    for item in corpus.items:
        element_item = ET.SubElement(racine, "item")
        ET.SubElement(element_item, "source").text = item.source if item.source is not None else 'Inconnue'
        ET.SubElement(element_item, "title").text = item.title if item.title is not None else 'Sans titre'
        ET.SubElement(element_item, "description").text = item.description if item.description is not None else 'Sans description'
        ET.SubElement(element_item, "pubDate").text = item.pubDate if item.pubDate is not None else 'Sans date'
        tokens = ET.SubElement(element_item, "tokens")
        for token in item.tokens:
            token_node = ET.SubElement(tokens, "token")
            ET.SubElement(token_node, "forme").text = token.forme
            ET.SubElement(token_node, "lemme").text = token.lemme
            ET.SubElement(token_node, "pos").text = token.pos
        # Créer les sous-éléments pour les catégories, en vérifiant si la clé 'categories' existe
        categories = item.category if item.category is not None else [] # Si 'categories' n'existe pas, utilisez une liste vide comme valeur par défaut
        for categorie in categories:
            ET.SubElement(element_item, "category").text = categorie
    arbre = ET.ElementTree(racine)
    with open(fichier_sortie, "wb") as fichier:
        arbre.write(fichier)

def load_xml(input_file: Path):
    with open(input_file, 'r', encoding="utf-8") as file:
        tree = ET.parse(file)
        root = tree.getroot()
        items = root.findall('.//item')
        list_items = []
        for item in items:
            data = Item("", "", "", "", [], [])
            titre = item.find('title').text if item.find('title') is not None else ''
            data.title = titre
            description = item.find('description').text if item.find('description') is not None else ''
            data.description = description
            categories = item.findall('category')
            if categories:
                data.category.extend([categorie.text for categorie in categories])
            date = item.find('pubDate').text if item.find('pubDate') is not None else ''
            data.pubDate = date
            source = item.find('source').text if item.find('source') is not None else ''
            data.source = source
            tokens = item.find('tokens')
            if tokens is not None:
                for token_element in tokens.findall('token'):
                    forme = token_element.find('forme').text if token_element.find('forme') is not None else ''
                    lemme = token_element.find('lemme').text if token_element.find('lemme') is not None else ''
                    pos = token_element.find('pos').text if token_element.find('pos') is not None else ''
                    token = Token(forme, lemme, pos)
                    data.tokens.append(token)
            list_items.append(data)
        corpus = Corpus(list_items)
    return corpus

def load(input_file: str) -> Corpus:
    input_file = Path(input_file)
    extension = input_file.suffix
    if extension == ".xml":
        return load_xml(input_file)
    elif extension == ".json":
        return load_json(input_file)
    elif extension == ".pickle":
        return load_pickle(input_file)
    else:
        raise ValueError(f"Format de fichier non géré: {extension}")

def save(corpus: Corpus, output_file: str) -> None:
    output_file = Path(output_file)
    extension = output_file.suffix
    if extension == ".xml":
        save_xml(corpus, output_file)
    elif extension == ".json":
        save_json(corpus, output_file)
    elif extension == ".pickle":
        save_pickle(corpus, output_file)
    else:
        raise ValueError(f"Format de fichier non géré: {extension}")
