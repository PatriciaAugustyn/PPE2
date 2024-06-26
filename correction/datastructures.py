from dataclasses import dataclass, asdict, field
from xml.etree import ElementTree as ET
from pathlib import Path
from typing import Optional, IO

import datetime
import json
import pickle
import sys

from dateutil import parser as dateparser


@dataclass
class Token:
    shape : str
    lemma : str
    pos : str
    dep : str
    gov : int


@dataclass
class Item:
    id : str  # élément guid (globally unique identifier) de l'item, sert à la déduplication
    source : str
    title : str
    description : str
    date : datetime.date
    categories : set[str]
    analysis : list[list[Token]] = field(default_factory=list)


@dataclass
class Corpus:
    # attention ! La liste ne gère pas en soit les guid (donc la déduplication).
    # Il faut soit :
    #    - faire une étape de déduplication en amont et supposer que cette liste est dédupliquée
    #    - changer le type vers dict[str, Item] où la clé (str) sera le guid de l'item.
    items : list[Item]


@dataclass(frozen=True)
class Match:
    rule: str
    lemmes: tuple[str, ...]
    pos: tuple[str, ...]
    relation: str


def save_xml(corpus : Corpus, output_file: Optional[Path]) -> None:
    root = ET.Element("corpus")
    for item in corpus.items:
        item_e = ET.SubElement(root, "item")

        id_e = ET.SubElement(item_e, "id")
        id_e.text = item.id

        source_e = ET.SubElement(item_e, "source")
        source_e.text = item.source

        title_e = ET.SubElement(item_e, "title")
        title_e.text = item.title

        description_e = ET.SubElement(item_e, "description")
        description_e.text = item.description

        date_e = ET.SubElement(item_e, "date")
        if item.date is not None:
            date_e.text = datetime.date.isoformat(item.date)

        categories_e = ET.SubElement(item_e, "categories")
        for cat in sorted(item.categories):
            cat_e = ET.SubElement(categories_e, "category")
            cat_e.text = cat

        analysis_e = ET.SubElement(item_e, "analysis")
        for sentence in item.analysis: 
            sent_e = ET.SubElement(analysis_e, "sentence")
            for token in sentence:
                token_e = ET.SubElement(sent_e, "token")
                shape_e = ET.SubElement(token_e, "shape").text = token.shape
                lemma_e = ET.SubElement(token_e, "lemma").text = token.lemma
                pos_e = ET.SubElement(token_e, "pos").text = token.pos
                pos_e = ET.SubElement(token_e, "dep").text = token.dep
                pos_e = ET.SubElement(token_e, "gov").text = str(token.gov)

    tree = ET.ElementTree(root)
    ET.indent(tree)  # for pretty printing
    if output_file:
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
    else:
        tree.write(sys.stdout, encoding="unicode", xml_declaration=True)


def load_xml(input_file: Optional[Path]) -> Corpus:
    if input_file:
        root = ET.parse(input_file)
    else:
        root = ET.parse(sys.stdin)

    corpus = Corpus([])

    for item in list(root.getroot()):
        item_date = item.find("date")
        if item_date is not None and item_date.text:
            item_date = dateparser.parse(item_date.text + " 00:00:00+00:00")
        else:
            item_date = None

        categories = set()
        for cat in list(item.find("categories")):
            categories.add(cat.text)

        analysis = []
        for sentence in list(item.find("analysis") or []):  # analysis node may not exist (previous versions)
            sentence = []
            for token in list(item.find("sentence") or []):  # analysis node may not exist (previous versions)
                sentence.append(Token(token.find("shape").text, token.find("lemma").text, token.find("pos").text, token.find("dep"), int(token.find("gov"))))
            analysis.append(sentence)

        corpus_item = Item(
            id = item.find("id").text,
            source = item.find("source").text,
            title = item.find("title").text,
            description = item.find("description").text,
            date = item_date,
            categories = categories,
            analysis = analysis
        )
        corpus.items.append(corpus_item)

    return corpus


def save_json(corpus : Corpus, output_file: Optional[Path]) -> None:
    data = []
    for item in corpus.items:
        the_date = None
        if item.date is not None:
            the_date = datetime.date.isoformat(item.date)

        current = {
            "id": item.id,
            "source": item.source,
            "title": item.title,
            "description": item.description,
            "date": the_date,
            "categories": sorted(item.categories),  # toujours avoir la même sérialisation (set n'est pas trié)
            "analysis": [[asdict(token) for token in sentence] for sentence in item.analysis]
        }
        data.append(current)

    if output_file:
        with open(output_file, "w") as output_stream:
            json.dump(data, output_stream, indent=2)
    else:
        json.dump(data, sys.stdout, indent=2)


def load_json(input_file: Optional[Path]) -> Corpus:
    def from_stream(input_stream: IO) -> list[Item]:
        return [
            Item(
                id=it["id"], 
                source=it["source"],
                title=it["title"],
                description=it["description"],
                date=it["date"] and datetime.date.fromisoformat(it["date"]),  # voir main.py pour syntaxe
                categories=set(it["categories"]),
                analysis = [
                    [
                        Token(token["shape"], token["lemma"], token["pos"], token["dep"], token["gov"])
                        for token in sentence
                    ]
                    for sentence in it.get("analysis",[]) 
                ]
            )
            for it in json.load(input_stream)
        ]

    corpus = Corpus([])
    if input_file:
        with open(input_file, "rb") as input_stream:
            corpus.items = from_stream(input_stream)
    else:
        corpus.items = from_stream(sys.stdin)

    return corpus


def save_pickle(corpus : Corpus, output_file: Optional[Path]) -> None:
    if output_file:
        with open(output_file, "wb") as output_stream:
            pickle.dump(corpus, output_stream)
    else:
        pickle.dump(corpus, sys.stdout.buffer)
        sys.stdout.flush()


def load_pickle(input_file: Optional[Path]) -> Corpus:
    if input_file:
        with open(input_file, "rb") as input_stream:
            return pickle.load(input_stream)
    else:
        return pickle.load(sys.stdin.buffer)


name2saver = {
    "xml": save_xml,
    "json": save_json,
    "pickle": save_pickle,
}

name2loader = {
    "xml": load_xml,
    "json": load_json,
    "pickle": load_pickle,
}
